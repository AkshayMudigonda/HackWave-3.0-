"""
Tests for core.observation.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.observation import Observation, AgentObservation


class TestObservation(unittest.TestCase):

    def test_observation_creation(self):
        obs = Observation(
            tool="calculator",
            success=True,
            data=42,
            message="Calculated 42",
        )
        self.assertEqual(obs.tool, "calculator")
        self.assertTrue(obs.success)
        self.assertEqual(obs.data, 42)
        self.assertIsInstance(obs, AgentObservation)


if __name__ == "__main__":
    unittest.main()
