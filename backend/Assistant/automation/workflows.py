"""Reusable workflow descriptors; execution remains owned by Agent."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class WorkflowDefinition:
    name: str
    objective: str
    steps: List[str]


class WorkflowLibrary:
    def __init__(self):
        self._workflows: Dict[str, WorkflowDefinition] = {
            "system_health": WorkflowDefinition("system_health", "Check system health", ["metrics", "processes", "analysis", "anomalies"]),
            "morning_workday": WorkflowDefinition("morning_workday", "Organize my workday", ["calendar", "email", "tasks", "schedule"]),
        }

    def get(self, name: str):
        return self._workflows.get(name)

    def list(self) -> List[WorkflowDefinition]:
        return list(self._workflows.values())
