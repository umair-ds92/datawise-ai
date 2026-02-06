# DataWise AI 

> AI-powered multi-agent data analysis platform that transforms raw data into actionable insights

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.7.5-green.svg)](https://github.com/microsoft/autogen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

DataWise AI leverages AutoGen's multi-agent framework to analyze, visualize, and explain data through natural language. Simply upload your dataset and ask questions - specialized AI agents collaborate to deliver comprehensive insights automatically.

## Features

- **Natural Language Queries** - Interact with data using plain English
- **Automated Visualizations** - Generate publication-ready charts automatically
- **Statistical Analysis** - Deep insights powered by specialized agents
- **Secure Code Execution** - Isolated Docker environments for safety
- **Multi-Agent Collaboration** - Coordinated teamwork for complex analysis
- **Web & API Interfaces** - Streamlit UI and REST endpoints
- **Cost Tracking** - Monitor API usage and expenses
- **Enterprise Security** - Authentication, encryption, and audit logs

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (for code execution)
- OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/datawise-ai.git
cd datawise-ai

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run Application

```bash
# Web Interface
streamlit run streamlit_app.py

# CLI Interface
python main.py

# API Server
uvicorn api.endpoints:app --reload
```

## Project Structure

```
datawise-ai/
├── config/               # Configuration and settings
├── agents/               # AI agent definitions
├── team/                 # Multi-agent orchestration
├── utils/                # Shared utilities
├── api/                  # REST API endpoints
├── monitoring/           # Observability tools
├── tests/                # Test suite
├── data/                 # Data storage
├── main.py               # CLI entry point
├── streamlit_app.py      # Web interface
├── requirements.txt      # Dependencies
├── docker-compose.yml    # Container setup
├── Dockerfile            # Container image
├── .env.example          # Environment template
└── README.md             # Documentation
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│              (Streamlit / CLI / REST API)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Team Orchestration                         │
│         ┌──────────────────────────────────┐                │
│         │   DataAnalyzer Team (GroupChat)  │                │
│         └──────────────────────────────────┘                │
└──────────┬────────────┬────────────┬───────────┬────────────┘
           │            │            │           │
           ▼            ▼            ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │   Data   │ │   Code   │ │  Visual  │ │Statistics│
    │ Analyzer │ │ Executor │ │  Agent   │ │  Agent   │
    │  Agent   │ │  Agent   │ │          │ │          │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘
           │            │            │           │
           └────────────┴────────────┴───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │   Docker Executor     │
           │  (Isolated Runtime)   │
           └───────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │   OpenAI GPT-4        │
           │   (Language Model)    │
           └───────────────────────┘
```

### Agent Workflow

```
User Query → Data Analyzer (Plans) → Code Executor (Runs Analysis)
                ↓                           ↓
         Statistics Agent          Visualization Agent
                ↓                           ↓
         Results → Report Generator → User
```

## Technology Stack

- **Framework**: [AutoGen](https://github.com/microsoft/autogen) - Multi-agent orchestration
- **LLM**: OpenAI GPT-4 / GPT-4o
- **Execution**: Docker - Isolated code runtime
- **Web UI**: Streamlit
- **API**: FastAPI
- **Data**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Testing**: Pytest

## Usage Examples

### CLI Example
```bash
python main.py --file data.csv --query "Show correlation between age and income"
```

### Python API Example
```python
from team.analyzer_gpt import getDataAnalyzerTeam
from config.openai_model_client import get_model_client

async def analyze():
    client = get_model_client()
    team = getDataAnalyzerTeam(client)
    
    result = await team.run(
        task="Analyze sales trends by region"
    )
    print(result)
```

### Web Interface
1. Launch: `streamlit run streamlit_app.py`
2. Upload CSV/Excel file
3. Enter natural language query
4. View results and download visualizations

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_agents.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen) for the multi-agent framework
- OpenAI for GPT models
- Open source community