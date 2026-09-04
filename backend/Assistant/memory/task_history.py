"""
Stores and retrieves a history of completed/attempted tasks.
"""
import json
from typing import List

from core.task import Task
from database.database import Database


class TaskHistory:

    def __init__(self, database: Database = None):

        self.database = database or Database()

    def record_task(self, task: Task):

        result = task.result

        if not isinstance(result, str):
            try:
                result = json.dumps(result)
            except (TypeError, ValueError):
                result = str(result)

        self.database.execute(
            """
            INSERT INTO tasks (
                query,
                tool,
                status,
                result,
                error
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                task.query,
                task.tool,
                task.status,
                result,
                task.error,
            ),
        )

    def get_tasks(self) -> List[Task]:

        rows = self.database.fetch_all(
            """
            SELECT
                query,
                tool,
                status,
                result,
                error
            FROM tasks
            ORDER BY id ASC
            """
        )

        tasks = []

        for row in rows:

            query, tool, status, result, error = row

            task = Task(
                query=query,
                tool=tool,
                status=status,
                result=result,
                error=error,
            )

            tasks.append(task)

        return tasks

    def clear(self):

        self.database.execute(
            "DELETE FROM tasks"
        )