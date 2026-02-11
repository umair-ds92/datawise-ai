"""
Error Handlers
Graceful error handling and retry logic for agent operations
"""

import asyncio
import functools
from typing import Callable, Any
from utils.logging import agent_logger


class DataWiseError(Exception):
    """Base exception for DataWise AI errors"""
    pass


class DockerError(DataWiseError):
    """Raised when Docker operations fail"""
    pass


class AgentError(DataWiseError):
    """Raised when agent operations fail"""
    pass


class FileError(DataWiseError):
    """Raised when file operations fail"""
    pass


class APIError(DataWiseError):
    """Raised when API calls fail"""
    pass


def handle_errors(default_return=None, log_errors: bool = True):
    """
    Decorator for graceful error handling in regular functions

    Args:
        default_return: Value to return on error
        log_errors: Whether to log errors

    Usage:
        @handle_errors(default_return=None)
        def my_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    agent_logger.log_error(e, context=func.__name__)
                return default_return
        return wrapper
    return decorator


def handle_async_errors(default_return=None, log_errors: bool = True):
    """
    Decorator for graceful error handling in async functions

    Args:
        default_return: Value to return on error
        log_errors: Whether to log errors

    Usage:
        @handle_async_errors(default_return=None)
        async def my_async_function():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    agent_logger.log_error(e, context=func.__name__)
                return default_return
        return wrapper
    return decorator


async def retry_async(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    *args,
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff

    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (doubles each time)
        *args, **kwargs: Arguments to pass to the function

    Returns:
        Result of the function, or raises the last exception
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)

        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                agent_logger.logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                await asyncio.sleep(wait_time)

    agent_logger.log_error(last_exception, context=f"retry_async({func.__name__})")
    raise last_exception


def format_error_for_user(error: Exception) -> str:
    """
    Format an error message to be user-friendly

    Args:
        error: Exception to format

    Returns:
        str: User-friendly error message
    """
    error_messages = {
        'ConnectionError': "Network connection failed. Please check your internet connection.",
        'TimeoutError': "The operation timed out. Please try again.",
        'PermissionError': "Permission denied. Please check your file permissions.",
        'FileNotFoundError': "File not found. Please check the file path.",
        'DockerError': "Docker container issue. Please ensure Docker is running.",
        'APIError': "API call failed. Please check your API key.",
        'ValueError': f"Invalid input: {str(error)}",
    }

    error_type = type(error).__name__
    return error_messages.get(
        error_type,
        f"An unexpected error occurred: {str(error)}"
    )


if __name__ == "__main__":
    print("🧪 Testing Error Handlers...")

    # Test handle_errors decorator
    @handle_errors(default_return="default")
    def risky_function():
        raise ValueError("Test error")

    result = risky_function()
    print(f"✅ handle_errors works: returned '{result}'")

    # Test handle_async_errors decorator
    @handle_async_errors(default_return="async_default")
    async def risky_async():
        raise RuntimeError("Async test error")

    result = asyncio.run(risky_async())
    print(f"✅ handle_async_errors works: returned '{result}'")

    # Test format_error_for_user
    error = ConnectionError("Network failed")
    msg = format_error_for_user(error)
    print(f"✅ Error formatting: {msg}")

    # Test custom exceptions
    try:
        raise DockerError("Docker not running")
    except DataWiseError as e:
        print(f"✅ Custom exceptions work: {e}")

    print("\n✅ Error Handlers working correctly!")