"""
Response representation: the agent's final or intermediate output
returned to the caller/user.
"""
from core.models import AgentResponse

Response = AgentResponse

__all__ = [
    "Response",
    "AgentResponse",
]
