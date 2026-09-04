"""Deterministic risk classification for tool and action requests."""
from core.models import RiskLevel, ToolRequest


class RiskClassifier:
    _HIGH_ACTIONS = {"delete", "send_email", "book", "purchase", "close"}
    _CRITICAL_WORDS = {"shutdown", "format", "wipe", "rm -rf", "registry"}

    def classify(self, request: ToolRequest) -> RiskLevel:
        text = f"{request.action} {request.parameters} {request.original_input or ''}".lower()
        if any(word in text for word in self._CRITICAL_WORDS):
            return RiskLevel.CRITICAL
        if request.tool == "terminal" and any(word in text for word in ("echo", "dir", "whoami", "pwd")):
            return RiskLevel.LOW
        if request.action.lower() in self._HIGH_ACTIONS or request.tool in {"terminal"}:
            return RiskLevel.HIGH
        if request.tool in {"filesystem", "applications"}:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
