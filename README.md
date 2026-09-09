# langchain-01

通过本地 [Ollama](https://ollama.com)（`http://192.168.211.163:11434`，默认模型 `qwen3.5:9b`）跑通 LangChain 的基础用法骨架：模型接入、提示词模板、管道组合、结构化输出、流式输出、带工具调用的 Agent。

环境基线：Python 3.14、LangChain 1.2.x（`uv` 管理）。

## 项目结构

```
src/langchain_01/
├── __init__.py
├── case_31_init_chat_model.py    # 3.1 一行接入模型
├── case_32_prompt_template.py    # 3.2 提示词模板
├── case_33_lc_pipe.py            # 3.3 管道符 | 串联 prompt、model、parser
├── case_41_structured_output.py  # 4.1 结构化输出（Pydantic + with_structured_output）
├── case_42_stream.py             # 4.2 流式输出
├── case_5_agent_with_tool.py     # 5.  给模型加工具（create_agent 工具循环）
└── case_6_full_demo.py           # 6.  完整示例（抽取工单 → 生成处理建议）
```

## 使用方法

### 1. 同步环境

```powershell
uv sync
```

### 2. 确认 Ollama 服务可达

```powershell
(Invoke-RestMethod -Uri "http://192.168.211.163:11434/api/tags").models.name
```

脚本通过 `.env` 中的 `OLLAMA_BASE_URL` 与 `OLLAMA_MODEL` 读取连接信息（默认 `http://192.168.211.163:11434` 的 `qwen3.5:9b`）。复制 `.env.example` 为 `.env` 并按需修改即可切换地址/模型。模型需支持工具调用，否则 §4.1/§5/§6 无法跑通。

### 3. 运行案例

```powershell
uv run python src/langchain_01/case_31_init_chat_model.py
# ... 依此类推
uv run python src/langchain_01/case_6_full_demo.py
```

首次调用会加载模型，单次约 20~30 秒，属正常现象。模型一次只处理一个请求，**不要并行跑多个案例**，否则会互相排队甚至超时。

## 字符编码问题解决办法

在 PowerShell 中直接运行脚本时，中文输出可能变成乱码（如 `�?`、`�`），原因是 PowerShell 默认控制台代码页与 Python 的 UTF-8 输出不一致，并非代码问题。三种解决办法：

1. **运行前设置 UTF-8 环境变量（推荐，只对本次命令生效）：**

   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   uv run python src/langchain_01/case_31_init_chat_model.py
   ```

2. **永久生效：** 打开系统「设置 → 时间和语言 → 语言和区域 → 管理语言设置 → 更改系统区域设置」，勾选「Beta: 使用 Unicode UTF-8 提供全球语言支持」，重启后所有控制台均默认 UTF-8。

3. **脚本内处理：** 在脚本顶部加 `sys.stdout.reconfigure(encoding="utf-8")`（Python 3.7+），并在脚本前先执行 `chcp 65001` 切换代码页。
