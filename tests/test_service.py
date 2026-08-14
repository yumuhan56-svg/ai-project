import pytest

from taskflow.models import Task
from taskflow.service import TaskNotFoundError, TaskService
from taskflow.storage import JsonTaskStorage


def make_service(tmp_path) -> TaskService:
    return TaskService(JsonTaskStorage(tmp_path / "tasks.json"))


def test_add_generates_increasing_ids(tmp_path) -> None:
    service = make_service(tmp_path)
    first = service.add_task("第一个")
    second = service.add_task("第二个")
    assert (first.id, second.id) == (1, 2)


def test_deleted_id_is_not_reused_when_later_ids_exist(tmp_path) -> None:
    service = make_service(tmp_path)
    service.add_task("一")
    service.add_task("二")
    service.delete_task(1)
    assert service.add_task("三").id == 3


def test_list_hides_completed_by_default(tmp_path) -> None:
    service = make_service(tmp_path)
    service.add_task("未完成")
    service.add_task("要完成")
    service.complete_task(2)
    assert [task.id for task in service.list_tasks()] == [1]
    assert [task.id for task in service.list_tasks(include_completed=True)] == [1, 2]


def test_complete_is_idempotent(tmp_path) -> None:
    service = make_service(tmp_path)
    service.add_task("任务")
    assert service.complete_task(1).completed is True
    assert service.complete_task(1).completed is True


def test_delete_returns_removed_task(tmp_path) -> None:
    service = make_service(tmp_path)
    service.add_task("待删除")
    removed = service.delete_task(1)
    assert removed.title == "待删除"
    assert service.list_tasks(include_completed=True) == []


@pytest.mark.parametrize("operation", ["complete", "delete"])
def test_missing_task_raises_clear_error(tmp_path, operation: str) -> None:
    service = make_service(tmp_path)
    with pytest.raises(TaskNotFoundError, match="99"):
        if operation == "complete":
            service.complete_task(99)
        else:
            service.delete_task(99)


def test_list_sorts_existing_tasks_by_id(tmp_path) -> None:
    storage = JsonTaskStorage(tmp_path / "tasks.json")
    storage.save([Task(id=3, title="三"), Task(id=1, title="一")])
    assert [task.id for task in TaskService(storage).list_tasks()] == [1, 3]
