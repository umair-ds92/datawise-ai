"""
Team Package
Multi-agent orchestration and collaboration patterns
"""

from team.analyzer_gpt import (
    create_data_analyzer_team,
    create_basic_team,
    create_visualization_team,
    create_statistics_team,
    getDataAnalyzerTeam
)

from team.selector import (
    CustomAgentSelector,
    RoundRobinSelector,
    PrioritySelector,
    create_smart_selector
)

from team.termination_conditions import (
    SuccessTermination,
    ErrorTermination,
    TimeoutTermination,
    StuckConversationTermination,
    create_standard_termination,
    create_robust_termination,
    create_quick_termination
)

from team.handoffs import (
    AgentHandoff,
    WorkflowPattern,
    HandoffContext,
    HandoffType,
    create_handoff_pattern
)

__all__ = [
    # Team creation
    'create_data_analyzer_team',
    'create_basic_team',
    'create_visualization_team',
    'create_statistics_team',
    'getDataAnalyzerTeam',
    
    # Selectors
    'CustomAgentSelector',
    'RoundRobinSelector',
    'PrioritySelector',
    'create_smart_selector',
    
    # Termination
    'SuccessTermination',
    'ErrorTermination',
    'TimeoutTermination',
    'StuckConversationTermination',
    'create_standard_termination',
    'create_robust_termination',
    'create_quick_termination',
    
    # Handoffs
    'AgentHandoff',
    'WorkflowPattern',
    'HandoffContext',
    'HandoffType',
    'create_handoff_pattern',
]