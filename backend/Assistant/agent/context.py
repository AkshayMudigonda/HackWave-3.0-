"""
Context module: maintains the working context (recent observations,
task state, memory references) passed to reasoning/planning/decision.
"""
from dataclasses import dataclass, field
from typing import Any, List, Optional
from core.models import AgentObservation, ToolRequest


@dataclass
class AgentContext:
    """Working context for an agent session/turn."""
    user_input: str = ""
    current_request: Optional[ToolRequest] = None
    last_observation: Optional[AgentObservation] = None
    history: List[AgentObservation] = field(default_factory=list)

    def add_observation(self, observation: AgentObservation):
        self.last_observation = observation
        self.history.append(observation)

    def clear(self):
        self.user_input = ""
        self.current_request = None
        self.last_observation = None
        self.history.clear()
