"""Command-line interface for TaskFlow."""

import argparse
from collections.abc import Callable, Sequence

from taskflow.models import Task
from taskflow.service import TaskNotFoundError, TaskService
from taskflow.storage import JsonTaskStorage, StorageError

OutputFunction = Callable[[str], None]
InputFunction = Callable[[str], str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="TaskFlow：一个适合初学者的命令行任务管理器",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="添加任务")
    add_parser.add_argument("title", help="任务标题")

    list_parser = subparsers.add_parser("list", help="列出任务")
    list_parser.add_argument("--all", action="store_true", help="同时显示已完成任务")

    done_parser = subparsers.add_parser("done", help="完成任务")
    done_parser.add_argument("task_id", type=positive_integer, help="任务 ID")

    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("task_id", type=positive_integer, help="任务 ID")
    delete_parser.add_argument("--yes", action="store_true", help="跳过删除确认")

    return parser


def positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("任务 ID 必须是整数") from error
    if number < 1:
        raise argparse.ArgumentTypeError("任务 ID 必须是正整数")
    return number


def format_tasks(tasks: list[Task]) -> str:
    if not tasks:
        return "暂无任务。"
    lines = ["ID  状态  标题", "--  ----  ----"]
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        lines.append(f"{task.id:<2}  {status:^4}  {task.title}")
    return "\n".join(lines)


def main(
    argv: Sequence[str] | None = None,
    *,
    storage: JsonTaskStorage | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    service = TaskService(storage or JsonTaskStorage())
    try:
        if args.command == "add":
            task = service.add_task(args.title)
            output_fn(f"已添加任务 #{task.id}: {task.title}")
        elif args.command == "list":
            output_fn(format_tasks(service.list_tasks(include_completed=args.all)))
        elif args.command == "done":
            task = service.complete_task(args.task_id)
            output_fn(f"已完成任务 #{task.id}: {task.title}")
        elif args.command == "delete":
            if not args.yes:
                answer = input_fn(f"确认删除任务 #{args.task_id}？[y/N] ").strip().lower()
                if answer not in {"y", "yes"}:
                    output_fn("已取消删除。")
                    return 0
            task = service.delete_task(args.task_id)
            output_fn(f"已删除任务 #{task.id}: {task.title}")
    except (ValueError, TaskNotFoundError, StorageError) as error:
        output_fn(f"错误: {error}")
        return 1
    return 0
