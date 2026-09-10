"""3.3 用管道符 | 把 prompt 和 model 串起来"""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

model = init_chat_model(
    os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{style}的风格回答，不要客套。"),
    ("human", "{question}"),
])

inputs = {
    "role": "数据库领域的技术顾问",
    "style": "简洁直接",
    "question": "向量数据库和传统数据库的核心区别是什么？",
}

resp = (prompt | model).invoke(inputs)
print(resp.content)

chain = prompt | model | StrOutputParser()
print(chain.invoke(inputs))  # 直接得到 str，不用再 .content
