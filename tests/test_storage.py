import json

import pytest

from taskflow.models import Task
from taskflow.storage import JsonTaskStorage, StorageError


def test_missing_file_returns_empty_list(tmp_path) -> None:
    storage = JsonTaskStorage(tmp_path / "missing" / "tasks.json")
    assert storage.load() == []


def test_save_and_load_unicode_tasks(tmp_path) -> None:
    path = tmp_path / "nested" / "tasks.json"
    storage = JsonTaskStorage(path)
    tasks = [Task(id=1, title="学习 Python，完成练习！")]
    storage.save(tasks)
    assert storage.load() == tasks
    assert "学习 Python" in path.read_text(encoding="utf-8")


def test_invalid_json_is_not_overwritten(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    original = "{broken json"
    path.write_text(original, encoding="utf-8")
    storage = JsonTaskStorage(path)
    with pytest.raises(StorageError, match="无法读取"):
        storage.load()
    assert path.read_text(encoding="utf-8") == original


def test_non_list_json_is_rejected(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(StorageError, match="顶层必须是数组"):
        JsonTaskStorage(path).load()


def test_invalid_task_data_is_rejected(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    path.write_text('[{"id": 1}]', encoding="utf-8")
    with pytest.raises(StorageError, match="缺少字段"):
        JsonTaskStorage(path).load()
