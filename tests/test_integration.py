"""
Integration Tests for DataWise AI
Tests that verify the full pipeline works end-to-end
"""

import pytest
import asyncio
import os
from pathlib import Path


class TestEnvironment:
    """Verify the environment is correctly set up"""

    def test_env_file_exists(self):
        """Check .env file exists"""
        assert Path('.env').exists(), ".env file not found"

    def test_required_directories_exist(self):
        """Check all required directories are created"""
        required = ['temp', 'logs', 'cache', 'state', 'utils', 'agents', 'team', 'config']
        for directory in required:
            assert Path(directory).exists(), f"Directory '{directory}' not found"

    def test_api_key_is_set(self):
        """Check OpenAI API key is configured"""
        from config.constants import OPENAI_API_KEY
        assert OPENAI_API_KEY is not None
        assert OPENAI_API_KEY != 'your_openai_api_key_here', \
            "Please set a real API key in .env"

    def test_all_imports_work(self):
        """Verify all modules can be imported"""
        from config.constants import MODEL_NAME
        from config.openai_model_client import get_model_client
        from config.docker_utils import getDockerCommandLineExecutor
        from agents import create_data_analyzer_agent, create_code_executor_agent
        from team import create_basic_team
        from utils import validate_file, validate_task, state_manager, cache_manager
        assert True


class TestAgentPipeline:
    """Test that agents can be created and connected"""

    def test_model_client_creation(self):
        """Test OpenAI model client can be created"""
        from config.openai_model_client import get_model_client
        client = get_model_client()
        assert client is not None

    def test_docker_executor_creation(self):
        """Test Docker executor can be created"""
        from config.docker_utils import getDockerCommandLineExecutor
        docker = getDockerCommandLineExecutor()
        assert docker is not None

    def test_full_team_creation(self):
        """Test full team can be assembled"""
        from config.openai_model_client import get_model_client
        from config.docker_utils import getDockerCommandLineExecutor
        from team import create_basic_team

        client = get_model_client()
        docker = getDockerCommandLineExecutor()
        team = create_basic_team(docker, client)

        assert team is not None
        assert len(team._participants) == 2


class TestUtilityPipeline:
    """Test utilities work together"""

    def test_file_validation_and_handling(self):
        """Test file can be validated"""
        from utils.validators import validate_file

        content = b"name,age,salary\nAlice,30,50000\nBob,25,45000"
        is_valid, msg = validate_file('test.csv', len(content))
        assert is_valid, f"Validation failed: {msg}"

    def test_state_save_and_restore(self, tmp_path):
        """Test session state can be saved and restored"""
        from utils.state_manager import StateManager

        manager = StateManager(str(tmp_path))
        test_state = {'messages': ['Hello'], 'turn': 1}

        manager.save_state('integration_test', test_state)
        restored = manager.load_state('integration_test')

        assert restored == test_state

    def test_metrics_full_cycle(self):
        """Test metrics tracking full cycle"""
        from utils.metrics import MetricsTracker
        import time

        tracker = MetricsTracker()
        tracker.start_task("Integration test task")
        time.sleep(0.05)
        tracker.end_task(
            input_tokens=500,
            output_tokens=200,
            model='gpt-4o',
            status='success'
        )

        summary = tracker.get_session_summary()
        assert summary['tasks_completed'] == 1
        assert summary['total_tokens'] == 700
        assert summary['total_cost_usd'] > 0

    def test_cache_full_cycle(self, tmp_path, monkeypatch):
        """Test cache set, get, and invalidate"""
        monkeypatch.setattr('utils.cache.ENABLE_CACHE', True)
        monkeypatch.setattr('utils.cache.CACHE_DIR', str(tmp_path))

        from utils.cache import CacheManager
        cache = CacheManager()

        task = "Analyze my sales data"
        filename = "sales.csv"
        result = {"summary": "Sales up 20%", "charts": ["output.png"]}

        cache.set(task, filename, result)
        retrieved = cache.get(task, filename)
        assert retrieved == result

        cache.invalidate(task, filename)
        assert cache.get(task, filename) is None


class TestAPIEndpoints:
    """Test FastAPI endpoints (without running server)"""

    def test_api_can_be_imported(self):
        """Test API module imports without errors"""
        try:
            from api.endpoints import app
            assert app is not None
            assert app.title == "DataWise AI API"
        except ImportError:
            pytest.skip("FastAPI not installed")

    def test_api_routes_exist(self):
        """Test that expected routes are registered"""
        try:
            from api.endpoints import app
            routes = [route.path for route in app.routes]
            assert "/" in routes
            assert "/health" in routes
            assert "/upload" in routes
            assert "/analyze" in routes
        except ImportError:
            pytest.skip("FastAPI not installed")


if __name__ == "__main__":
    print("🧪 Running Integration Tests...")

    try:
        test_env = TestEnvironment()
        test_env.test_all_imports_work()
        print("✅ All imports work")

        test_env.test_required_directories_exist()
        print("✅ All directories exist")

        test_pipeline = TestAgentPipeline()
        test_pipeline.test_model_client_creation()
        print("✅ Model client works")

        test_pipeline.test_docker_executor_creation()
        print("✅ Docker executor works")

        test_pipeline.test_full_team_creation()
        print("✅ Full team creation works")

        print("\n✅ All integration tests passed!")
        print("To run with pytest: pytest tests/test_integration.py -v")

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)