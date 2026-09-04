"""
Reasoning module: turns observations and context into intermediate
thoughts that inform planning and decisions.
"""
class Reasoning:

    def __init__(self, tool_manager):

        self.tool_manager = tool_manager

    def classify(self, user_input):

        text = user_input.strip().lower()

        if not text:
            return None

        # Calculator
        if self._calculator_request(text):
            return "calculator"

        # Browser
        if self._browser_request(text):
            return "browser"

        # Applications
        if self._application_request(text):
            return "applications"

        # Date and time
        if self._datetime_request(text):
            return "datetime"

        # Filesystem
        if self._filesystem_request(text):
            return "filesystem"

        # Terminal
        if self._terminal_request(text):
            return "terminal"

        return None

    def _calculator_request(self, text):

        if text in {
            "calculate",
            "calculator",
        }:
            return True

        if any(symbol in text for symbol in [
            "+",
            "-",
            "*",
            "/",
            "%",
            "^",
        ]):
            return any(
                char.isdigit()
                for char in text
            )

        return text.startswith(
            "calculate "
        )

    def _datetime_request(self, text):

        if "search" in text or "google" in text or "youtube" in text:
            return False

        keywords = [
            "today",
            "tomorrow",
            "yesterday",
            "current time",
            "current date",
            "what time",
            "what date",
            "date today",
            "time now",
            "day today",
        ]

        return any(
            keyword in text
            for keyword in keywords
        )

    def _browser_request(self, text):

        browser_prefixes = [
            "open google",
            "open youtube",
            "open github",
            "open wikipedia",
            "open maps",
            "open stackoverflow",
            "search ",
            "youtube ",
            "github ",
            "wikipedia ",
            "maps ",
            "stackoverflow ",
            "search for ",
        ]

        browser_domains = [
            ".com",
            ".org",
            ".net",
        ]

        if "search" in text and any(site in text for site in ("google", "youtube", "web", "internet")):
            return True

        if any(
            text.startswith(prefix)
            for prefix in browser_prefixes
        ):
            return True

        if any(
            domain in text
            for domain in browser_domains
        ):
            return True

        return False

    def _application_request(self, text):

        prefixes = [
            "open ",
            "close ",
            "restart ",
            "launch ",
            "start ",
            "stop ",
            "status ",
        ]

        if not any(
            text.startswith(prefix)
            for prefix in prefixes
        ):
            return False

        browser_words = [
            "google",
            "youtube",
            "github",
            "wikipedia",
            "maps",
            "stackoverflow",
        ]

        if any(
            word in text
            for word in browser_words
        ):
            return False

        return True

    def _filesystem_request(self, text):

        prefixes = [
            "create folder ",
            "create file ",
            "delete ",
            "rename ",
            "move ",
            "copy ",
            "find ",
            "list ",
        ]

        return any(
            text.startswith(prefix)
            for prefix in prefixes
        )

    def _terminal_request(self, text):

        prefixes = [
            "run ",
            "execute ",
            "terminal ",
        ]

        return any(
            text.startswith(prefix)
            for prefix in prefixes
        )
