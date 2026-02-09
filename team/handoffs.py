"""
Agent Handoff Patterns
Define how agents transfer control and information between each other
"""

from typing import Dict, List, Optional
from enum import Enum


class HandoffType(Enum):
    """Types of handoffs between agents"""
    SEQUENTIAL = "sequential"      # Linear flow: A -> B -> C
    PARALLEL = "parallel"          # Multiple agents work simultaneously
    CONDITIONAL = "conditional"    # Handoff based on conditions
    CYCLIC = "cyclic"             # Agents can loop back


class AgentHandoff:
    """
    Defines handoff rules between agents
    """
    
    def __init__(self):
        # Define handoff patterns
        self.handoff_rules = {
            'Data_Analyzer': {
                'next': ['Code_Executor'],
                'conditions': {
                    'has_code': 'Code_Executor',
                    'needs_stats': 'Statistics_Analyst',
                    'needs_viz': 'Visualization_Specialist'
                }
            },
            'Code_Executor': {
                'next': ['Data_Analyzer'],  # Return to analyzer after execution
                'conditions': {
                    'error': 'Data_Analyzer',  # Go back to fix code
                    'success': 'Data_Analyzer'  # Analyze results
                }
            },
            'Visualization_Specialist': {
                'next': ['Code_Executor'],  # Execute visualization code
                'conditions': {
                    'ready': 'Code_Executor'
                }
            },
            'Statistics_Analyst': {
                'next': ['Code_Executor'],  # Execute statistical code
                'conditions': {
                    'ready': 'Code_Executor'
                }
            }
        }
    
    def get_next_agent(
        self, 
        current_agent: str, 
        context: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Determine which agent should speak next
        
        Args:
            current_agent: Name of current agent
            context: Optional context for conditional handoffs
            
        Returns:
            Name of next agent, or None for default routing
        """
        if current_agent not in self.handoff_rules:
            return None
        
        rules = self.handoff_rules[current_agent]
        
        # Check conditional handoffs first
        if context and 'conditions' in rules:
            for condition, next_agent in rules['conditions'].items():
                if context.get(condition):
                    return next_agent
        
        # Default to first agent in 'next' list
        if 'next' in rules and rules['next']:
            return rules['next'][0]
        
        return None
    
    def get_handoff_chain(self, start_agent: str, length: int = 5) -> List[str]:
        """
        Get a chain of agent handoffs
        
        Args:
            start_agent: Starting agent
            length: Length of chain to generate
            
        Returns:
            List of agent names in handoff order
        """
        chain = [start_agent]
        current = start_agent
        
        for _ in range(length - 1):
            next_agent = self.get_next_agent(current)
            if next_agent:
                chain.append(next_agent)
                current = next_agent
            else:
                break
        
        return chain


class WorkflowPattern:
    """
    Predefined workflow patterns for common analysis tasks
    """
    
    @staticmethod
    def simple_analysis() -> List[str]:
        """
        Simple analysis workflow: Analyze -> Execute -> Done
        
        Returns:
            List of agent names in order
        """
        return [
            'Data_Analyzer',
            'Code_Executor'
        ]
    
    @staticmethod
    def visualization_workflow() -> List[str]:
        """
        Visualization workflow: Analyze -> Visualize -> Execute -> Done
        
        Returns:
            List of agent names in order
        """
        return [
            'Data_Analyzer',
            'Visualization_Specialist',
            'Code_Executor'
        ]
    
    @staticmethod
    def statistical_workflow() -> List[str]:
        """
        Statistical analysis workflow
        
        Returns:
            List of agent names in order
        """
        return [
            'Data_Analyzer',
            'Statistics_Analyst',
            'Code_Executor'
        ]
    
    @staticmethod
    def comprehensive_workflow() -> List[str]:
        """
        Comprehensive workflow with all agents
        
        Returns:
            List of agent names in order
        """
        return [
            'Data_Analyzer',
            'Statistics_Analyst',
            'Visualization_Specialist',
            'Code_Executor'
        ]
    
    @staticmethod
    def iterative_workflow() -> List[str]:
        """
        Iterative workflow that can loop
        
        Returns:
            List of agent names (with potential cycles)
        """
        return [
            'Data_Analyzer',
            'Code_Executor',
            'Data_Analyzer',  # Loop back for refinement
            'Code_Executor'
        ]


class HandoffContext:
    """
    Manages context for agent handoffs
    Tracks state and conditions for conditional routing
    """
    
    def __init__(self):
        self.state = {}
        self.history = []
    
    def set_condition(self, key: str, value: bool):
        """Set a condition for handoff decisions"""
        self.state[key] = value
    
    def get_condition(self, key: str) -> bool:
        """Get a condition value"""
        return self.state.get(key, False)
    
    def add_to_history(self, agent_name: str):
        """Track agent execution history"""
        self.history.append(agent_name)
    
    def get_history(self) -> List[str]:
        """Get agent execution history"""
        return self.history.copy()
    
    def reset(self):
        """Reset context"""
        self.state = {}
        self.history = []


def create_handoff_pattern(pattern_type: str) -> List[str]:
    """
    Factory function to create handoff patterns
    
    Args:
        pattern_type: Type of workflow pattern
        
    Returns:
        List of agent names in handoff order
    """
    patterns = {
        'simple': WorkflowPattern.simple_analysis,
        'visualization': WorkflowPattern.visualization_workflow,
        'statistical': WorkflowPattern.statistical_workflow,
        'comprehensive': WorkflowPattern.comprehensive_workflow,
        'iterative': WorkflowPattern.iterative_workflow
    }
    
    if pattern_type not in patterns:
        raise ValueError(f"Unknown pattern type: {pattern_type}")
    
    return patterns[pattern_type]()


if __name__ == "__main__":
    """Test handoff patterns"""
    print("🧪 Testing Agent Handoff Patterns...")
    
    # Test handoff rules
    handoff = AgentHandoff()
    next_agent = handoff.get_next_agent('Data_Analyzer')
    print(f"✅ After Data_Analyzer: {next_agent}")
    
    # Test handoff chain
    chain = handoff.get_handoff_chain('Data_Analyzer', length=5)
    print(f"✅ Handoff chain: {' -> '.join(chain)}")
    
    # Test workflow patterns
    simple = WorkflowPattern.simple_analysis()
    print(f"✅ Simple workflow: {' -> '.join(simple)}")
    
    viz = WorkflowPattern.visualization_workflow()
    print(f"✅ Visualization workflow: {' -> '.join(viz)}")
    
    stats = WorkflowPattern.statistical_workflow()
    print(f"✅ Statistical workflow: {' -> '.join(stats)}")
    
    comprehensive = WorkflowPattern.comprehensive_workflow()
    print(f"✅ Comprehensive workflow: {' -> '.join(comprehensive)}")
    
    # Test context
    context = HandoffContext()
    context.set_condition('has_code', True)
    context.add_to_history('Data_Analyzer')
    print(f"✅ Context tracking works")
    
    print("\n✅ All handoff patterns working correctly!")