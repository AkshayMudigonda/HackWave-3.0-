"""
Generic persistence layer (e.g. JSON/SQLite backend) used by
conversation and task history modules.
"""
from typing import Any, Dict, Optional


class MemoryStorage:
    """In-memory key-value storage engine."""

    def __init__(self):
        self._store: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def set(self, key: str, value: Any):
        self._store[key] = value

    def delete(self, key: str):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()
