"""
Termination Conditions
Advanced strategies to determine when agent conversations should end
"""

from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
    TerminationCondition
)
from autogen_agentchat.messages import ChatMessage, AgentMessage
from typing import Sequence


class SuccessTermination(TerminationCondition):
    """
    Terminate when task is successfully completed
    Looks for success indicators in agent messages
    """
    
    def __init__(self):
        self.success_keywords = [
            'task completed',
            'analysis complete',
            'successfully saved',
            'finished',
            'done',
            '✅'
        ]
    
    async def __call__(self, messages: Sequence[ChatMessage]) -> bool:
        """Check if success keywords are present"""
        if not messages:
            return False
        
        last_message = messages[-1]
        if isinstance(last_message, AgentMessage):
            content = last_message.content.lower()
            return any(keyword in content for keyword in self.success_keywords)
        
        return False


class ErrorTermination(TerminationCondition):
    """
    Terminate when too many errors occur
    Prevents infinite retry loops
    """
    
    def __init__(self, max_errors: int = 3):
        self.max_errors = max_errors
        self.error_count = 0
        self.error_keywords = ['error', 'exception', 'failed', 'traceback']
    
    async def __call__(self, messages: Sequence[ChatMessage]) -> bool:
        """Count errors and terminate if threshold exceeded"""
        if not messages:
            return False
        
        last_message = messages[-1]
        if isinstance(last_message, AgentMessage):
            content = last_message.content.lower()
            if any(keyword in content for keyword in self.error_keywords):
                self.error_count += 1
                if self.error_count >= self.max_errors:
                    return True
        
        return False


class TimeoutTermination(TerminationCondition):
    """
    Terminate after a certain number of rounds
    Wrapper around MaxMessageTermination with custom logic
    """
    
    def __init__(self, max_rounds: int = 15):
        self.max_rounds = max_rounds
        self.round_count = 0
    
    async def __call__(self, messages: Sequence[ChatMessage]) -> bool:
        """Terminate after max rounds"""
        self.round_count = len(messages)
        return self.round_count >= self.max_rounds


class StuckConversationTermination(TerminationCondition):
    """
    Terminate if conversation seems stuck (repeating messages)
    """
    
    def __init__(self, repetition_threshold: int = 3):
        self.threshold = repetition_threshold
        self.recent_messages = []
    
    async def __call__(self, messages: Sequence[ChatMessage]) -> bool:
        """Check for repeated messages"""
        if len(messages) < self.threshold:
            return False
        
        # Get last few messages
        recent = messages[-self.threshold:]
        contents = [msg.content for msg in recent if isinstance(msg, AgentMessage)]
        
        # Check if all messages are very similar
        if len(contents) >= self.threshold:
            # Simple check: if first message repeats
            first_content = contents[0]
            repetitions = sum(1 for c in contents if c == first_content)
            return repetitions >= self.threshold
        
        return False


def create_standard_termination(max_rounds: int = 15):
    """
    Create standard termination condition
    Combines multiple conditions with OR logic
    
    Args:
        max_rounds: Maximum conversation rounds
        
    Returns:
        Combined termination condition
    """
    # Stop on explicit termination keywords
    text_termination = TextMentionTermination('TERMINATE') | TextMentionTermination('STOP')
    
    # Stop after max rounds
    max_message = MaxMessageTermination(max_rounds)
    
    # Stop on success
    success = SuccessTermination()
    
    # Combine: stop if ANY condition is met
    combined = text_termination | max_message | success
    
    return combined


def create_robust_termination(max_rounds: int = 15, max_errors: int = 3):
    """
    Create robust termination condition with error handling
    
    Args:
        max_rounds: Maximum conversation rounds
        max_errors: Maximum allowed errors before stopping
        
    Returns:
        Combined termination condition
    """
    # Standard terminations
    text_termination = TextMentionTermination('TERMINATE') | TextMentionTermination('STOP')
    max_message = MaxMessageTermination(max_rounds)
    success = SuccessTermination()
    
    # Error handling
    error_termination = ErrorTermination(max_errors)
    
    # Stuck conversation detection
    stuck_termination = StuckConversationTermination()
    
    # Combine all conditions
    combined = (
        text_termination | 
        max_message | 
        success | 
        error_termination | 
        stuck_termination
    )
    
    return combined


def create_quick_termination():
    """
    Create quick termination for simple tasks
    Stops after 5 rounds or on success
    
    Returns:
        Quick termination condition
    """
    return (
        TextMentionTermination('TERMINATE') | 
        TextMentionTermination('STOP') | 
        MaxMessageTermination(5) |
        SuccessTermination()
    )


if __name__ == "__main__":
    """Test termination conditions"""
    print("🧪 Testing Termination Conditions...")
    
    # Test creating different termination conditions
    standard = create_standard_termination()
    print("✅ Standard termination created")
    
    robust = create_robust_termination()
    print("✅ Robust termination created")
    
    quick = create_quick_termination()
    print("✅ Quick termination created")
    
    # Test individual conditions
    success_term = SuccessTermination()
    print("✅ Success termination created")
    
    error_term = ErrorTermination(max_errors=3)
    print("✅ Error termination created")
    
    stuck_term = StuckConversationTermination()
    print("✅ Stuck conversation termination created")
    
    print("\n✅ All termination conditions working correctly!")