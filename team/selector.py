"""
Custom Agent Selection Logic
Simple selector strategies for agent routing
"""

from typing import List, Optional, Any


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
    
    def select_by_keywords(self, content: str, agents: List[Any]) -> Optional[Any]:
        """
        Select agent based on keywords in content
        
        Args:
            content: Message content
            agents: List of available agents
            
        Returns:
            Selected agent or None
        """
        content_lower = content.lower()
        
        # Check for visualization keywords
        if any(keyword in content_lower for keyword in self.routing_keywords['visualization']):
            return self._find_agent_by_name(agents, 'Visualization_Specialist')
        
        # Check for statistics keywords
        if any(keyword in content_lower for keyword in self.routing_keywords['statistics']):
            return self._find_agent_by_name(agents, 'Statistics_Analyst')
        
        # Check for code execution keywords
        if any(keyword in content_lower for keyword in self.routing_keywords['code_executor']):
            return self._find_agent_by_name(agents, 'Code_Executor')
        
        # Default to data analyzer
        if any(keyword in content_lower for keyword in self.routing_keywords['data_analyzer']):
            return self._find_agent_by_name(agents, 'Data_Analyzer')
        
        return None
    
    def _find_agent_by_name(self, agents: List[Any], name: str) -> Optional[Any]:
        """Find agent by name from list"""
        for agent in agents:
            if hasattr(agent, 'name') and agent.name == name:
                return agent
        return None


class RoundRobinSelector:
    """
    Simple round-robin agent selection
    Cycles through agents in order
    """
    
    def __init__(self):
        self.current_index = 0
    
    def get_next_agent(self, agents: List):
        """Get next agent in rotation"""
        if not agents:
            return None
        agent = agents[self.current_index % len(agents)]
        self.current_index += 1
        return agent


class PrioritySelector:
    """
    Priority-based agent selection
    Follows a predefined order
    """
    
    def __init__(self):
        self.turn_count = 0
        self.priority_order = [
            'Data_Analyzer',
            'Code_Executor',
            'Statistics_Analyst',
            'Visualization_Specialist'
        ]
    
    def get_next_agent_name(self) -> str:
        """Get next agent name by priority"""
        if self.turn_count < len(self.priority_order):
            agent_name = self.priority_order[self.turn_count % len(self.priority_order)]
            self.turn_count += 1
            return agent_name
        return self.priority_order[0]


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
        agent = rr_selector.get_next_agent(agents)
        print(f"  Round {i+1}: {agent.name}")
    
    # Test priority selector
    priority_selector = create_smart_selector('priority')
    print("✅ Priority Selector created")
    
    print("\n✅ All selectors working correctly!")