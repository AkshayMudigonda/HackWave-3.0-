"""
Task representation: what the agent has been asked to do, its status,
and associated metadata.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from core.models import TaskStatus


@dataclass
class Task:
    """Represents a discrete task given to the agent."""
    query: str
    tool: Optional[str] = None
    status: str = TaskStatus.CREATED.value
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
