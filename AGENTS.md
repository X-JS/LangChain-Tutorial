# AGENTS.md

Chinese LangChain tutorial repo (`uv`-managed, Python 3.14 pinned in `.python-version`). No tests, linter, formatter, or CI — do not invent verification commands; the only way to verify a case is to run it.

## Running the tutorial

- Each lesson is a standalone script under `src/langchain_01/case_*.py` with module-level top-level code (no `if __name__ == "__main__"`, no entry point). Run directly:
  `uv run python src/langchain_01/case_31_init_chat_model.py`
- The console scripts `langchain-01` / `langchain-02` (in `pyproject.toml`) only print "Hello" — they are scaffold stubs, not the tutorial. `src/langchain_02/` is an empty placeholder.

## Environment quirks

- Every case reads the Ollama endpoint/model from `.env` via `load_dotenv()`: `OLLAMA_BASE_URL` (default `http://192.168.211.163:11434`) and `OLLAMA_MODEL` (default `ollama:qwen3.5:9b`). Since each file falls back to those hardcoded defaults, `.env` is optional — copy `.env.example` and edit it (or the fallbacks) to point elsewhere. `.env` also carries OPENAI keys (unused by current cases).
- Connection errors/timeouts mean the Ollama host is unreachable — an environment issue, not a code bug. Ollama handles one request at a time, so never run cases in parallel (they queue and time out).
- Tool-calling is required for cases 4.1/5/6; a non-tool model silently breaks those.

## Windows / encoding

- Repo text is UTF-8 (Chinese). Preserve UTF-8 on edit; when reading via `pwsh` redirects output can garble — prefer the Read/Grep tools.
- Running scripts from PowerShell garbles Chinese output (console code page, not a code bug). Set `$env:PYTHONIOENCODING="utf-8"` before `uv run` when output matters.
