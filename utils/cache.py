"""
Cache Utility
Caches analysis results to avoid redundant API calls
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
from config.constants import CACHE_DIR, CACHE_TTL, ENABLE_CACHE


class CacheManager:
    """
    Simple file-based cache for analysis results
    """

    def __init__(self):
        if ENABLE_CACHE:
            Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, task: str, filename: str) -> str:
        """
        Generate a unique cache key from task and filename

        Args:
            task: Analysis task description
            filename: Data filename

        Returns:
            str: MD5 hash as cache key
        """
        content = f"{task.strip().lower()}_{filename.strip().lower()}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, task: str, filename: str) -> Optional[dict]:
        """
        Retrieve cached result if it exists and isn't expired

        Args:
            task: Analysis task
            filename: Data filename

        Returns:
            dict: Cached result, or None if not found/expired
        """
        if not ENABLE_CACHE:
            return None

        try:
            key = self._get_cache_key(task, filename)
            cache_file = Path(CACHE_DIR) / f"{key}.json"

            if not cache_file.exists():
                return None

            with open(cache_file, 'r') as f:
                cached = json.load(f)

            # Check if cache has expired
            cached_at = datetime.fromisoformat(cached['cached_at'])
            if datetime.now() - cached_at > timedelta(seconds=CACHE_TTL):
                cache_file.unlink()  # Delete expired cache
                return None

            return cached.get('result')

        except Exception:
            return None

    def set(self, task: str, filename: str, result: dict) -> bool:
        """
        Cache an analysis result

        Args:
            task: Analysis task
            filename: Data filename
            result: Result to cache

        Returns:
            bool: True if cached successfully
        """
        if not ENABLE_CACHE:
            return False

        try:
            key = self._get_cache_key(task, filename)
            cache_file = Path(CACHE_DIR) / f"{key}.json"

            cache_data = {
                'task': task,
                'filename': filename,
                'cached_at': datetime.now().isoformat(),
                'result': result
            }

            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)

            return True

        except Exception:
            return False

    def invalidate(self, task: str, filename: str) -> bool:
        """
        Remove a specific cached result

        Args:
            task: Analysis task
            filename: Data filename

        Returns:
            bool: True if deleted successfully
        """
        try:
            key = self._get_cache_key(task, filename)
            cache_file = Path(CACHE_DIR) / f"{key}.json"

            if cache_file.exists():
                cache_file.unlink()
                return True
            return False

        except Exception:
            return False

    def clear_all(self) -> int:
        """
        Clear all cached results

        Returns:
            int: Number of cache entries cleared
        """
        count = 0
        for cache_file in Path(CACHE_DIR).glob('*.json'):
            cache_file.unlink()
            count += 1
        return count

    def get_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            dict: Cache stats (size, count, etc.)
        """
        cache_files = list(Path(CACHE_DIR).glob('*.json'))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            'enabled': ENABLE_CACHE,
            'entries': len(cache_files),
            'size_kb': round(total_size / 1024, 2),
            'ttl_seconds': CACHE_TTL,
            'directory': str(CACHE_DIR)
        }


# Global instance
cache_manager = CacheManager()


if __name__ == "__main__":
    print("🧪 Testing Cache Manager...")

    cache = CacheManager()

    # Test set and get
    task = "Analyze sales trends"
    filename = "sales_data.csv"
    result = {"summary": "Sales increased by 20%", "charts": ["output.png"]}

    cache.set(task, filename, result)
    print("✅ Cache set successfully")

    retrieved = cache.get(task, filename)
    print(f"✅ Cache get: {retrieved}")

    # Test cache miss
    miss = cache.get("Different task", filename)
    print(f"✅ Cache miss: {miss is None}")

    # Test stats
    stats = cache.get_stats()
    print(f"✅ Cache stats: {stats}")

    # Test clear
    cleared = cache.clear_all()
    print(f"✅ Cleared {cleared} cache entries")

    print("\n✅ Cache Manager working correctly!")