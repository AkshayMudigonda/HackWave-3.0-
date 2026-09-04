import unittest

from tools.applications.parser import ApplicationParser


class TestApplicationParser(unittest.TestCase):
    def test_open_and_write_keeps_application_name_clean(self):
        parsed = ApplicationParser().parse('open notepad and write "HELLO WORLD"')
        self.assertEqual(parsed["application"], "notepad")
        self.assertEqual(parsed["text"], "HELLO WORLD")
