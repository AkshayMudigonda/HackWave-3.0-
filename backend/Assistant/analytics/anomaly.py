import statistics
from typing import Dict, List
from analytics.metrics import MetricHistory


class AnomalyDetector:
    thresholds = {"cpu_percent": 90, "memory_percent": 90, "disk_percent": 90}

    def detect(self, metrics: Dict[str, object], history: MetricHistory = None) -> List[Dict[str, object]]:
        anomalies = []
        for metric, threshold in self.thresholds.items():
            value = metrics.get(metric)
            if not isinstance(value, (int, float)):
                continue
            if value >= threshold:
                anomalies.append({"metric": metric, "severity": "HIGH", "reason": f"threshold exceeded ({value} >= {threshold})", "evidence": value})
            if history:
                values = history.values(metric)
                if len(values) >= 5:
                    mean, deviation = statistics.mean(values), statistics.pstdev(values)
                    if deviation and value > mean + 3 * deviation:
                        anomalies.append({"metric": metric, "severity": "MEDIUM", "reason": "deviation from rolling baseline", "evidence": value})
        return anomalies
