"""
Tracks and persists terminal command history.
"""
from typing import List, Dict, Any


class TerminalHistory:
    """In-memory and persistent command history tracker."""

    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def record(self, command: str, result: Dict[str, Any]):
        self._history.append({
            "command": command,
            "result": result,
        })

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._history[-limit:]

    def clear(self):
        self._history.clear()
