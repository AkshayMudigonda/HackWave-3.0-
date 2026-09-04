import sys
import os
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Ensure Assistant directory is in sys.path
_assistant_root = str(Path(__file__).resolve().parent)
if _assistant_root not in sys.path:
    sys.path.insert(0, _assistant_root)

from agent.agent import Agent
from interface.text.text_interface import TextInterface

from tools.tool_manager import ToolManager

from tools.calculator.calculator_tool import CalculatorTool
from tools.datetime.datetime_tool import DateTimeTool
from tools.browser.browser_tool import BrowserTool
from tools.applications.applications_tool import ApplicationsTool
from tools.filesystem.filesystem_tool import FilesystemTool
from tools.terminal.terminal_tool import TerminalTool


def create_tool_manager():

    manager = ToolManager()

    manager.register(
        "calculator",
        CalculatorTool(),
    )

    manager.register(
        "datetime",
        DateTimeTool(),
    )

    manager.register(
        "browser",
        BrowserTool(),
    )

    manager.register(
        "applications",
        ApplicationsTool(),
    )

    manager.register(
        "filesystem",
        FilesystemTool(),
    )

    manager.register(
        "terminal",
        TerminalTool(),
    )

    return manager


def _allowed_origins():
    """Read trusted browser origins without permitting every website by default."""
    raw = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173")
    return {origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()}


def create_api_server(agent, host="0.0.0.0", port=None):
    """Expose the existing agent through a small dependency-free JSON API."""
    allowed_origins = _allowed_origins()
    server_port = port or int(os.environ.get("PORT", "8000"))

    class AssistantApiHandler(BaseHTTPRequestHandler):
        def _origin(self):
            origin = self.headers.get("Origin", "").rstrip("/")
            return origin if origin in allowed_origins else None

        def _send_json(self, status, payload):
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            origin = self._origin()
            if origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(encoded)

        def do_OPTIONS(self):
            if not self._origin():
                self._send_json(403, {"success": False, "error": "Origin is not allowed."})
                return
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", self._origin())
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Vary", "Origin")
            self.end_headers()

        def do_GET(self):
            if self.path == "/health":
                self._send_json(200, {"success": True, "status": "ok"})
                return
            self._send_json(404, {"success": False, "error": "Route not found."})

        def do_POST(self):
            if self.path != "/api/assist":
                self._send_json(404, {"success": False, "error": "Route not found."})
                return
            if self.headers.get("Origin") and not self._origin():
                self._send_json(403, {"success": False, "error": "Origin is not allowed."})
                return
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
                if content_length <= 0 or content_length > 16_384:
                    raise ValueError("Request body must be between 1 and 16384 bytes.")
                payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
                message = payload.get("message") if isinstance(payload, dict) else None
                if not isinstance(message, str) or not message.strip():
                    raise ValueError("'message' must be a non-empty string.")
                if len(message) > 8_000:
                    raise ValueError("'message' must be 8000 characters or fewer.")
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                self._send_json(400, {"success": False, "error": str(exc)})
                return

            try:
                reply = agent.run(message)
                self._send_json(200, {"success": True, "message": reply})
            except Exception:
                # Do not expose internals or provider details to browsers.
                self._send_json(500, {"success": False, "error": "The assistant encountered an unexpected error."})

        def log_message(self, format, *args):
            # Keep routine HTTP logs out of user-facing console output.
            return

    return ThreadingHTTPServer((host, server_port), AssistantApiHandler)


def main():

    tool_manager = create_tool_manager()

    agent = Agent(tool_manager)

    interface = TextInterface()

    interface.run(agent)


def serve():
    """Run the browser API. Start with: python main.py --serve"""
    import webbrowser
    import threading

    agent = Agent(create_tool_manager())
    server = create_api_server(agent)
    frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
    print(f"Assistant API listening on http://localhost:{server.server_port}")
    print(f"Opening frontend at {frontend_url} …")
    # Open browser shortly after the server starts so it is ready to accept connections.
    threading.Timer(1.5, lambda: webbrowser.open(frontend_url)).start()
    server.serve_forever()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        serve()
    else:
        main()
