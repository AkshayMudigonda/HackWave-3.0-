"""Best-effort system observations; unavailable hardware is represented as None."""
import platform
import time
from typing import Any, Dict


class SystemMonitor:
    def collect(self) -> Dict[str, Any]:
        observation = {"os": platform.platform(), "uptime_seconds": None, "cpu_percent": None,
                       "cpu_frequency_mhz": None, "memory_percent": None, "available_memory": None,
                       "disk_percent": None, "free_disk": None, "network": {}, "battery": None}
        try:
            import psutil
            boot = psutil.boot_time()
            observation.update({"uptime_seconds": max(0, int(time.time() - boot)), "cpu_percent": psutil.cpu_percent(interval=None)})
            frequency = psutil.cpu_freq()
            observation["cpu_frequency_mhz"] = frequency.current if frequency else None
            memory = psutil.virtual_memory()
            observation.update({"memory_percent": memory.percent, "available_memory": memory.available})
            disk = psutil.disk_usage("/")
            observation.update({"disk_percent": disk.percent, "free_disk": disk.free})
            net = psutil.net_io_counters()
            observation["network"] = {"bytes_sent": net.bytes_sent, "bytes_received": net.bytes_recv}
            battery = psutil.sensors_battery()
            observation["battery"] = {"percent": battery.percent, "plugged": battery.power_plugged} if battery else None
        except (ImportError, OSError, AttributeError):
            observation["unavailable"] = "psutil or a hardware metric is unavailable"
        return observation
