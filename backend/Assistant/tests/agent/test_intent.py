import unittest
from agent.intent import IntentEngine


class TestIntentEngine(unittest.TestCase):
    def test_trip_entities(self):
        result = IntentEngine().detect("Plan a trip from Hyderabad to Bangalore next weekend under ₹15,000")
        self.assertEqual(result.name, "travel_planning")
        self.assertEqual(result.entities["origin"], "Hyderabad")
        self.assertEqual(result.entities["destination"], "Bangalore")
        self.assertEqual(result.entities["budget"], 15000)
