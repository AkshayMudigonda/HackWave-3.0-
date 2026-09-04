import unittest

from agent.planner import Planner
from agent.reasoning import Reasoning
from tools.tool_manager import ToolManager


class TestWorkflowPlanning(unittest.TestCase):
    def setUp(self):
        self.planner = Planner(Reasoning(ToolManager()))

    def test_notepad_notes_requires_context_workflow(self):
        plan = self.planner.create_workflow_plan("Open Notepad and create a new file called meeting_notes.txt")
        self.assertEqual(plan.steps[0].tool, "meeting_notes")

    def test_pdf_download_workflow(self):
        plan = self.planner.create_workflow_plan("Open Downloads, identify PDFs, create PDF_Reports, and move PDFs into it")
        self.assertEqual(plan.steps[0].tool, "pdf_organization")
