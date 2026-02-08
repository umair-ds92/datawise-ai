import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# API CONFIGURATION
# ============================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ============================================
# MODEL CONFIGURATION
# ============================================
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4000'))

# ============================================
# AGENT CONFIGURATION
# ============================================
MAX_ROUNDS = int(os.getenv('MAX_ROUNDS', '15'))
TERMINATION_MSG = os.getenv('TERMINATION_MSG', 'TERMINATE')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', '120'))

# ============================================
# DOCKER CONFIGURATION
# ============================================
DOCKER_IMAGE = os.getenv('DOCKER_IMAGE', 'python:3.11-slim')
USE_DOCKER = os.getenv('USE_DOCKER', 'true').lower() == 'true'
DOCKER_TIMEOUT = int(os.getenv('DOCKER_TIMEOUT', '300'))
DOCKER_WORK_DIR = './temp'
TIMEOUT_DOCKER=120

# Legacy naming (for backward compatibility)
TIMEOUT_DOCKER = DOCKER_TIMEOUT
WORK_DIR_DOCKER = DOCKER_WORK_DIR

# ============================================
# FILE HANDLING
# ============================================
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '100'))
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'csv,xlsx,json,parquet').split(',')
UPLOAD_DIR = os.getenv('UPLOAD_DIR', './data/uploads')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', './data/outputs')
TEMP_DIR = os.getenv('TEMP_DIR', './temp')

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/datawise.log')
VERBOSE_LOGGING = os.getenv('VERBOSE_LOGGING', 'false').lower() == 'true'

# ============================================
# STREAMLIT
# ============================================
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', '8501'))
STREAMLIT_ADDRESS = os.getenv('STREAMLIT_ADDRESS', 'localhost')

# Validate required variables
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")