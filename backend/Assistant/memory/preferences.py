"""Persistent, non-sensitive user preference storage."""
import json
from typing import Any
from database.database import Database


class PreferenceMemory:
    def __init__(self, database: Database = None):
        self.database = database or Database()

    def set(self, key: str, value: Any) -> None:
        self.database.execute("INSERT INTO preferences (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) "
                              "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                              (key, json.dumps(value, default=str)))

    def get(self, key: str, default: Any = None) -> Any:
        row = self.database.fetch_one("SELECT value FROM preferences WHERE key = ?", (key,))
        return json.loads(row[0]) if row else default
