"""
Core datetime utilities and calculations.
"""
from datetime import datetime


class DateTime:

    def get(self, query: str) -> str:

        now = datetime.now()
        text = query.lower()

        if "time" in text and "date" not in text:
            return now.strftime("%I:%M:%S %p")

        if "date" in text or "today" in text:
            return now.strftime("%A, %d %B %Y")

        if "tomorrow" in text:
            from datetime import timedelta

            tomorrow = now + timedelta(days=1)

            return tomorrow.strftime(
                "%A, %d %B %Y"
            )

        if "yesterday" in text:
            from datetime import timedelta

            yesterday = now - timedelta(days=1)

            return yesterday.strftime(
                "%A, %d %B %Y"
            )

        return now.strftime(
            "%A, %d %B %Y, %I:%M:%S %p"
        )