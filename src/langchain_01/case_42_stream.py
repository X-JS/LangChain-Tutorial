"""4.2 流式输出：逐字返回结果，不用等模型写完"""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = init_chat_model(
    os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{style}的风格回答，不要客套。"),
    ("human", "{question}"),
])

chain = prompt | model | StrOutputParser()

for chunk in chain.stream({
    "role": "数据库领域的技术顾问",
    "style": "简洁直接",
    "question": "向量数据库和传统数据库的核心区别是什么？",
}):
    print(chunk, end="", flush=True)
