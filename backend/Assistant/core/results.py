"""
Result and response types returned by tools and the agent.
"""
from typing import Any, Optional

from core.models import ToolResult


def success(
    message: str = "",
    data: Any = None,
    **kwargs: Any,
) -> ToolResult:
    """Create a successful ToolResult."""
    return ToolResult(
        success=True,
        data=data,
        message=str(message) if message else "",
    )


def failure(
    message: str = "",
    error: Optional[str] = None,
    data: Any = None,
    **kwargs: Any,
) -> ToolResult:
    """Create a failed ToolResult."""
    err_str = error if error is not None else (message if message else "Operation failed.")
    return ToolResult(
        success=False,
        data=data,
        message=str(message) if message else err_str,
        error=err_str,
    )


def success_result(
    data: Any = None,
    message: str = "",
    **kwargs: Any,
) -> ToolResult:
    """Alias for success ToolResult with data as first param."""
    return ToolResult(
        success=True,
        data=data,
        message=message,
    )


def failure_result(
    message: str = "Operation failed.",
    error: str = "",
    data: Any = None,
    **kwargs: Any,
) -> ToolResult:
    """Alias for failure ToolResult with message as first param."""
    return ToolResult(
        success=False,
        data=data,
        message=message,
        error=error if error else message,
    )