"""
Data Analyzer Agent
Coordinates data analysis tasks and generates Python code for execution
"""

from autogen_agentchat.agents import AssistantAgent
from agents.prompts.DataAnalyzerAgentPrompt import DATA_ANALYZER_MSG
from config.constants import MODEL_NAME


def create_data_analyzer_agent(model_client):
    """
    Create a Data Analyzer agent for planning and code generation
    
    Args:
        model_client: OpenAI model client instance
        
    Returns:
        AssistantAgent: Configured data analyzer agent
    """
    data_analyzer_agent = AssistantAgent(
        name='Data_Analyzer',
        description='Expert data analyst that plans analysis strategies and generates Python code',
        model_client=model_client,
        system_message=DATA_ANALYZER_MSG
    )
    
    return data_analyzer_agent


# Alias for backward compatibility
getDataAnalyzerAgent = create_data_analyzer_agent


if __name__ == "__main__":
    """Test the agent creation"""
    from config.openai_model_client import get_model_client
    
    print("🧪 Testing Data Analyzer Agent Creation...")
    
    try:
        client = get_model_client()
        agent = create_data_analyzer_agent(client)
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"📝 Description: {agent.description}")
    except Exception as e:
        print(f"❌ Error: {e}")