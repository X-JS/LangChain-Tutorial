"""3.1 一行接入模型"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from common.config import (
    get_ollama_model,
    get_ollama_base_url
)

load_dotenv(override=True)

model = init_chat_model(
    f"ollama:{get_ollama_model()}",
    base_url=get_ollama_base_url()
)

resp = model.invoke("用一句话解释什么是向量数据库")
print(f"response content:\n{resp.content}")
print(f"token 用量:\n{resp.usage_metadata}")
print(f"模型名、停止原因等:\n{resp.response_metadata}")
print(f"")

resp = model.invoke([
    SystemMessage("你是一个数据库领域的技术顾问，回答简洁，不说客套话。"),
    HumanMessage("向量数据库和传统数据库的核心区别是什么？"),
])
print(f"response content:\n{resp.content}")
