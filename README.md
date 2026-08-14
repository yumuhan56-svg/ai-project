# TaskFlow

TaskFlow 是一个适合 Python 初学者学习工程化流程的命令行任务管理器。它使用标准库实现业务功能，以 JSON 保存数据，并使用 pytest、Ruff、Git 和 GitHub Actions保证质量。

## 功能

- 添加任务
- 默认查看未完成任务
- 查看全部任务
- 标记任务为完成
- 确认后删除任务
- UTF-8 JSON 本地持久化，支持中文
- 自动化测试、覆盖率和代码质量检查

## 环境要求

- Windows 10/11
- Python 3.12 或更高版本
- Git
- VS Code（推荐）

## 10 分钟安装

```powershell
git clone <你的仓库地址>
cd ai-project
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

如果是已经初始化好的本地目录，只需从创建虚拟环境开始。

## 使用方法

```powershell
.venv\Scripts\python.exe -m taskflow --help
.venv\Scripts\python.exe -m taskflow add "学习 Git"
.venv\Scripts\python.exe -m taskflow add "练习 pytest"
.venv\Scripts\python.exe -m taskflow list
.venv\Scripts\python.exe -m taskflow done 1
.venv\Scripts\python.exe -m taskflow list --all
.venv\Scripts\python.exe -m taskflow delete 2
```

安装后也可以直接运行：

```powershell
.venv\Scripts\taskflow.exe list --all
```

示例输出：

```text
ID  状态  标题
--  ----  ----
1   [x]   学习 Git
2   [ ]   练习 pytest
```

## 项目结构

```text
src/taskflow/       应用源代码
tests/              自动化测试
data/               本地 JSON 数据目录
docs/               学习指南
.vscode/            推荐扩展、测试和调试配置
.github/workflows/  GitHub Actions 持续集成
```

## 测试与质量检查

```powershell
.venv\Scripts\python.exe -m pytest -v
.venv\Scripts\python.exe -m pytest --cov=taskflow
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
```

## 常见问题

### PowerShell 提示禁止运行脚本

无需修改系统安全策略，直接使用 `.venv\Scripts\python.exe -m ...` 或对应的 `.exe` 文件。

### 数据保存在哪里

默认保存在 `data/tasks.json`，此文件不会提交到 GitHub。可使用环境变量 `TASKFLOW_DATA_FILE` 指定其他位置。

### JSON 损坏怎么办

TaskFlow 会停止并报告错误，不会覆盖损坏的文件。修复文件或将其备份后重新开始。

## 学习路线

请阅读 [TaskFlow 学习指南](docs/LEARNING_GUIDE.md)，其中包含模块说明、VS Code 调试步骤、Git 日常循环和四个扩展练习。

## 当前限制

- 单用户、单机使用
- 无图形界面
- 不支持云同步

这些限制是有意保留的，便于初学者先掌握清晰、可测试的小型工程。
