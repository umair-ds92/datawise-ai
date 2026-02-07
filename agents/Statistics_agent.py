"""
Statistics Agent
Specialized agent for statistical analysis and hypothesis testing
"""

from autogen_agentchat.agents import AssistantAgent
from agents.prompts.Statisticsagentprompt import STATISTICS_MSG


def create_statistics_agent(model_client):
    """
    Create a Statistics agent for numerical analysis
    
    Args:
        model_client: OpenAI model client instance
        
    Returns:
        AssistantAgent: Configured statistics agent
    """
    statistics_agent = AssistantAgent(
        name='Statistics_Analyst',
        description='Expert statistician specialized in descriptive stats, hypothesis testing, and statistical modeling',
        model_client=model_client,
        system_message=STATISTICS_MSG
    )
    
    return statistics_agent


# Alias for consistency
getStatisticsAgent = create_statistics_agent


if __name__ == "__main__":
    """Test the agent creation"""
    from config.openai_model_client import get_model_client
    
    print("🧪 Testing Statistics Agent Creation...")
    
    try:
        client = get_model_client()
        agent = create_statistics_agent(client)
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"📈 Description: {agent.description}")
    except Exception as e:
        print(f"❌ Error: {e}")