"""
OpenAI Model Client Configuration
Provides configured OpenAI client for agent communication
"""

from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import OPENAI_API_KEY, MODEL_NAME

def get_model_client():
    """
    Create and return configured OpenAI client
    
    Returns:
        OpenAIChatCompletionClient: Configured OpenAI client instance
        
    Raises:
        ValueError: If API key is not set
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your .env file."
        )
    
    openai_model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=OPENAI_API_KEY
    )
    
    return openai_model_client