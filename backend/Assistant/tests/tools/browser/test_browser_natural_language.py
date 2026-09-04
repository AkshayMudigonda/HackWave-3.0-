import unittest

from tools.browser.parser import BrowserParser


class TestNaturalLanguageBrowserParser(unittest.TestCase):
    def test_youtube_compound_request_forms_a_search_url(self):
        parsed = BrowserParser().parse("Open YouTube and search for 'Python tutorial', then open the first video.")
        self.assertEqual(parsed["engine"], "youtube")
        self.assertEqual(parsed["query"], "Python tutorial")
        self.assertIn("search_query=Python+tutorial", parsed["url"])

    def test_google_weather_is_a_search(self):
        parsed = BrowserParser().parse("Open Google and search for today's weather in Hyderabad.")
        self.assertEqual(parsed["engine"], "google")
        self.assertIn("weather", parsed["query"])
