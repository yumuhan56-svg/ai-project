"""JSON persistence for TaskFlow."""

import json
import os
from pathlib import Path

from taskflow.models import Task


class StorageError(RuntimeError):
    """Raised when task data cannot be loaded or saved safely."""


def default_data_path() -> Path:
    """Return the configured data file or the project-local default."""
    configured_path = os.environ.get("TASKFLOW_DATA_FILE")
    return Path(configured_path) if configured_path else Path("data/tasks.json")


class JsonTaskStorage:
    """Load and save tasks in a UTF-8 JSON file."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_data_path()

    def load(self) -> list[Task]:
        """Load all tasks. A missing file represents an empty task list."""
        if not self.path.exists():
            return []
        try:
            with self.path.open(encoding="utf-8") as file:
                raw_data = json.load(file)
            if not isinstance(raw_data, list):
                raise ValueError("JSON 顶层必须是数组")
            return [Task.from_dict(item) for item in raw_data]
        except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
            raise StorageError(f"无法读取任务文件 {self.path}: {error}") from error

    def save(self, tasks: list[Task]) -> None:
        """Atomically save all tasks without exposing a partially written file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        try:
            with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(
                    [task.to_dict() for task in tasks],
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
                file.write("\n")
            temporary_path.replace(self.path)
        except (OSError, TypeError, ValueError) as error:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise StorageError(f"无法保存任务文件 {self.path}: {error}") from error
