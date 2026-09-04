from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.models import RiskLevel


@dataclass
class ActionMetadata:
    name: str
    description: str
    category: str
    risk_level: RiskLevel = RiskLevel.LOW
    requires_confirmation: bool = False
    reversible: bool = True
    permissions: List[str] = field(default_factory=list)
    verification_method: Optional[str] = None


class ActionRegistry:
    def __init__(self):
        self._actions: Dict[str, ActionMetadata] = {}

    def register(self, metadata: ActionMetadata) -> None:
        self._actions[metadata.name] = metadata

    def get(self, name: str) -> Optional[ActionMetadata]:
        return self._actions.get(name)

    def list(self) -> List[ActionMetadata]:
        return list(self._actions.values())
