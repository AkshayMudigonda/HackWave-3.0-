"""
Custom exceptions used throughout the assistant system.
"""
class AssistantError(Exception):
    """Base exception for the assistant."""


class ToolError(AssistantError):
    """Raised when a tool operation fails."""


class ToolNotFoundError(ToolError):
    """Raised when a requested tool is not registered."""


class InvalidToolRequestError(ToolError):
    """Raised when a tool request is invalid."""


class AgentError(AssistantError):
    """Raised when the agent encounters an error."""