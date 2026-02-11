"""
Structured Logging Utility
Handles logging for agent conversations and system events
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from config.constants import LOG_LEVEL, LOG_FILE


def setup_logger(name: str = 'datawise') -> logging.Logger:
    """
    Setup and return a configured logger

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    # Console handler - shows logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)

    # File handler - saves logs to file
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


class AgentLogger:
    """
    Specialized logger for tracking agent conversations
    """

    def __init__(self):
        self.logger = setup_logger('agents')
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    def log_task_start(self, task: str):
        """Log when a new analysis task starts"""
        self.logger.info(f"[Session: {self.session_id}] Task started: {task[:100]}...")

    def log_agent_message(self, agent_name: str, message: str):
        """Log an agent's message"""
        self.logger.debug(f"[{agent_name}]: {message[:200]}...")

    def log_task_complete(self, task: str, duration: float):
        """Log when a task completes"""
        self.logger.info(
            f"[Session: {self.session_id}] Task completed in {duration:.2f}s"
        )

    def log_error(self, error: Exception, context: str = ''):
        """Log an error with context"""
        self.logger.error(f"Error in {context}: {str(error)}", exc_info=True)

    def log_docker_event(self, event: str):
        """Log Docker container events"""
        self.logger.info(f"[Docker] {event}")

    def log_file_event(self, event: str, filename: str):
        """Log file upload/download events"""
        self.logger.info(f"[File] {event}: {filename}")


# Global logger instance
agent_logger = AgentLogger()


if __name__ == "__main__":
    print("🧪 Testing Logger...")

    logger = setup_logger('test')
    logger.info("✅ Info message works")
    logger.debug("✅ Debug message works")
    logger.warning("✅ Warning message works")

    agent_log = AgentLogger()
    agent_log.log_task_start("Analyze sales data")
    agent_log.log_agent_message("Data_Analyzer", "I will analyze the data")
    agent_log.log_docker_event("Container started")
    agent_log.log_file_event("Uploaded", "data.csv")
    agent_log.log_task_complete("Analyze sales data", 12.5)

    print("✅ Logger working correctly!")
    print(f"📄 Log file: {LOG_FILE}")