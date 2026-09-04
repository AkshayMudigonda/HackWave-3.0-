import unittest

from analytics.anomaly import AnomalyDetector
from system.analyzer import SystemAnalyzer


class TestSystemAnalysis(unittest.TestCase):
    def test_high_cpu_is_explained(self):
        report = SystemAnalyzer().analyze({"cpu_percent": 95, "memory_percent": 20, "disk_percent": 10})
        self.assertEqual(report["severity"], "HIGH")
        self.assertTrue(report["findings"])

    def test_threshold_anomaly(self):
        anomalies = AnomalyDetector().detect({"cpu_percent": 95})
        self.assertEqual(anomalies[0]["metric"], "cpu_percent")
