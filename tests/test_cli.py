from taskflow.cli import format_tasks, main, positive_integer
from taskflow.models import Task
from taskflow.storage import JsonTaskStorage


def run_cli(tmp_path, args, *, answers=None):
    output: list[str] = []
    answer_iter = iter(answers or [])
    code = main(
        args,
        storage=JsonTaskStorage(tmp_path / "tasks.json"),
        input_fn=lambda _prompt: next(answer_iter),
        output_fn=output.append,
    )
    return code, output


def test_no_command_prints_help(capsys) -> None:
    assert main([]) == 0
    assert "TaskFlow" in capsys.readouterr().out


def test_add_list_done_and_list_all(tmp_path) -> None:
    assert run_cli(tmp_path, ["add", "学习 Git"])[0] == 0
    assert "学习 Git" in run_cli(tmp_path, ["list"])[1][0]
    assert run_cli(tmp_path, ["done", "1"])[0] == 0
    assert run_cli(tmp_path, ["list"])[1] == ["暂无任务。"]
    assert "学习 Git" in run_cli(tmp_path, ["list", "--all"])[1][0]


def test_delete_can_be_cancelled(tmp_path) -> None:
    run_cli(tmp_path, ["add", "保留我"])
    code, output = run_cli(tmp_path, ["delete", "1"], answers=["n"])
    assert code == 0
    assert output == ["已取消删除。"]
    assert "保留我" in run_cli(tmp_path, ["list"])[1][0]


def test_delete_with_yes_skips_prompt(tmp_path) -> None:
    run_cli(tmp_path, ["add", "删除我"])
    code, output = run_cli(tmp_path, ["delete", "1", "--yes"])
    assert code == 0
    assert "已删除" in output[0]


def test_missing_task_returns_error(tmp_path) -> None:
    code, output = run_cli(tmp_path, ["done", "99"])
    assert code == 1
    assert output[0].startswith("错误:")


def test_blank_title_returns_error_without_creating_data(tmp_path) -> None:
    path = tmp_path / "tasks.json"
    output: list[str] = []
    code = main(["add", "   "], storage=JsonTaskStorage(path), output_fn=output.append)
    assert code == 1
    assert not path.exists()


def test_format_tasks_shows_status() -> None:
    text = format_tasks(
        [
            Task(id=1, title="未完成"),
            Task(id=2, title="已完成", completed=True),
        ]
    )
    assert "[ ]" in text
    assert "[x]" in text


def test_positive_integer_validation() -> None:
    assert positive_integer("2") == 2
