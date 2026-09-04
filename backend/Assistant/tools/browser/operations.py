"""
Low-level browser operations (navigate, click, fill, extract content).
"""
import webbrowser


class BrowserOperations:

    def open(self, url: str) -> bool:
        return webbrowser.open(url)