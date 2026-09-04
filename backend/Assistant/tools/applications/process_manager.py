"""
Manages application processes: launch, track, and terminate.
"""
import subprocess


class ProcessManager:

    def open(self, application: dict) -> bool:

        try:
            subprocess.Popen(
                application["command"],
                shell=True,
            )

            return True

        except Exception:
            return False

    def close(self, application: dict) -> bool:

        process = application.get("process")

        if not process:
            return False

        try:
            subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    f"{process}.exe",
                    "/F",
                ],
                capture_output=True,
                text=True,
            )

            return True

        except Exception:
            return False

    def restart(self, application: dict) -> bool:

        self.close(application)

        return self.open(application)