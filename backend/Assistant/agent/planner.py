"""
Planner module: breaks a multitasking task down into an ordered sequence of steps/tool calls.
"""
import re
from typing import List, Optional
from core.models import Plan, PlanStep, RiskLevel, ToolRequest
from agent.intent import IntentEngine


class Planner:

    def __init__(self, reasoning):

        self.reasoning = reasoning
        self.intent_engine = IntentEngine()

    def create_workflow_plan(self, user_input: str) -> Plan:
        """Create dependency-aware plans for supported high-level objectives."""
        intent = self.intent_engine.detect(user_input)
        if intent.name == "system_monitoring":
            steps = [
                PlanStep("metrics", "Collect current system metrics", "system_monitor", verification_method="metrics_present"),
                PlanStep("processes", "Inspect active processes", "process_monitor", dependencies=["metrics"]),
                PlanStep("analysis", "Analyze health and evidence", "system_analyzer", dependencies=["metrics", "processes"]),
                PlanStep("anomalies", "Detect anomalous resource usage", "anomaly_detector", dependencies=["metrics"]),
            ]
            return Plan(user_input, steps)
        if intent.name == "workflow_automation":
            unavailable = {"status": "NOT_CONFIGURED", "message": "No external provider has been configured."}
            steps = [
                PlanStep("calendar", "Retrieve calendar context", "calendar", {"fallback": unavailable}),
                PlanStep("email", "Retrieve important email context", "email", {"fallback": unavailable}),
                PlanStep("tasks", "Retrieve task-list context", "task_list", {"fallback": unavailable}),
                PlanStep("schedule", "Prepare a schedule from available context", "schedule", dependencies=["calendar", "email", "tasks"]),
            ]
            return Plan(user_input, steps, RiskLevel.MEDIUM)
        if intent.name == "travel_planning":
            context = intent.entities
            steps = [
                PlanStep("weather", "Research weather", "weather", {"fallback": "NOT_CONFIGURED"}),
                PlanStep("transport", "Research transport", "transport", {"fallback": "NOT_CONFIGURED"}),
                PlanStep("hotels", "Research hotels", "hotel", {"fallback": "NOT_CONFIGURED"}),
                PlanStep("itinerary", "Prepare itinerary only from verified research", "itinerary", {"entities": context}, ["weather", "transport", "hotels"]),
            ]
            return Plan(user_input, steps, RiskLevel.MEDIUM)
        lowered = user_input.lower()
        if "download" in lowered and "pdf" in lowered and "pdf_reports" in lowered:
            return Plan(user_input, [PlanStep("pdf_organization", "Organize PDFs in Downloads", "pdf_organization", risk=RiskLevel.MEDIUM)])
        if "notepad" in lowered and "meeting_notes" in lowered:
            return Plan(user_input, [PlanStep("meeting_notes", "Prepare meeting notes", "meeting_notes", risk=RiskLevel.MEDIUM)])
        return Plan(user_input, [])

    def create_plan(self, user_input: str) -> Optional[ToolRequest]:
        """Create a single ToolRequest for a simple task."""
        tool_name = self.reasoning.classify(
            user_input
        )

        if tool_name is None:
            return None

        return self._build_request(
            tool_name,
            user_input,
        )

    def create_multi_plan(
        self,
        user_input: str,
        llm_client=None,
    ) -> List[ToolRequest]:
        """
        Decompose a multitasking user input into a list of ToolRequests.
        Uses Featherless AI (DeepSeek) if available, with deterministic fallback.
        """
        text = user_input.strip()
        if not text:
            return []

        lowered = text.lower()
        if "search" in lowered and any(site in lowered for site in ("youtube", "google")):
            return [self._build_request("browser", text)]

        # 1. Rule-based / deterministic multitasking decomposition. This must
        # run before single-tool classification: an arithmetic expression in a
        # compound command should not swallow the later commands.
        # Split on conjunct delimiters: " and ", " then ", " also ", ";", ","
        delimiters_pattern = r'\s+(?:and|then|also)\s+|[;,]\s*'
        segments = [s.strip() for s in re.split(delimiters_pattern, text, flags=re.IGNORECASE) if s.strip()]

        multi_requests = []
        if len(segments) > 1:
            for segment in segments:
                req = self.create_plan(segment)
                if req:
                    multi_requests.append(req)

            # If all segments were successfully resolved to tools
            if len(multi_requests) == len(segments):
                return multi_requests

        # 2. Fast deterministic single-step plan
        single_req = self.create_plan(text)
        if single_req:
            return [single_req]

        # 3. Try Featherless AI multitasking decomposition if client is provided
        if llm_client:
            try:
                llm_tasks = llm_client.decompose_multitask(text)
                if llm_tasks and isinstance(llm_tasks, list):
                    requests = []
                    for task in llm_tasks:
                        if isinstance(task, dict) and "tool" in task:
                            tool = task["tool"].lower().strip()
                            action = task.get("action", "execute")
                            params = task.get("parameters", {})
                            if not isinstance(params, dict):
                                params = {}
                            requests.append(
                                ToolRequest(
                                    tool=tool,
                                    action=action,
                                    parameters=params,
                                    original_input=text,
                                )
                            )
                    if requests:
                        return requests
            except Exception:
                pass

        # 4. Partial rule-based multi-plan fallback
        if len(segments) > 1 and multi_requests:
            return multi_requests

        return []

    def _build_request(
        self,
        tool_name: str,
        user_input: str,
    ) -> ToolRequest:

        text = user_input.strip()

        if tool_name == "calculator":

            expression = text

            if text.lower().startswith("calculate "):
                expression = text[10:].strip()
            elif text.lower().startswith("compute "):
                expression = text[8:].strip()
            elif text.lower().startswith("what is "):
                expression = text[8:].strip()

            return ToolRequest(
                tool="calculator",
                action="calculate",
                parameters={
                    "expression": expression
                },
                original_input=text,
            )

        if tool_name == "datetime":

            return ToolRequest(
                tool="datetime",
                action="get",
                parameters={
                    "query": text
                },
                original_input=text,
            )

        if tool_name == "browser":

            return ToolRequest(
                tool="browser",
                action="parse_and_execute",
                parameters={
                    "command": text
                },
                original_input=text,
            )

        if tool_name == "applications":

            return ToolRequest(
                tool="applications",
                action="parse_and_execute",
                parameters={
                    "command": text
                },
                original_input=text,
            )

        if tool_name == "filesystem":

            return ToolRequest(
                tool="filesystem",
                action="parse_and_execute",
                parameters={
                    "command": text
                },
                original_input=text,
            )

        if tool_name == "terminal":

            return ToolRequest(
                tool="terminal",
                action="parse_and_execute",
                parameters={
                    "command": text
                },
                original_input=text,
            )

        return ToolRequest(
            tool=tool_name,
            action="execute",
            parameters={"command": text},
            original_input=text,
        )
