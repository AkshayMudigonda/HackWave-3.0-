"""Deterministic intent detection with lightweight entity extraction."""
import re
from core.models import Intent


class IntentEngine:
    def detect(self, text: str) -> Intent:
        lower = text.lower().strip()
        entities = self._entities(text)
        if any(term in lower for term in ("system health", "running slowly", "slow computer", "cpu", "memory usage")):
            return Intent("system_monitoring", .95, entities)
        if any(term in lower for term in ("trip", "travel", "hotel", "flight", "itinerary")):
            required = [key for key in ("origin", "destination", "date_range", "budget") if key not in entities]
            return Intent("travel_planning", .9, entities, required)
        if any(term in lower for term in ("organize my workday", "workday", "morning plan")):
            return Intent("workflow_automation", .9, entities)
        if re.search(r"\d\s*[+*/^-]\s*\d", lower) or lower.startswith("calculate "):
            return Intent("calculation", .99, entities)
        return Intent("unknown", .2, entities)

    def _entities(self, text):
        entities = {}
        route = re.search(r"from\s+(.+?)\s+to\s+(.+?)(?:\s+(?:on|next|under|for)\b|$)", text, re.I)
        if route:
            entities.update(origin=route.group(1).strip(), destination=route.group(2).strip())
        destination = re.search(r"(?:trip|travel)\s+(?:to|for)\s+([A-Za-z ]+?)(?:\s+(?:on|next|under|for)\b|$)", text, re.I)
        if destination and "destination" not in entities:
            entities["destination"] = destination.group(1).strip()
        budget = re.search(r"(?:under|budget(?: of)?)\s*[₹$]?\s*([\d,]+)", text, re.I)
        if budget:
            entities["budget"] = int(budget.group(1).replace(",", ""))
        dates = re.search(r"(next weekend|this weekend|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)", text, re.I)
        if dates:
            entities["date_range"] = dates.group(1)
        return entities
