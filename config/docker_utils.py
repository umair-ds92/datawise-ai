"""
Docker Utilities for Code Execution
Manages Docker container lifecycle for isolated code execution
"""

from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import DOCKER_TIMEOUT, DOCKER_WORK_DIR, DOCKER_IMAGE

def getDockerCommandLineExecutor():
    """
    Create Docker executor for code execution
    
    Returns:
        DockerCommandLineCodeExecutor: Configured Docker executor
    """
    docker = DockerCommandLineCodeExecutor(
        image=DOCKER_IMAGE,
        work_dir=DOCKER_WORK_DIR,
        timeout=DOCKER_TIMEOUT
    )
    
    return docker


async def start_docker_container(docker):
    """
    Start the Docker container
    
    Args:
        docker: DockerCommandLineCodeExecutor instance
    """
    print("Starting Docker container...")
    await docker.start()
    print("Docker container started successfully")


async def stop_docker_container(docker):
    """
    Stop and cleanup the Docker container
    
    Args:
        docker: DockerCommandLineCodeExecutor instance
    """
    print("Stopping Docker container...")
    await docker.stop()
    print("Docker container stopped successfully")