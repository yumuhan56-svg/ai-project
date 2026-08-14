"""Business logic for TaskFlow."""

from taskflow.models import Task
from taskflow.storage import JsonTaskStorage


class TaskNotFoundError(LookupError):
    """Raised when a requested task ID does not exist."""


class TaskService:
    """Perform task operations independently of the user interface."""

    def __init__(self, storage: JsonTaskStorage) -> None:
        self.storage = storage

    def add_task(self, title: str) -> Task:
        tasks = self.storage.load()
        next_id = max((task.id for task in tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list_tasks(self, include_completed: bool = False) -> list[Task]:
        tasks = sorted(self.storage.load(), key=lambda task: task.id)
        if include_completed:
            return tasks
        return [task for task in tasks if not task.completed]

    def complete_task(self, task_id: int) -> Task:
        tasks = self.storage.load()
        task = self._find_task(tasks, task_id)
        if not task.completed:
            task.completed = True
            self.storage.save(tasks)
        return task

    def delete_task(self, task_id: int) -> Task:
        tasks = self.storage.load()
        task = self._find_task(tasks, task_id)
        tasks.remove(task)
        self.storage.save(tasks)
        return task

    @staticmethod
    def _find_task(tasks: list[Task], task_id: int) -> Task:
        for task in tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"找不到 ID 为 {task_id} 的任务")
