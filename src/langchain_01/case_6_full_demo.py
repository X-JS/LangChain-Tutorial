"""6. 完整示例：读入用户反馈 -> 抽成结构化数据 -> 流式生成客服处理建议"""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv(override=True)

model = init_chat_model(
    os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
)


class Feedback(BaseModel):
    sentiment: Literal["正面", "负面", "中性"] = Field(description="整体情绪倾向")
    category: str = Field(description="问题所属模块，如登录、支付、性能")
    urgent: bool = Field(description="是否需要人工紧急介入")
    summary: str = Field(description="一句话概括，不超过 30 字")


extractor = model.with_structured_output(Feedback)

advice_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是客服主管，根据工单信息给出一条处理建议，两句话以内，不要客套。"),
        ("human", "模块：{category}\n紧急：{urgent}\n概要：{summary}"),
    ])
    | model
    | StrOutputParser()
)

raw = "付款页面点了三次都没反应，钱扣了订单没生成，急死了"

ticket = extractor.invoke(raw)
print(f"[{ticket.sentiment}] {ticket.category} 紧急={ticket.urgent}")
print(f"概要：{ticket.summary}\n建议：", end="")

for chunk in advice_chain.stream(ticket.model_dump()):
    print(chunk, end="", flush=True)
