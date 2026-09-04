"""
Shared data models (pydantic/dataclasses) used across the agent, tools,
and interface layers.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    REPLANNING = "REPLANNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ToolRequest:
    tool: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    original_input: Optional[str] = None


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    message: str = ""
    error: Optional[str] = None


@dataclass
class AgentObservation:
    tool: str
    success: bool
    data: Any = None
    message: str = ""
    error: Optional[str] = None


@dataclass
class AgentResponse:
    success: bool
    message: str
    observation: Optional[AgentObservation] = None


@dataclass
class Intent:
    name: str
    confidence: float
    entities: Dict[str, Any] = field(default_factory=dict)
    required_context: List[str] = field(default_factory=list)


@dataclass
class PlanStep:
    id: str
    description: str
    tool: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    risk: RiskLevel = RiskLevel.LOW
    requires_confirmation: bool = False
    status: str = "PENDING"
    verification_method: Optional[str] = None
    retries: int = 0


@dataclass
class Plan:
    objective: str
    steps: List[PlanStep]
    estimated_risk: RiskLevel = RiskLevel.LOW


@dataclass
class DecisionRecord:
    observation: Optional[AgentObservation]
    evidence: List[str]
    reasoning_summary: str
    confidence: float
    risk: RiskLevel
    action: str
    next_step: Optional[str] = None
