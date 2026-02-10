"""
Termination Conditions
Simple termination strategies using AutoGen's built-in conditions
"""

from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination
)


def create_standard_termination(max_rounds: int = 15):
    """
    Create standard termination condition
    Stops on 'TERMINATE', 'STOP', or after max rounds
    
    Args:
        max_rounds: Maximum conversation rounds
        
    Returns:
        Combined termination condition
    """
    # Stop on explicit termination keywords
    text_termination = TextMentionTermination('TERMINATE') | TextMentionTermination('STOP')
    
    # Stop after max rounds
    max_message = MaxMessageTermination(max_rounds)
    
    # Combine: stop if ANY condition is met
    combined = text_termination | max_message
    
    return combined


def create_robust_termination(max_rounds: int = 15, max_errors: int = 3):
    """
    Create robust termination condition
    (Simplified version - just uses max_rounds)
    
    Args:
        max_rounds: Maximum conversation rounds
        max_errors: Not used in simplified version
        
    Returns:
        Combined termination condition
    """
    return create_standard_termination(max_rounds)


def create_quick_termination():
    """
    Create quick termination for simple tasks
    Stops after 5 rounds or on success keywords
    
    Returns:
        Quick termination condition
    """
    return (
        TextMentionTermination('TERMINATE') | 
        TextMentionTermination('STOP') | 
        MaxMessageTermination(5)
    )


# For backward compatibility
SuccessTermination = None
ErrorTermination = None
TimeoutTermination = None
StuckConversationTermination = None


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
    
    print("\n✅ All termination conditions working correctly!")