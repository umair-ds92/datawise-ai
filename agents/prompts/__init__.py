"""
Agent Prompts Package
System prompts for all agents
"""

from agents.prompts.DataAnalyzerAgentPrompt import DATA_ANALYZER_MSG
from agents.prompts.Visualizationagentprompt import VISUALIZATION_MSG
from agents.prompts.Statisticsagentprompt import STATISTICS_MSG

__all__ = [
    'DATA_ANALYZER_MSG',
    'VISUALIZATION_MSG',
    'STATISTICS_MSG',
]