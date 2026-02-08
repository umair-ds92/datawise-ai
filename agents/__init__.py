"""
Agents Package
Defines all AI agents for data analysis tasks
"""

from agents.Data_Analyzer_agent import create_data_analyzer_agent, getDataAnalyzerAgent
from agents.Code_Executor_agent import create_code_executor_agent, getCodeExecutorAgent
from agents.Visualization_agent import create_visualization_agent, getVisualizationAgent
from agents.Statistics_agent import create_statistics_agent, getStatisticsAgent

__all__ = [
    'create_data_analyzer_agent',
    'create_code_executor_agent',
    'create_visualization_agent',
    'create_statistics_agent',
    'getDataAnalyzerAgent',
    'getCodeExecutorAgent',
    'getVisualizationAgent',
    'getStatisticsAgent',
]