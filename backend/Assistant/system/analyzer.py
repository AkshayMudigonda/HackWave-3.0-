from typing import Any, Dict, List


class SystemAnalyzer:
    def analyze(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []
        checks = (("cpu_percent", "CPU utilization", 90), ("memory_percent", "Memory utilization", 90), ("disk_percent", "Disk utilization", 90))
        for key, label, threshold in checks:
            value = metrics.get(key)
            if value is not None and value >= threshold:
                findings.append({"severity": "HIGH", "metric": key, "reason": f"{label} is {value}% (threshold: {threshold}%).", "evidence": value})
        score = max(0, 100 - 25 * len(findings))
        return {"health_score": score, "severity": "HIGH" if findings else "NORMAL", "findings": findings,
                "recommendations": ["Inspect high-resource processes before closing anything."] if findings else ["No urgent resource issue was detected."]}
