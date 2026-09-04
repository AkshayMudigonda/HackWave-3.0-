"""
Registry of known applications and how to launch/locate them.
"""
import os


class ApplicationRegistry:

    def __init__(self):
        self.applications = {
            "chrome": {
                "name": "Google Chrome",
                "command": "chrome",
                "process": "chrome",
            },
            "google chrome": {
                "name": "Google Chrome",
                "command": "chrome",
                "process": "chrome",
            },
            "vs code": {
                "name": "Visual Studio Code",
                "command": "code",
                "process": "code",
            },
            "vscode": {
                "name": "Visual Studio Code",
                "command": "code",
                "process": "code",
            },
            "visual studio code": {
                "name": "Visual Studio Code",
                "command": "code",
                "process": "code",
            },
            "notepad": {
                "name": "Notepad",
                "command": "notepad",
                "process": "notepad",
            },
            "calculator": {
                "name": "Calculator",
                "command": "calc",
                "process": "calculator",
            },
            "paint": {
                "name": "Paint",
                "command": "mspaint",
                "process": "mspaint",
            },
            "explorer": {
                "name": "File Explorer",
                "command": "explorer",
                "process": "explorer",
            },
            "file explorer": {
                "name": "File Explorer",
                "command": "explorer",
                "process": "explorer",
            },
            "chatgpt": {
                "name": "ChatGPT",
                "command": "chatgpt",
                "process": "chatgpt",
            },
        }

    def find(self, name: str):

        key = name.lower().strip()

        return self.applications.get(key)