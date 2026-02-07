"""
Visualization Agent
Specialized agent for creating data visualizations and charts
"""

from autogen_agentchat.agents import AssistantAgent
from agents.prompts.Visualizationagentprompt import VISUALIZATION_MSG


def create_visualization_agent(model_client):
    """
    Create a Visualization agent for chart generation
    
    Args:
        model_client: OpenAI model client instance
        
    Returns:
        AssistantAgent: Configured visualization agent
    """
    visualization_agent = AssistantAgent(
        name='Visualization_Specialist',
        description='Expert in creating publication-quality charts and visualizations using matplotlib, seaborn, and plotly',
        model_client=model_client,
        system_message=VISUALIZATION_MSG
    )
    
    return visualization_agent


# Alias for consistency
getVisualizationAgent = create_visualization_agent


if __name__ == "__main__":
    """Test the agent creation"""
    from config.openai_model_client import get_model_client
    
    print("🧪 Testing Visualization Agent Creation...")
    
    try:
        client = get_model_client()
        agent = create_visualization_agent(client)
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"📊 Description: {agent.description}")
    except Exception as e:
        print(f"❌ Error: {e}")