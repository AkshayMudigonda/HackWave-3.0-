"""
Tests for Filesystem tool.
"""
import sys
import os
import unittest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.filesystem.parser import FilesystemParser
from tools.filesystem.filesystem_tool import FilesystemTool
from core.models import ToolRequest


class TestFilesystem(unittest.TestCase):

    def setUp(self):
        self.parser = FilesystemParser()
        self.tool = FilesystemTool()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_parse_create_folder(self):
        parsed = self.parser.parse("create folder test_dir")
        self.assertEqual(parsed["action"], "create_folder")
        self.assertEqual(parsed["path"], "test_dir")

    def test_create_and_delete_file(self):
        file_path = os.path.join(self.test_dir, "sample.txt")
        req = ToolRequest(tool="filesystem", action="parse_and_execute", parameters={"command": f"create file {file_path}"})
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        self.assertTrue(os.path.exists(file_path))

        del_req = ToolRequest(tool="filesystem", action="parse_and_execute", parameters={"command": f"delete {file_path}"})
        del_res = self.tool.execute(del_req)
        self.assertTrue(del_res.success)
        self.assertFalse(os.path.exists(file_path))


if __name__ == "__main__":
    unittest.main()
