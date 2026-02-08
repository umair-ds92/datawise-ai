"""
Minimal Test Suite for DataWise AI
Simple and professional testing approach
"""

import pytest
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineExecutor
from agents import (
    create_data_analyzer_agent,
    create_code_executor_agent,
    create_visualization_agent,
    create_statistics_agent
)


class TestAgents:
    """Basic tests to ensure agents work"""
    
    def test_all_agents_can_be_created(self):
        """Test that all agents can be instantiated without errors"""
        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        # Try creating each agent
        agents = [
            create_data_analyzer_agent(model_client),
            create_visualization_agent(model_client),
            create_statistics_agent(model_client),
            create_code_executor_agent(docker),
        ]
        
        # Basic checks
        assert len(agents) == 4
        for agent in agents:
            assert agent is not None
            assert hasattr(agent, 'name')
    
    def test_agent_names_are_unique(self):
        """Test that all agents have unique names"""
        model_client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        agents = [
            create_data_analyzer_agent(model_client),
            create_visualization_agent(model_client),
            create_statistics_agent(model_client),
            create_code_executor_agent(docker),
        ]
        
        names = [agent.name for agent in agents]
        assert len(names) == len(set(names)), "Agent names must be unique"


if __name__ == "__main__":
    """Run tests directly without pytest"""
    print("🧪 Testing DataWise AI Agents...")
    
    try:
        test = TestAgents()
        test.test_all_agents_can_be_created()
        print("✅ All agents created successfully!")
        print("\nTo run with pytest: pytest tests/test_agents.py -v")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)