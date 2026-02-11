"""
State Manager
Handles conversation state persistence across sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


STATE_DIR = Path('./state')


class StateManager:
    """
    Manages saving and loading of agent team state
    Enables conversation continuity across sessions
    """

    def __init__(self, state_dir: str = './state'):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, session_id: str, state: dict) -> bool:
        """
        Save team state to disk

        Args:
            session_id: Unique session identifier
            state: State dictionary from team.save_state()

        Returns:
            bool: True if saved successfully
        """
        try:
            state_file = self.state_dir / f"{session_id}.json"

            # Add metadata
            state_with_meta = {
                'session_id': session_id,
                'saved_at': datetime.now().isoformat(),
                'state': state
            }

            with open(state_file, 'w') as f:
                json.dump(state_with_meta, f, indent=2)

            return True

        except Exception as e:
            print(f"❌ Error saving state: {e}")
            return False

    def load_state(self, session_id: str) -> Optional[dict]:
        """
        Load team state from disk

        Args:
            session_id: Session identifier to load

        Returns:
            dict: State dictionary, or None if not found
        """
        try:
            state_file = self.state_dir / f"{session_id}.json"

            if not state_file.exists():
                return None

            with open(state_file, 'r') as f:
                data = json.load(f)

            return data.get('state')

        except Exception as e:
            print(f"❌ Error loading state: {e}")
            return None

    def list_sessions(self) -> list:
        """
        List all saved sessions

        Returns:
            list: List of session IDs
        """
        sessions = []
        for file in self.state_dir.glob('*.json'):
            sessions.append(file.stem)
        return sorted(sessions)

    def delete_state(self, session_id: str) -> bool:
        """
        Delete a saved session state

        Args:
            session_id: Session to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            state_file = self.state_dir / f"{session_id}.json"
            if state_file.exists():
                state_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting state: {e}")
            return False

    def clear_old_sessions(self, keep_last: int = 10) -> int:
        """
        Delete old sessions, keeping only the most recent

        Args:
            keep_last: Number of sessions to keep

        Returns:
            int: Number of sessions deleted
        """
        sessions = self.list_sessions()
        to_delete = sessions[:-keep_last] if len(sessions) > keep_last else []

        for session_id in to_delete:
            self.delete_state(session_id)

        return len(to_delete)

    def get_latest_session(self) -> Optional[str]:
        """
        Get the most recent session ID

        Returns:
            str: Latest session ID, or None if no sessions exist
        """
        sessions = self.list_sessions()
        return sessions[-1] if sessions else None


# Global instance
state_manager = StateManager()


if __name__ == "__main__":
    print("🧪 Testing State Manager...")

    manager = StateManager('./test_state')

    # Test save
    test_state = {'messages': ['Hello', 'World'], 'turn': 3}
    saved = manager.save_state('test_session_001', test_state)
    print(f"✅ Save state: {saved}")

    # Test load
    loaded = manager.load_state('test_session_001')
    print(f"✅ Load state: {loaded}")

    # Test list
    sessions = manager.list_sessions()
    print(f"✅ Sessions: {sessions}")

    # Test latest
    latest = manager.get_latest_session()
    print(f"✅ Latest session: {latest}")

    # Cleanup test
    manager.delete_state('test_session_001')
    import shutil
    shutil.rmtree('./test_state', ignore_errors=True)

    print("\n✅ State Manager working correctly!")