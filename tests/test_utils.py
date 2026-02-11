"""
Tests for Utility Modules
"""

import pytest
import asyncio
from utils.validators import validate_file, validate_task, validate_csv_content, validate_environment
from utils.state_manager import StateManager
from utils.cache import CacheManager
from utils.metrics import MetricsTracker
from utils.error_handlers import (
    handle_errors, handle_async_errors,
    DataWiseError, DockerError
)
from utils.logging import setup_logger


class TestValidators:
    """Tests for input validators"""

    def test_valid_csv_file(self):
        valid, msg = validate_file('data.csv', 1024 * 100)
        assert valid is True
        assert msg == ""

    def test_invalid_extension(self):
        valid, msg = validate_file('data.exe', 1024)
        assert valid is False
        assert 'not allowed' in msg

    def test_file_too_large(self):
        valid, msg = validate_file('data.csv', 1024 * 1024 * 200)
        assert valid is False
        assert 'large' in msg.lower()

    def test_empty_filename(self):
        valid, msg = validate_file('', 1024)
        assert valid is False

    def test_valid_task(self):
        valid, msg = validate_task("Analyze the sales trends in my data")
        assert valid is True

    def test_empty_task(self):
        valid, msg = validate_task("")
        assert valid is False

    def test_short_task(self):
        valid, msg = validate_task("analyze")
        assert valid is False
        assert 'short' in msg.lower()

    def test_valid_csv_content(self):
        csv = "col1,col2\n1,2\n3,4"
        valid, msg = validate_csv_content(csv)
        assert valid is True

    def test_empty_csv(self):
        valid, msg = validate_csv_content("")
        assert valid is False

    def test_csv_no_data_rows(self):
        valid, msg = validate_csv_content("col1,col2")
        assert valid is False

    def test_environment_check(self):
        valid, missing = validate_environment()
        # Just check it returns correct types
        assert isinstance(valid, bool)
        assert isinstance(missing, list)


class TestStateManager:
    """Tests for state persistence"""

    def test_save_and_load_state(self, tmp_path):
        manager = StateManager(str(tmp_path))
        state = {'messages': ['Hello'], 'turn': 1}

        manager.save_state('test_001', state)
        loaded = manager.load_state('test_001')

        assert loaded == state

    def test_load_nonexistent_state(self, tmp_path):
        manager = StateManager(str(tmp_path))
        result = manager.load_state('nonexistent')
        assert result is None

    def test_list_sessions(self, tmp_path):
        manager = StateManager(str(tmp_path))
        manager.save_state('session_a', {'data': 1})
        manager.save_state('session_b', {'data': 2})

        sessions = manager.list_sessions()
        assert 'session_a' in sessions
        assert 'session_b' in sessions

    def test_delete_state(self, tmp_path):
        manager = StateManager(str(tmp_path))
        manager.save_state('to_delete', {'data': 1})

        deleted = manager.delete_state('to_delete')
        assert deleted is True

        loaded = manager.load_state('to_delete')
        assert loaded is None

    def test_get_latest_session(self, tmp_path):
        manager = StateManager(str(tmp_path))
        manager.save_state('session_001', {'data': 1})
        manager.save_state('session_002', {'data': 2})

        latest = manager.get_latest_session()
        assert latest == 'session_002'


class TestCacheManager:
    """Tests for caching"""

    def test_set_and_get(self, tmp_path, monkeypatch):
        monkeypatch.setattr('utils.cache.ENABLE_CACHE', True)
        monkeypatch.setattr('utils.cache.CACHE_DIR', str(tmp_path))

        cache = CacheManager()
        cache.state_dir = tmp_path

        result = {'summary': 'Test result'}
        cache.set('test task', 'data.csv', result)
        retrieved = cache.get('test task', 'data.csv')

        assert retrieved == result

    def test_cache_miss(self, tmp_path, monkeypatch):
        monkeypatch.setattr('utils.cache.ENABLE_CACHE', True)
        monkeypatch.setattr('utils.cache.CACHE_DIR', str(tmp_path))

        cache = CacheManager()
        result = cache.get('nonexistent task', 'data.csv')
        assert result is None


class TestMetricsTracker:
    """Tests for metrics tracking"""

    def test_task_tracking(self):
        tracker = MetricsTracker()
        tracker.start_task("Test analysis task")
        tracker.end_task(
            input_tokens=1000,
            output_tokens=500,
            model='gpt-4o',
            status='success'
        )

        summary = tracker.get_session_summary()
        assert summary['tasks_completed'] == 1
        assert summary['total_tokens'] == 1500

    def test_cost_estimate(self):
        tracker = MetricsTracker()
        cost = tracker.get_cost_estimate(1000, 500, 'gpt-4o')

        assert isinstance(cost, float)
        assert cost > 0

    def test_session_reset(self):
        tracker = MetricsTracker()
        tracker.start_task("Task 1")
        tracker.end_task(input_tokens=100, output_tokens=50)

        tracker.reset_session()
        summary = tracker.get_session_summary()
        assert summary['tasks_completed'] == 0


class TestErrorHandlers:
    """Tests for error handling utilities"""

    def test_handle_errors_decorator(self):
        @handle_errors(default_return="fallback")
        def risky():
            raise ValueError("Test")

        result = risky()
        assert result == "fallback"

    def test_handle_errors_success(self):
        @handle_errors(default_return=None)
        def safe():
            return "success"

        result = safe()
        assert result == "success"

    def test_handle_async_errors(self):
        @handle_async_errors(default_return="async_fallback")
        async def risky_async():
            raise RuntimeError("Async error")

        result = asyncio.run(risky_async())
        assert result == "async_fallback"

    def test_custom_exceptions(self):
        with pytest.raises(DataWiseError):
            raise DockerError("Docker not running")


class TestLogger:
    """Tests for logging utility"""

    def test_logger_creation(self):
        logger = setup_logger('test_logger')
        assert logger is not None
        assert logger.name == 'test_logger'

    def test_logger_levels(self):
        from utils.logging import AgentLogger
        agent_log = AgentLogger()

        # These should not raise
        agent_log.log_task_start("Test task")
        agent_log.log_agent_message("TestAgent", "Hello")
        agent_log.log_docker_event("Container started")
        agent_log.log_file_event("Upload", "data.csv")


if __name__ == "__main__":
    print("🧪 Testing Utilities...")

    try:
        # Quick smoke tests
        from utils.validators import validate_task
        valid, _ = validate_task("Analyze sales data in my CSV file")
        assert valid, "Validator failed"
        print("✅ Validators work")

        manager = StateManager('./test_state_temp')
        manager.save_state('test', {'key': 'value'})
        loaded = manager.load_state('test')
        assert loaded == {'key': 'value'}
        import shutil
        shutil.rmtree('./test_state_temp', ignore_errors=True)
        print("✅ State Manager works")

        tracker = MetricsTracker()
        tracker.start_task("test")
        tracker.end_task(100, 50)
        summary = tracker.get_session_summary()
        assert summary['tasks_completed'] == 1
        print("✅ Metrics Tracker works")

        logger = setup_logger('smoke_test')
        logger.info("Smoke test passed")
        print("✅ Logger works")

        print("\n✅ All utility tests passed!")
        print("To run with pytest: pytest tests/test_utils.py -v")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)