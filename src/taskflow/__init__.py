"""TaskFlow: a beginner-friendly command-line task manager."""

from taskflow.models import Task
from taskflow.service import TaskNotFoundError, TaskService
from taskflow.storage import JsonTaskStorage, StorageError

__all__ = [
    "JsonTaskStorage",
    "StorageError",
    "Task",
    "TaskNotFoundError",
    "TaskService",
]
__version__ = "0.1.0"
