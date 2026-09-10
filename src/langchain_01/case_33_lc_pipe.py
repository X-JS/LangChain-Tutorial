"""3.3 用管道符 | 把 prompt 和 model 串起来"""


from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from common.config import (
    get_ollama_model,
    get_ollama_base_url
)

load_dotenv(override=True)

model = init_chat_model(
    f"ollama:{get_ollama_model()}",
    base_url=get_ollama_base_url()
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
