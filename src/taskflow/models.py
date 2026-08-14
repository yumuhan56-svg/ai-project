"""Domain models used by TaskFlow."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def current_time_iso() -> str:
    """Return a timezone-aware ISO 8601 timestamp."""
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass(slots=True)
class Task:
    """One task stored by TaskFlow."""

    id: int
    title: str
    completed: bool = False
    created_at: str = field(default_factory=current_time_iso)

    def __post_init__(self) -> None:
        if isinstance(self.id, bool) or not isinstance(self.id, int) or self.id < 1:
            raise ValueError("任务 ID 必须是正整数")
        if not isinstance(self.title, str):
            raise ValueError("任务标题必须是字符串")
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("任务标题不能为空")
        if not isinstance(self.completed, bool):
            raise ValueError("任务完成状态必须是布尔值")
        if not isinstance(self.created_at, str) or not self.created_at:
            raise ValueError("任务创建时间不能为空")

    def to_dict(self) -> dict[str, Any]:
        """Convert the task into JSON-serializable data."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Build a task from data loaded from JSON."""
        if not isinstance(data, dict):
            raise ValueError("每条任务数据必须是对象")
        try:
            return cls(
                id=data["id"],
                title=data["title"],
                completed=data.get("completed", False),
                created_at=data["created_at"],
            )
        except KeyError as error:
            raise ValueError(f"任务数据缺少字段: {error.args[0]}") from error
