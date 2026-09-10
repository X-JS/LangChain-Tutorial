"""5. 给模型加工具：create_agent 工具调用循环"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

load_dotenv()


@tool
def get_order_status(order_id: str) -> str:
    """根据订单号查询订单状态。order_id 是形如 SO-12345 的字符串。"""
    fake_db = {"SO-12345": "已发货，预计明天送达", "SO-67890": "支付失败"}
    return fake_db.get(order_id, "未找到该订单")

model = init_chat_model(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL")
)

agent = create_agent(
    model=model,
    tools=[get_order_status],
    system_prompt="你是电商客服助手。涉及订单状态的问题必须调用工具查询，不要凭猜测回答。",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "帮我看下 SO-12345 到哪了"}]
})
print(result["messages"][-1].content)

print("---- 完整对话记录 ----")
for m in result["messages"]:
    print(type(m).__name__, ":", m.content)
