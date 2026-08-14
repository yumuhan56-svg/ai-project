import pytest

from taskflow.models import Task


def test_task_strips_title_and_uses_defaults() -> None:
    task = Task(id=1, title="  学习 Git  ")
    assert task.title == "学习 Git"
    assert task.completed is False
    assert "T" in task.created_at


@pytest.mark.parametrize("title", ["", "   ", "\t\n"])
def test_task_rejects_blank_title(title: str) -> None:
    with pytest.raises(ValueError, match="不能为空"):
        Task(id=1, title=title)


@pytest.mark.parametrize("task_id", [0, -1, True, "1"])
def test_task_rejects_invalid_id(task_id: object) -> None:
    with pytest.raises(ValueError, match="正整数"):
        Task(id=task_id, title="任务")  # type: ignore[arg-type]


def test_task_round_trip_dict() -> None:
    original = Task(id=3, title="写测试", completed=True, created_at="2026-08-14T10:00:00+00:00")
    restored = Task.from_dict(original.to_dict())
    assert restored == original


def test_from_dict_reports_missing_field() -> None:
    with pytest.raises(ValueError, match="created_at"):
        Task.from_dict({"id": 1, "title": "任务"})
