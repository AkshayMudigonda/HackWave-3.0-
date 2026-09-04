"""
Observation representation: results/output captured from executing a
tool or action, fed back into the agent's context.
"""
from core.models import AgentObservation, ToolResult

Observation = AgentObservation

__all__ = [
    "Observation",
    "AgentObservation",
]
