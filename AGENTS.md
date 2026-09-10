# AGENTS.md

中文 LangChain 教程仓库（`uv` 管理，Python 3.14 锁在 `.python-version`，LangChain 1.4.0）。无测试、lint、格式化或 CI —— 不要自造校验命令，唯一的验证方式是直接运行脚本。

## 目录结构

- `src/common/config.py` —— 共享配置：`get_ollama_model()` / `get_ollama_base_url()`，从环境读取 Ollama 模型名与地址（**无内置默认值**）。
- `src/langchain_01/case_*.py` —— 第 1 篇案例：模型接入、提示词模板、管道组合、结构化输出、流式输出、工具调用 Agent。
- `src/langchain_02/case_full_demo.py` —— 第 2 篇完整示例：统一模型入口 `get_model()`，默认平台 ollama。
- 面向人的运行 / 编码说明见 `README.md`。

## 运行教程

- 每个案例都是独立脚本，模块顶层直接执行（**没有 `if __name__ == "__main__"`，无入口函数**）：
  `uv run python src/langchain_01/case_31_init_chat_model.py`
- 控制台脚本 `langchain-01` / `langchain-02`（`pyproject.toml`）只打印 "Hello"，是脚手架占位，**不是教程主体**。

## 环境与依赖

- 案例通过 `load_dotenv(override=True)` 读 `.env`：`OLLAMA_BASE_URL`（`http://192.168.211.163:11434`）、`OLLAMA_MODEL`（`qwen3.5:9b`）。`.env` 已被 gitignore，**新克隆需从 `.env.example` 复制**，否则 `langchain_01` 案例拿不到地址/模型名而失败。`.env` 另含当前未使用的 OpenAI 密钥。
- 已装依赖：`langchain`、`langchain-core`、`langchain-ollama`、`langchain-openai`、`pydantic`、`python-dotenv`。**未装 `langchain-community` 与 `langchain-deepseek`** —— 文章里 `SQLiteCache`、`ChatZhipuAI`、`deepseek:` provider 等写法直接运行会报错，需先 `uv add`。
- Ollama 一次只处理一个请求：**不要并行运行多个案例**（会排队并超时）。连接报错 / 超时 = Ollama 服务不可达，属环境问题，不是代码 bug。
- 案例 4.1/5/6 依赖工具调用；不支持工具调用的模型运行这些案例会静默失效。

## Windows / 编码

- 仓库文本 UTF-8（含中文），编辑时保持 UTF-8。查看文件用 Read/Grep 工具，不要用 pwsh 重定向读取（中文易乱码）。
- PowerShell 直接运行脚本会导致中文输出乱码（控制台代码页问题，非代码 bug）。需要正常输出时，运行前设 `$env:PYTHONIOENCODING="utf-8"`；三种解决办法见 `README.md`。
