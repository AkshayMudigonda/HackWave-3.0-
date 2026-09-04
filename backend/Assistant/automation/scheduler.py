"""Small scheduler seam for future recurring workflows without background side effects."""
from typing import Callable, Dict


class WorkflowScheduler:
    def __init__(self):
        self._jobs: Dict[str, Callable[[], object]] = {}

    def register(self, name: str, callback: Callable[[], object]) -> None:
        self._jobs[name] = callback

    def run_now(self, name: str):
        if name not in self._jobs:
            raise KeyError(f"Unknown workflow: {name}")
        return self._jobs[name]()
