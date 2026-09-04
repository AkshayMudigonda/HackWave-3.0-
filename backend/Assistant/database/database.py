import sqlite3
import json
from pathlib import Path
from typing import Any, List, Tuple


class Database:

    def __init__(self, db_path: str = None):

        if db_path is None:
            project_root = Path(__file__).resolve().parent.parent
            data_dir = project_root / "data"
            data_dir.mkdir(parents=True, exist_ok=True)

            db_path = data_dir / "assistant.db"

        self.db_path = str(db_path)

        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    tool TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, name TEXT NOT NULL,
                    status TEXT NOT NULL, risk TEXT, parameters TEXT, result TEXT,
                    error TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, tool TEXT,
                    success INTEGER NOT NULL, data TEXT, message TEXT, error TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, metric_type TEXT NOT NULL,
                    payload TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS anomalies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, metric TEXT NOT NULL, severity TEXT,
                    evidence TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS workflow_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, workflow_name TEXT NOT NULL,
                    status TEXT NOT NULL, summary TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            connection.commit()

    def execute(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ):

        with self._connect() as connection:

            cursor = connection.execute(
                query,
                parameters,
            )

            connection.commit()

            return cursor

    def fetch_all(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ) -> List[Tuple]:

        with self._connect() as connection:

            cursor = connection.execute(
                query,
                parameters,
            )

            return cursor.fetchall()

    def fetch_one(
        self,
        query: str,
        parameters: Tuple[Any, ...] = (),
    ):

        with self._connect() as connection:

            cursor = connection.execute(
                query,
                parameters,
            )

            return cursor.fetchone()

    def record_observation(self, task_id: str, tool: str, success: bool, data: Any = None,
                           message: str = "", error: str = None):
        self.execute("INSERT INTO observations (task_id, tool, success, data, message, error) VALUES (?, ?, ?, ?, ?, ?)",
                     (task_id, tool, int(success), json.dumps(data, default=str), message, error))

    def record_metric(self, metric_type: str, payload: Any):
        self.execute("INSERT INTO system_metrics (metric_type, payload) VALUES (?, ?)",
                     (metric_type, json.dumps(payload, default=str)))
