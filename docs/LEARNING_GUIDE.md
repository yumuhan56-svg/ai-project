# TaskFlow 学习指南

这份指南用于理解项目，而不是背诵命令。每完成一节，都先预测结果，再亲自运行。

## 1. 认识虚拟环境

虚拟环境把当前项目的 Python 包与系统环境隔离。Windows PowerShell 中直接使用虚拟环境解释器最可靠：

```powershell
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip --version
```

`python -m pip` 表示“使用这个 Python 所属的 pip”，能避免把包装进错误环境。

## 2. 运行项目

```powershell
.venv\Scripts\python.exe -m taskflow --help
.venv\Scripts\python.exe -m taskflow add "学习 Git"
.venv\Scripts\python.exe -m taskflow list
```

观察 `data/tasks.json`。它是运行数据，因此被 `.gitignore` 排除。

## 3. 理解模块职责

- `models.py`：任务长什么样，以及数据是否合法。
- `storage.py`：如何读写 JSON，不负责业务规则。
- `service.py`：添加、查询、完成和删除任务。
- `cli.py`：解析命令、调用服务并显示结果。
- `tests/`：用自动化例子描述预期行为。

这种拆分让界面、业务和存储可以分别测试与替换。

## 4. 运行测试和检查

```powershell
.venv\Scripts\python.exe -m pytest -v
.venv\Scripts\python.exe -m pytest --cov=taskflow
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
```

测试失败时先读最下方的失败摘要，再读 `E` 开头的异常行和断言差异。

## 5. VS Code 调试练习

1. 打开 `src/taskflow/service.py`。
2. 在 `add_task` 第一行左侧单击，创建红色断点。
3. 打开“运行和调试”，选择“TaskFlow: 添加示例任务”。
4. 查看 `tasks`、`next_id` 和 `task` 的值。
5. 使用 F10 单步执行，观察何时写入 JSON。

## 6. Git 日常循环

```powershell
git status
git diff
git add <明确的文件>
git commit -m "feat: describe the change"
git log --oneline --decorate -5
```

提交前必须先看 `git diff`，确认没有密码、运行数据或无关改动。

## 7. 建议的亲手练习

按顺序完成，每题新建一个分支：

1. 给 `list` 添加 `--completed`，只显示已完成任务。
2. 添加 `rename ID 新标题` 命令。
3. 添加按标题关键字搜索的 `search` 命令。
4. 给每项功能先写一个失败测试，再实现功能让测试通过。

