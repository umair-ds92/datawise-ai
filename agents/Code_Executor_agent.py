"""
Code Executor Agent
Executes Python and Bash code in isolated Docker environment
"""

from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor


def create_code_executor_agent(code_executor):
    """
    Create a Code Executor agent for running code safely
    
    Args:
        code_executor: Docker code executor instance
        
    Returns:
        CodeExecutorAgent: Configured code executor agent
    """
    code_executor_agent = CodeExecutorAgent(
        name='Code_Executor',
        description='Executes Python and Bash code in isolated Docker containers',
        code_executor=code_executor
    )
    
    return code_executor_agent


# Alias for backward compatibility
getCodeExecutorAgent = create_code_executor_agent


if __name__ == "__main__":
    """Test the agent with simple code execution"""
    import asyncio
    from autogen_agentchat.messages import TextMessage
    from autogen_core import CancellationToken
    from config.docker_utils import getDockerCommandLineExecutor
    
    async def test_agent():
        print("🧪 Testing Code Executor Agent...")
        
        docker = getDockerCommandLineExecutor()
        agent = create_code_executor_agent(docker)
        
        test_code = TextMessage(
            content='''Here is the Python code to execute:
```python
import sys
print("✅ Python version:", sys.version)
print("✅ Code execution successful!")
```''',
            source='User'
        )
        
        try:
            await docker.start()
            print("🐳 Docker container started")
            
            result = await agent.on_messages(
                messages=[test_code],
                cancellation_token=CancellationToken()
            )
            
            print("📊 Result:", result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await docker.stop()
            print("🛑 Docker container stopped")
    
    asyncio.run(test_agent())