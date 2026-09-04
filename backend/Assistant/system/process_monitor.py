from typing import Any, Dict, List


class ProcessMonitor:
    def top_processes(self, limit: int = 8) -> List[Dict[str, Any]]:
        try:
            import psutil
            items = []
            for process in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    items.append(process.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return sorted(items, key=lambda item: item.get("cpu_percent") or 0, reverse=True)[:limit]
        except ImportError:
            return []
