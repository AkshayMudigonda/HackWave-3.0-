"""
Top-level Agent orchestration: ties together reasoning, planning,
multitasking execution, and decision-making into a single run loop.
"""
import sys
import os
from pathlib import Path
from typing import Optional

# Ensure Assistant directory is in sys.path
_assistant_root = str(Path(__file__).resolve().parent.parent)
if _assistant_root not in sys.path:
    sys.path.insert(0, _assistant_root)

import uuid
import shutil
from core.models import AgentObservation, TaskStatus, ToolRequest
from core import config
from database.database import Database
from actions.executor import ActionExecutor
from system.monitor import SystemMonitor
from system.process_monitor import ProcessMonitor
from system.analyzer import SystemAnalyzer
from analytics.anomaly import AnomalyDetector
from analytics.metrics import MetricHistory
from core.llm import FeatherlessClient
from agent.reasoning import Reasoning
from agent.planner import Planner
from agent.decision import Decision


class Agent:

    def __init__(self, tool_manager, llm_client: Optional[FeatherlessClient] = None, database=None, confirmation=None):

        self.tool_manager = tool_manager

        self.reasoning = Reasoning(
            tool_manager
        )

        self.planner = Planner(
            self.reasoning
        )

        self.decision = Decision()

        self.llm_client = llm_client or FeatherlessClient()
        self.database = database or Database()
        self.executor = ActionExecutor(tool_manager, self.database, confirmation=confirmation)
        self.metrics_history = MetricHistory()

    def run(self, user_input: str) -> str:
        """Process any user input and always return a meaningful response."""

        text = user_input.strip() if user_input else ""

        # --- Empty input guard ---
        if not text:
            return "I didn't catch that. Could you please say something?"

        lower = text.lower()

        # --- Built-in meta-commands ---
        # /models  → list all available Featherless AI models
        if lower in ("/models", "list models", "show models", "available models"):
            models = self.llm_client.list_models()
            lines = ["Available Featherless AI models:\n"]
            current = self.llm_client.get_model()
            for m in models:
                marker = " ✔ (active)" if m == current else ""
                lines.append(f"  • {m}{marker}")
            return "\n".join(lines)

        # /model <name>  → switch active model
        if lower.startswith("/model ") or lower.startswith("use model ") or lower.startswith("switch model "):
            parts = text.split(None, 1)
            if len(parts) == 2:
                new_model = parts[1].strip()
                known = self.llm_client.set_model(new_model)
                status = "(recognised model)" if known else "(custom/unlisted model — will attempt anyway)"
                return f"Active model switched to: {new_model} {status}"

        # --- Workflow plans (multi-step structured tasks) ---
        workflow = self.planner.create_workflow_plan(text)
        if workflow.steps:
            return self._run_workflow(workflow)

        # --- Multi-task / tool decomposition ---
        requests = self.planner.create_multi_plan(
            text,
            llm_client=self.llm_client,
        )

        if requests:
            # Execute all decomposed tasks in sequence and collect observations
            observations = []
            for req in requests:
                result = self.executor.execute(req)
                obs = AgentObservation(
                    tool=req.tool,
                    success=result.success,
                    data=result.data,
                    message=result.message,
                    error=result.error,
                )
                observations.append(obs)
                self.database.record_observation("", obs.tool, obs.success, obs.data, obs.message, obs.error)

            # Synthesize decision and format final response
            return self.decision.format_response(observations)

        # --- Conversational AI fallback (always responds) ---
        # Every input that doesn't match a tool gets answered by the LLM.
        # ask_guaranteed() never returns an empty string.
        return self.llm_client.ask_guaranteed(
            text,
            system_prompt=config.ASSISTANT_SYSTEM_PROMPT,
        )

    def _run_workflow(self, plan):
        task_id = str(uuid.uuid4())
        self.database.execute("INSERT INTO tasks (query, status, result) VALUES (?, ?, ?)", (plan.objective, TaskStatus.EXECUTING.value, ""))
        outputs, completed = {}, []
        for step in plan.steps:
            if any(dep not in outputs for dep in step.dependencies):
                step.status = "BLOCKED"
                outputs[step.id] = {"status": "BLOCKED"}
                continue
            output = self._execute_workflow_step(step, outputs)
            outputs[step.id] = output
            step.status = "COMPLETED" if output.get("success", True) else "FAILED"
            completed.append((step, output))
        successful = all(step.status == "COMPLETED" for step, _ in completed)
        status = TaskStatus.COMPLETED.value if successful else TaskStatus.FAILED.value
        self.database.execute("UPDATE tasks SET status = ?, result = ? WHERE query = ? AND status = ?", (status, str(outputs), plan.objective, TaskStatus.EXECUTING.value))
        lines = [f"TASK: {plan.objective}"]
        for step, output in completed:
            marker = "✓" if step.status == "COMPLETED" else "✗"
            detail = output.get("summary") or output.get("message") or output.get("status", "completed")
            lines.append(f"[{marker}] {step.description}: {detail}")
        return "\n".join(lines)

    def _execute_workflow_step(self, step, outputs):
        if step.tool == "meeting_notes":
            return {"success": False, "status": "WAITING_FOR_INPUT", "summary": "Please provide the three project points before I create meeting_notes.txt; I will not invent project details."}
        if step.tool == "pdf_organization":
            downloads = Path.home() / "Downloads"
            if not downloads.is_dir():
                return {"success": False, "summary": f"Downloads folder was not found: {downloads}"}
            destination = downloads / "PDF_Reports"
            destination.mkdir(exist_ok=True)
            pdfs = [entry for entry in downloads.iterdir() if entry.is_file() and entry.suffix.lower() == ".pdf"]
            moved = []
            for pdf in pdfs:
                target = destination / pdf.name
                if target.exists():
                    return {"success": False, "summary": f"Stopped safely because destination already contains {pdf.name}."}
                shutil.move(str(pdf), str(target))
                moved.append(pdf.name)
            manifest = destination / "moved_pdfs.txt"
            manifest.write_text("\n".join(moved), encoding="utf-8")
            return {"success": True, "summary": f"Moved {len(moved)} PDF file(s) and wrote {manifest.name}.", "data": moved}
        if step.tool == "system_monitor":
            data = SystemMonitor().collect(); self.metrics_history.add(data); self.database.record_metric("system", data)
            return {"success": True, "data": data, "summary": "Metrics collected."}
        if step.tool == "process_monitor":
            processes = ProcessMonitor().top_processes()
            return {"success": True, "data": processes, "summary": f"Collected {len(processes)} process records."}
        if step.tool == "system_analyzer":
            data = SystemAnalyzer().analyze(outputs["metrics"]["data"])
            return {"success": True, "data": data, "summary": f"Health score: {data['health_score']}; severity: {data['severity']}."}
        if step.tool == "anomaly_detector":
            data = AnomalyDetector().detect(outputs["metrics"]["data"], self.metrics_history)
            for anomaly in data:
                self.database.execute("INSERT INTO anomalies (metric, severity, evidence) VALUES (?, ?, ?)", (anomaly["metric"], anomaly["severity"], str(anomaly["evidence"])))
            return {"success": True, "data": data, "summary": f"Found {len(data)} anomaly/anomalies."}
        if step.tool == "schedule":
            unavailable = [key for key, value in outputs.items() if value.get("status") == "NOT_CONFIGURED"]
            return {"success": True, "summary": "No schedule finalized; missing integrations: " + ", ".join(unavailable)}
        fallback = step.parameters.get("fallback", "NOT_CONFIGURED")
        message = fallback.get("message", "Integration is not configured.") if isinstance(fallback, dict) else "Integration is not configured."
        return {"success": True, "status": "NOT_CONFIGURED", "summary": message}


if __name__ == "__main__":
    from main import main
    main()
