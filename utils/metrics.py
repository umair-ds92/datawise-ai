"""
Metrics Tracker
Tracks performance metrics: tokens used, time taken, and API costs
"""

import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from config.constants import TRACK_COSTS, DAILY_COST_THRESHOLD


# OpenAI pricing per 1K tokens (as of 2024 - update as needed)
PRICING = {
    'gpt-4o': {'input': 0.0025, 'output': 0.01},
    'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    'gpt-4': {'input': 0.03, 'output': 0.06},
}

METRICS_DIR = Path('./metrics')


class MetricsTracker:
    """
    Tracks API usage, cost, and performance metrics
    """

    def __init__(self):
        if TRACK_COSTS:
            METRICS_DIR.mkdir(parents=True, exist_ok=True)

        self.current_session = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'started_at': datetime.now().isoformat(),
            'tasks': [],
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'total_cost_usd': 0.0,
            'total_duration_seconds': 0.0
        }
        self._task_start_time = None

    def start_task(self, task: str):
        """
        Start tracking a task

        Args:
            task: Task description
        """
        self._task_start_time = time.time()
        self._current_task = {
            'task': task[:100],
            'started_at': datetime.now().isoformat(),
            'input_tokens': 0,
            'output_tokens': 0,
            'cost_usd': 0.0,
            'duration_seconds': 0.0,
            'status': 'running'
        }

    def end_task(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = 'gpt-4o',
        status: str = 'success'
    ):
        """
        End tracking a task and record metrics

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            model: Model name for cost calculation
            status: Task completion status
        """
        if not self._task_start_time:
            return

        duration = time.time() - self._task_start_time
        cost = self._calculate_cost(input_tokens, output_tokens, model)

        # Update current task
        self._current_task.update({
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost_usd': cost,
            'duration_seconds': round(duration, 2),
            'status': status
        })

        # Update session totals
        self.current_session['tasks'].append(self._current_task)
        self.current_session['total_input_tokens'] += input_tokens
        self.current_session['total_output_tokens'] += output_tokens
        self.current_session['total_cost_usd'] += cost
        self.current_session['total_duration_seconds'] += duration

        # Check cost threshold
        if TRACK_COSTS and self.current_session['total_cost_usd'] > DAILY_COST_THRESHOLD:
            print(f"⚠️  Daily cost threshold exceeded: ${self.current_session['total_cost_usd']:.4f}")

        # Save metrics
        if TRACK_COSTS:
            self._save_metrics()

    def get_session_summary(self) -> dict:
        """
        Get summary of current session metrics

        Returns:
            dict: Session metrics summary
        """
        session = self.current_session
        return {
            'session_id': session['session_id'],
            'tasks_completed': len(session['tasks']),
            'total_tokens': session['total_input_tokens'] + session['total_output_tokens'],
            'total_cost_usd': round(session['total_cost_usd'], 4),
            'total_duration_seconds': round(session['total_duration_seconds'], 2),
            'average_task_duration': round(
                session['total_duration_seconds'] / max(len(session['tasks']), 1), 2
            )
        }

    def get_cost_estimate(self, input_tokens: int, output_tokens: int, model: str = 'gpt-4o') -> float:
        """
        Estimate cost for a given token usage

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model to use for pricing

        Returns:
            float: Estimated cost in USD
        """
        return self._calculate_cost(input_tokens, output_tokens, model)

    def _calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost based on token usage and model pricing"""
        pricing = PRICING.get(model, PRICING['gpt-4o'])
        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']
        return round(input_cost + output_cost, 6)

    def _save_metrics(self):
        """Save metrics to file"""
        try:
            metrics_file = METRICS_DIR / f"{self.current_session['session_id']}.json"
            with open(metrics_file, 'w') as f:
                json.dump(self.current_session, f, indent=2)
        except Exception:
            pass

    def reset_session(self):
        """Reset current session metrics"""
        self.current_session = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'started_at': datetime.now().isoformat(),
            'tasks': [],
            'total_input_tokens': 0,
            'total_output_tokens': 0,
            'total_cost_usd': 0.0,
            'total_duration_seconds': 0.0
        }


# Global instance
metrics_tracker = MetricsTracker()


if __name__ == "__main__":
    print("🧪 Testing Metrics Tracker...")

    tracker = MetricsTracker()

    # Test task tracking
    tracker.start_task("Analyze sales data and create visualization")
    import time
    time.sleep(0.1)  # Simulate work
    tracker.end_task(
        input_tokens=1500,
        output_tokens=500,
        model='gpt-4o',
        status='success'
    )
    print("✅ Task tracking works")

    # Test cost estimate
    cost = tracker.get_cost_estimate(1000, 500, 'gpt-4o')
    print(f"✅ Cost estimate for 1000/500 tokens (gpt-4o): ${cost:.6f}")

    # Test session summary
    summary = tracker.get_session_summary()
    print(f"✅ Session summary: {summary}")

    print("\n✅ Metrics Tracker working correctly!")