"""
DataAnalyzer Team
Coordinates multiple agents for comprehensive data analysis
"""

from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from agents import (
    getDataAnalyzerAgent,
    getCodeExecutorAgent,
    getVisualizationAgent,
    getStatisticsAgent
)
from config.constants import MAX_ROUNDS, TERMINATION_MSG


def create_data_analyzer_team(docker, model_client, use_selector=False):
    """
    Create a team of agents for data analysis
    
    Args:
        docker: Docker code executor instance
        model_client: OpenAI model client
        use_selector: If True, use SelectorGroupChat for intelligent routing
        
    Returns:
        Team: Configured agent team
    """
    # Create agents
    data_analyzer = getDataAnalyzerAgent(model_client)
    code_executor = getCodeExecutorAgent(docker)
    visualization_agent = getVisualizationAgent(model_client)
    statistics_agent = getStatisticsAgent(model_client)
    
    # Define termination conditions
    # Stop when "TERMINATE" or "STOP" is mentioned
    termination = TextMentionTermination(TERMINATION_MSG) | TextMentionTermination('STOP')
    
    # Also stop after max rounds to prevent infinite loops
    max_message_termination = MaxMessageTermination(MAX_ROUNDS)
    
    # Combine termination conditions
    combined_termination = termination | max_message_termination
    
    if use_selector:
        # SelectorGroupChat: Model chooses which agent speaks next
        team = SelectorGroupChat(
            participants=[data_analyzer, code_executor, visualization_agent, statistics_agent],
            model_client=model_client,
            termination_condition=combined_termination
        )
    else:
        # RoundRobinGroupChat: Simple rotation between agents
        team = RoundRobinGroupChat(
            participants=[data_analyzer, code_executor],
            max_turns=MAX_ROUNDS,
            termination_condition=combined_termination
        )
    
    return team


def create_basic_team(docker, model_client):
    """
    Create a basic two-agent team (Data Analyzer + Code Executor)
    Simpler and faster for straightforward analysis tasks
    
    Args:
        docker: Docker code executor instance
        model_client: OpenAI model client
        
    Returns:
        RoundRobinGroupChat: Basic two-agent team
    """
    data_analyzer = getDataAnalyzerAgent(model_client)
    code_executor = getCodeExecutorAgent(docker)
    
    termination = TextMentionTermination('STOP') | TextMentionTermination(TERMINATION_MSG)
    
    team = RoundRobinGroupChat(
        participants=[data_analyzer, code_executor],
        max_turns=MAX_ROUNDS,
        termination_condition=termination
    )
    
    return team


def create_visualization_team(docker, model_client):
    """
    Create a team specialized in data visualization
    
    Args:
        docker: Docker code executor instance
        model_client: OpenAI model client
        
    Returns:
        RoundRobinGroupChat: Visualization-focused team
    """
    data_analyzer = getDataAnalyzerAgent(model_client)
    visualization_agent = getVisualizationAgent(model_client)
    code_executor = getCodeExecutorAgent(docker)
    
    termination = TextMentionTermination('STOP') | TextMentionTermination(TERMINATION_MSG)
    
    team = RoundRobinGroupChat(
        participants=[data_analyzer, visualization_agent, code_executor],
        max_turns=MAX_ROUNDS,
        termination_condition=termination
    )
    
    return team


def create_statistics_team(docker, model_client):
    """
    Create a team specialized in statistical analysis
    
    Args:
        docker: Docker code executor instance
        model_client: OpenAI model client
        
    Returns:
        RoundRobinGroupChat: Statistics-focused team
    """
    data_analyzer = getDataAnalyzerAgent(model_client)
    statistics_agent = getStatisticsAgent(model_client)
    code_executor = getCodeExecutorAgent(docker)
    
    termination = TextMentionTermination('STOP') | TextMentionTermination(TERMINATION_MSG)
    
    team = RoundRobinGroupChat(
        participants=[data_analyzer, statistics_agent, code_executor],
        max_turns=MAX_ROUNDS,
        termination_condition=termination
    )
    
    return team


# Backward compatibility
def getDataAnalyzerTeam(docker, model_client):
    """Legacy function - creates basic team"""
    return create_basic_team(docker, model_client)


if __name__ == "__main__":
    """Test team creation"""
    from config.openai_model_client import get_model_client
    from config.docker_utils import getDockerCommandLineExecutor
    
    print("🧪 Testing Team Creation...")
    
    try:
        client = get_model_client()
        docker = getDockerCommandLineExecutor()
        
        # Test basic team
        basic_team = create_basic_team(docker, client)
        print(f"✅ Basic Team: {len(basic_team.participants)} agents")
        
        # Test full team
        full_team = create_data_analyzer_team(docker, client)
        print(f"✅ Full Team: {len(full_team.participants)} agents")
        
        # Test visualization team
        viz_team = create_visualization_team(docker, client)
        print(f"✅ Visualization Team: {len(viz_team.participants)} agents")
        
        # Test statistics team
        stats_team = create_statistics_team(docker, client)
        print(f"✅ Statistics Team: {len(stats_team.participants)} agents")
        
        print("\n✅ All teams created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")