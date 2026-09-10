"""4.1 结构化输出：Pydantic 模型 + with_structured_output"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()


class Feedback(BaseModel):
    sentiment: Literal["正面", "负面", "中性"] = Field(description="整体情绪倾向")
    category: str = Field(description="问题所属模块，如登录、支付、性能")
    urgent: bool = Field(description="是否需要紧急处理")
    summary: str = Field(description="一句话概括，不超过 30 字")


model = init_chat_model(
    os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
)
extractor = model.with_structured_output(Feedback)

result = extractor.invoke("付款页面点了三次都没反应，钱扣了订单没生成，急死了")
print(result.sentiment, result.category, result.urgent)
print(type(result))  # <class '__main__.Feedback'>
