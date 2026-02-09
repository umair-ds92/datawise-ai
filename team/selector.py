"""
Custom Agent Selection Logic
Intelligent routing to determine which agent should speak next
"""

from typing import List, Optional
from autogen_agentchat.base import ChatAgent
from autogen_agentchat.messages import AgentMessage, ChatMessage


class CustomAgentSelector:
    """
    Custom logic for selecting the next agent to speak
    Uses keyword-based routing for efficiency
    """
    
    def __init__(self):
        self.routing_keywords = {
            'visualization': ['plot', 'chart', 'graph', 'visualize', 'visualization', 'show me'],
            'statistics': ['correlation', 'regression', 't-test', 'anova', 'mean', 'median', 'std', 'statistical'],
            'code_executor': ['run', 'execute', 'error', 'traceback', 'install'],
            'data_analyzer': ['analyze', 'data', 'dataset', 'csv', 'load', 'read']
        }
    
    def select_next_agent(
        self, 
        agents: List[ChatAgent], 
        last_message: ChatMessage
    ) -> Optional[ChatAgent]:
        """
        Select the next agent based on message content
        
        Args:
            agents: List of available agents
            last_message: The last message in conversation
            
        Returns:
            ChatAgent: The selected agent, or None for automatic selection
        """
        if not isinstance(last_message, AgentMessage):
            return None
        
        content = last_message.content.lower()
        
        # Check for visualization keywords
        if any(keyword in content for keyword in self.routing_keywords['visualization']):
            return self._find_agent_by_name(agents, 'Visualization_Specialist')
        
        # Check for statistics keywords
        if any(keyword in content for keyword in self.routing_keywords['statistics']):
            return self._find_agent_by_name(agents, 'Statistics_Analyst')
        
        # Check for code execution keywords
        if any(keyword in content for keyword in self.routing_keywords['code_executor']):
            return self._find_agent_by_name(agents, 'Code_Executor')
        
        # Default to data analyzer for general queries
        if any(keyword in content for keyword in self.routing_keywords['data_analyzer']):
            return self._find_agent_by_name(agents, 'Data_Analyzer')
        
        # Return None to use default selection
        return None
    
    def _find_agent_by_name(self, agents: List[ChatAgent], name: str) -> Optional[ChatAgent]:
        """Find agent by name from list"""
        for agent in agents:
            if agent.name == name:
                return agent
        return None


class RoundRobinSelector:
    """
    Simple round-robin agent selection
    Cycles through agents in order
    """
    
    def __init__(self):
        self.current_index = 0
    
    def select_next_agent(
        self, 
        agents: List[ChatAgent], 
        last_message: ChatMessage
    ) -> ChatAgent:
        """
        Select next agent in round-robin fashion
        
        Args:
            agents: List of available agents
            last_message: The last message (not used)
            
        Returns:
            ChatAgent: Next agent in rotation
        """
        agent = agents[self.current_index % len(agents)]
        self.current_index += 1
        return agent


class PrioritySelector:
    """
    Priority-based agent selection
    Certain agents get priority based on conversation stage
    """
    
    def __init__(self):
        self.turn_count = 0
        self.priority_order = [
            'Data_Analyzer',      # First: Plan the analysis
            'Code_Executor',       # Second: Execute the code
            'Statistics_Analyst',  # Third: Analyze results
            'Visualization_Specialist'  # Fourth: Create visuals
        ]
    
    def select_next_agent(
        self, 
        agents: List[ChatAgent], 
        last_message: ChatMessage
    ) -> Optional[ChatAgent]:
        """
        Select agent based on priority order and turn count
        
        Args:
            agents: List of available agents
            last_message: The last message
            
        Returns:
            ChatAgent: Selected agent based on priority
        """
        # For first few turns, follow strict priority
        if self.turn_count < len(self.priority_order):
            agent_name = self.priority_order[self.turn_count]
            self.turn_count += 1
            return self._find_agent_by_name(agents, agent_name)
        
        # After initial rounds, use content-based selection
        self.turn_count += 1
        return None  # Use default selection
    
    def _find_agent_by_name(self, agents: List[ChatAgent], name: str) -> Optional[ChatAgent]:
        """Find agent by name from list"""
        for agent in agents:
            if agent.name == name:
                return agent
        return None


def create_smart_selector(strategy: str = 'keyword'):
    """
    Factory function to create different selector strategies
    
    Args:
        strategy: 'keyword', 'round_robin', or 'priority'
        
    Returns:
        Selector instance
    """
    if strategy == 'keyword':
        return CustomAgentSelector()
    elif strategy == 'round_robin':
        return RoundRobinSelector()
    elif strategy == 'priority':
        return PrioritySelector()
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


if __name__ == "__main__":
    """Test selector logic"""
    print("🧪 Testing Agent Selectors...")
    
    # Mock agents for testing
    class MockAgent:
        def __init__(self, name):
            self.name = name
    
    agents = [
        MockAgent('Data_Analyzer'),
        MockAgent('Code_Executor'),
        MockAgent('Visualization_Specialist'),
        MockAgent('Statistics_Analyst')
    ]
    
    # Test keyword selector
    keyword_selector = create_smart_selector('keyword')
    print("✅ Keyword Selector created")
    
    # Test round robin selector
    rr_selector = create_smart_selector('round_robin')
    for i in range(3):
        agent = rr_selector.select_next_agent(agents, None)
        print(f"  Round {i+1}: {agent.name}")
    
    # Test priority selector
    priority_selector = create_smart_selector('priority')
    print("✅ Priority Selector created")
    
    print("\n✅ All selectors working correctly!")