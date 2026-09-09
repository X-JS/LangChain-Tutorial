"""3.2 把提示词抽成模板"""

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{style}的风格回答，不要客套。"),
    ("human", "{question}"),
])

messages = prompt.invoke({
    "role": "数据库领域的技术顾问",
    "style": "简洁直接",
    "question": "向量数据库和传统数据库的核心区别是什么？",
})

model = init_chat_model("ollama:qwen3.5:9b", base_url="http://192.168.211.163:11434")
print(model.invoke(messages).content)
