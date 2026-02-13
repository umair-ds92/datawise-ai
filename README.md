# DataWise AI 

> AI-powered multi-agent data analysis platform that transforms raw data into actionable insights

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.7.5-green.svg)](https://github.com/microsoft/autogen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

DataWise AI leverages AutoGen's multi-agent framework to analyze, visualize, and explain data through natural language. Simply upload your dataset and ask questions - specialized AI agents collaborate to deliver comprehensive insights automatically.

## Features

- **Natural Language Queries** - Interact with data using plain English
- **Automated Visualizations** - Generate publication-ready charts automatically
- **Statistical Analysis** - Deep insights powered by specialized agents
- **Secure Code Execution** - Isolated Docker environments for safety
- **Multi-Agent Collaboration** - Coordinated teamwork for complex analysis
- **Web & API Interfaces** - Streamlit UI and REST endpoints
- **Cost Tracking** - Monitor API usage and expenses in real-time
- **Session State** - Continue analysis across sessions

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (for code execution)
- OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/umair-ds92/datawise-ai.git
cd datawise-ai

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run Application

```bash
# Web Interface (Port 8501)
streamlit run streamlit_app.py

# CLI Interface
python main.py --interactive

# API Server (Port 8000)
python api/endpoints.py

# Monitoring Dashboard (Port 8502)
streamlit run monitoring/dashboard.py --server.port 8502

# Docker (All services)
docker-compose up
```

## Project Structure

```
datawise-ai/
├── config/               # Configuration and settings
├── agents/               # AI agent definitions
│   ├── Data_Analyzer_agent.py
│   ├── Code_Executor_agent.py
│   ├── Visualization_agent.py
│   └── Statistics_agent.py
├── team/                 # Multi-agent orchestration
│   ├── analyzer_gpt.py
│   ├── selector.py
│   ├── termination_conditions.py
│   └── handoffs.py
├── utils/                # Utilities
│   ├── logging.py
│   ├── state_manager.py
│   ├── file_handler.py
│   ├── validators.py
│   ├── error_handlers.py
│   ├── cache.py
│   └── metrics.py
├── api/                  # REST API endpoints
├── monitoring/           # Monitoring dashboard
├── tests/                # Test suite
├── data/                 # Data storage (uploads/outputs)
├── main.py               # CLI entry point
├── streamlit_app.py      # Web interface
├── requirements.txt      # Dependencies
├── docker-compose.yml    # Multi-container setup
└── Dockerfile            # Container image
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                       │
│              (Streamlit / CLI / REST API)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Team Orchestration                        │
│         ┌──────────────────────────────────┐                │
│         │   DataAnalyzer Team (GroupChat)  │                │
│         └──────────────────────────────────┘                │
└──────────┬────────────┬────────────┬───────────┬────────────┘
           │            │            │           │
           ▼            ▼            ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │   Data   │ │   Code   │ │  Visual  │ │Statistics│
    │ Analyzer │ │ Executor │ │  Agent   │ │  Agent   │
    │  Agent   │ │  Agent   │ │          │ │          │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘
           │            │            │           │
           └────────────┴────────────┴───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │   Docker Executor     │
           │  (Isolated Runtime)   │
           └───────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │   OpenAI GPT-4o       │
           │   (Language Model)    │
           └───────────────────────┘
```

## Technology Stack

- **Framework**: [AutoGen 0.7.5](https://github.com/microsoft/autogen) - Multi-agent orchestration
- **LLM**: OpenAI GPT-4o
- **Execution**: Docker - Isolated code runtime
- **Web UI**: Streamlit 1.41.1
- **API**: FastAPI + Uvicorn
- **Data**: Pandas 2.2.3, NumPy 2.2.1
- **Visualization**: Matplotlib 3.10.0, Seaborn 0.13.2, Plotly
- **Testing**: Pytest 8.0+

## Usage Examples

### CLI Examples
```bash
# Interactive mode
python main.py --interactive

# Single task
python main.py --task "Show correlation between age and salary" --file data/sales.csv

# Help
python main.py --help
```

### REST API Examples
```bash
# Upload file
curl -X POST http://localhost:8000/upload -F "file=@data.csv"

# Start analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"task":"Calculate mean of all numeric columns"}'

# Check job status
curl http://localhost:8000/jobs/{job_id}

# Get metrics
curl http://localhost:8000/metrics
```

### Web Interface
1. Launch: `streamlit run streamlit_app.py`
2. Upload CSV/Excel file
3. Enter natural language query
4. View results and download visualizations

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_agents.py -v
pytest tests/test_team.py -v
pytest tests/test_utils.py -v
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Docker Deployment

```bash
# Build image
docker build -t datawise-ai .

# Run with Docker Compose
docker-compose up -d

# Access services:
# - Streamlit: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Configuration

Key environment variables in `.env`:

```bash
OPENAI_API_KEY=sk-...           # Required
MODEL_NAME=gpt-4o               # Model to use
MAX_ROUNDS=15                   # Max conversation rounds
ENABLE_CACHE=true               # Cache analysis results
TRACK_COSTS=true                # Track API costs
DAILY_COST_THRESHOLD=10.0       # Cost alert threshold
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen) for the multi-agent framework
- OpenAI for GPT models
- Open source community