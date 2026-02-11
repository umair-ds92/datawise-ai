"""
Input Validators
Validates user inputs before processing
"""

import os
from pathlib import Path
from typing import Tuple
from config.constants import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_file(filename: str, file_size_bytes: int) -> Tuple[bool, str]:
    """
    Validate an uploaded file

    Args:
        filename: Name of the file
        file_size_bytes: File size in bytes

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check filename
    if not filename or filename.strip() == '':
        return False, "Filename cannot be empty"

    # Check extension
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File type '.{ext}' not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"

    # Check file size
    size_mb = file_size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f}MB). Maximum: {MAX_FILE_SIZE_MB}MB"

    # Check for empty file
    if file_size_bytes == 0:
        return False, "File is empty"

    return True, ""


def validate_task(task: str) -> Tuple[bool, str]:
    """
    Validate a user task/query

    Args:
        task: User's task description

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not task or task.strip() == '':
        return False, "Task cannot be empty"

    if len(task.strip()) < 10:
        return False, "Task is too short. Please provide more detail"

    if len(task) > 2000:
        return False, "Task is too long. Please keep it under 2000 characters"

    return True, ""


def validate_csv_content(content: str) -> Tuple[bool, str]:
    """
    Basic validation of CSV content

    Args:
        content: CSV file content as string

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not content or content.strip() == '':
        return False, "CSV file is empty"

    lines = content.strip().split('\n')

    if len(lines) < 2:
        return False, "CSV must have at least a header row and one data row"

    # Check header row
    header = lines[0]
    if not header.strip():
        return False, "CSV header row is empty"

    # Check consistent columns
    num_cols = len(header.split(','))
    if num_cols < 1:
        return False, "CSV must have at least one column"

    return True, ""


def validate_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Validate OpenAI API key format

    Args:
        api_key: API key to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not api_key or api_key.strip() == '':
        return False, "API key cannot be empty"

    if not api_key.startswith('sk-'):
        return False, "Invalid API key format. Should start with 'sk-'"

    if len(api_key) < 40:
        return False, "API key appears too short"

    return True, ""


def validate_environment() -> Tuple[bool, list]:
    """
    Validate that all required environment variables are set

    Returns:
        Tuple[bool, list]: (is_valid, list_of_missing_vars)
    """
    required_vars = ['OPENAI_API_KEY']
    missing = []

    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    return len(missing) == 0, missing


if __name__ == "__main__":
    print("🧪 Testing Validators...")

    # Test file validation
    valid, msg = validate_file('data.csv', 1024 * 500)  # 500KB
    print(f"✅ Valid CSV file: {valid}")

    valid, msg = validate_file('data.exe', 1024)
    print(f"✅ Invalid extension caught: {not valid} | {msg}")

    valid, msg = validate_file('data.csv', 1024 * 1024 * 200)  # 200MB
    print(f"✅ Oversized file caught: {not valid} | {msg}")

    # Test task validation
    valid, msg = validate_task("Analyze the sales trends in my data")
    print(f"✅ Valid task: {valid}")

    valid, msg = validate_task("")
    print(f"✅ Empty task caught: {not valid} | {msg}")

    # Test environment validation
    valid, missing = validate_environment()
    print(f"✅ Environment check: {valid} | Missing: {missing}")

    print("\n✅ Validators working correctly!")