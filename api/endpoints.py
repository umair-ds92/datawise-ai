"""
DataWise AI - FastAPI REST API
Programmatic access to data analysis capabilities
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import uuid
import os
from pathlib import Path
from datetime import datetime

from team.analyzer_gpt import create_basic_team
from config.openai_model_client import get_model_client
from config.docker_utils import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container
)
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from utils.validators import validate_file, validate_task
from utils.metrics import metrics_tracker
from utils.logging import agent_logger

# ============================================
# APP SETUP
# ============================================
app = FastAPI(
    title="DataWise AI API",
    description="Multi-agent data analysis REST API",
    version="1.0.0"
)

# In-memory job storage (use Redis in production)
jobs = {}


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================
class AnalysisRequest(BaseModel):
    task: str
    session_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[list] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


# ============================================
# ROUTES
# ============================================
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "DataWise AI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_jobs": len([j for j in jobs.values() if j["status"] == "running"])
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a data file for analysis

    Returns file_id to reference in analysis requests
    """
    # Validate file
    content = await file.read()
    is_valid, error_msg = validate_file(file.filename, len(content))

    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Save to temp directory
    os.makedirs('temp', exist_ok=True)
    file_path = f"temp/data.csv"
    with open(file_path, 'wb') as f:
        f.write(content)

    agent_logger.log_file_event("Uploaded via API", file.filename)

    return {
        "status": "success",
        "filename": file.filename,
        "size_kb": round(len(content) / 1024, 2),
        "message": "File ready for analysis"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start an analysis job (async)

    Returns job_id to check status and results
    """
    # Validate task
    is_valid, error_msg = validate_task(request.task)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Create job
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "task": request.task,
        "result": None,
        "error": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }

    # Run in background
    background_tasks.add_task(run_analysis_job, job_id, request.task)

    return AnalysisResponse(
        job_id=job_id,
        status="queued",
        message=f"Analysis started. Check status at /jobs/{job_id}"
    )


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get status and results of an analysis job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    job = jobs[job_id]
    return JobStatus(**job)


@app.get("/jobs")
async def list_jobs():
    """List all analysis jobs"""
    return {
        "total": len(jobs),
        "jobs": list(jobs.values())
    }


@app.get("/output/{filename}")
async def get_output_file(filename: str):
    """Download a generated output file (e.g. charts)"""
    file_path = f"temp/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")

    return FileResponse(file_path)


@app.get("/metrics")
async def get_metrics():
    """Get current session metrics"""
    return metrics_tracker.get_session_summary()


# ============================================
# BACKGROUND JOB RUNNER
# ============================================
async def run_analysis_job(job_id: str, task: str):
    """Run analysis as a background job"""
    jobs[job_id]["status"] = "running"
    messages = []

    model_client = get_model_client()
    docker = getDockerCommandLineExecutor()
    team = create_basic_team(docker, model_client)

    metrics_tracker.start_task(task)

    try:
        await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                messages.append({
                    "source": message.source,
                    "content": message.content
                })
            elif isinstance(message, TaskResult):
                messages.append({
                    "source": "system",
                    "content": f"Stop reason: {message.stop_reason}"
                })

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = messages
        jobs[job_id]["completed_at"] = datetime.now().isoformat()

        metrics_tracker.end_task(status='success')

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        metrics_tracker.end_task(status='error')
        agent_logger.log_error(e, context=f'job_{job_id}')

    finally:
        await stop_docker_container(docker)


# ============================================
# RUN SERVER
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)