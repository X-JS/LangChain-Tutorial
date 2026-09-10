"""2.7 完整示例：一个统一的模型入口

所有篇目通过 get_model() 拿模型实例。本仓库默认只使用本地 Ollama，
其他平台保留在 PLATFORMS 表中仅作参考，默认不会进入降级链。
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.caches import InMemoryCache
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.globals import set_llm_cache
from langchain_core.language_models import BaseChatModel

load_dotenv(override=True)

# 本地缓存全局只设一次，放在模块顶层，import 时就生效。
# 文章用的是 langchain-community 的 SQLiteCache；本仓库未装该依赖，改用内置内存缓存。
set_llm_cache(InMemoryCache())

# 用量统计也放模块级：跨函数、跨模型共用一个实例，才能汇总整个脚本的账。
usage_callback = UsageMetadataCallbackHandler()


@dataclass(frozen=True)
class Platform:
    """一个平台需要的三样东西：provider、key 的环境变量名、base_url。"""

    provider: str
    api_key_env: str
    base_url: str | None = None
    base_url_env: str | None = None

    def resolve_base_url(self) -> str | None:
        # 写死的 URL 优先级低于环境变量，方便临时换中转地址。
        if self.base_url_env and os.getenv(self.base_url_env):
            return os.getenv(self.base_url_env)
        return self.base_url


PLATFORMS: dict[str, Platform] = {
    "ollama": Platform(
        provider="ollama",
        api_key_env="",  # 本地不鉴权
        base_url="http://localhost:11434",
        base_url_env="OLLAMA_BASE_URL",
    ),
    "deepseek": Platform(
        provider="deepseek",
        api_key_env="DEEPSEEK_API_KEY",
        base_url_env="DEEPSEEK_BASE_URL",
    ),
    "zhipu": Platform(
        provider="openai",  # 走 OpenAI 兼容模式
        api_key_env="ZHIPUAI_API_KEY",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        base_url_env="ZHIPUAI_BASE_URL",
    ),
    "bailian": Platform(
        provider="openai",  # dashscope 没进注册表，借 openai
        api_key_env="DASHSCOPE_API_KEY",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "closeai": Platform(
        provider="openai",
        api_key_env="CLOSEAI_API_KEY",
        base_url_env="CLOSEAI_BASE_URL",
    ),
}


def _default_ollama_model() -> str:
    # .env 里可能写成 "ollama:qwen3.5:9b"，去掉前缀，避免拼出 ollama:ollama:...
    name = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    return name.split(":", 1)[1] if name.startswith("ollama:") else name


# 每个平台的默认模型，调用方不传 model 时用它。
DEFAULT_MODELS = {
    "ollama": _default_ollama_model(),
    "deepseek": "deepseek-v4-flash",
    "zhipu": "glm-5.1",
    "bailian": "qwen-plus",
    "closeai": "gpt-5.5",
}


def _build(platform: str, model: str | None = None, **kwargs) -> BaseChatModel:
    """按平台配置初始化单个模型，不带降级。"""
    if platform not in PLATFORMS:
        raise ValueError(f"未知平台 {platform}，可选：{list(PLATFORMS)}")

    conf = PLATFORMS[platform]
    params: dict = {
        "model": model or DEFAULT_MODELS[platform],
        "model_provider": conf.provider,
        **kwargs,
    }

    api_key = os.getenv(conf.api_key_env) if conf.api_key_env else None
    if api_key:
        params["api_key"] = api_key
    if base_url := conf.resolve_base_url():
        params["base_url"] = base_url

    return init_chat_model(**params)


def get_model(
    platform: str = "ollama",
    model: str | None = None,
    temperature: float = 0.2,
    timeout: int = 60,
    max_retries: int = 3,
    fallbacks: list[str] | None = None,
    **kwargs,
) -> BaseChatModel:
    """拿一个带降级的模型实例。

    platform  平台键，见 PLATFORMS
    model     模型名，不传用该平台默认
    fallbacks 降级链，按顺序尝试；传 [] 表示不要降级
    kwargs    透传给底层，比如 max_tokens、extra_body
    """
    primary = _build(
        platform,
        model,
        temperature=temperature,
        timeout=timeout,
        max_retries=max_retries,
        **kwargs,
    )

    # 默认降级到另一家线上平台，再退到本地，避免同厂商一起挂。
    if fallbacks is None:
        candidates = [p for p in ("bailian", "ollama") if p != platform]
        # 只保留已配置好的平台：ollama 本地不鉴权，其他平台要有对应的 key。
        # 本仓库默认只配了 ollama，所以默认降级链为空，不会调用其他供应商。
        fallbacks = [
            p
            for p in candidates
            if not PLATFORMS[p].api_key_env or os.getenv(PLATFORMS[p].api_key_env)
        ]

    backups = [
        _build(p, temperature=temperature, timeout=timeout)
        for p in fallbacks
        if p in PLATFORMS
    ]
    return primary.with_fallbacks(backups) if backups else primary


def print_usage(reset: bool = True) -> None:
    """打印到目前为止的 token 用量，按模型名分组。"""
    data = usage_callback.usage_metadata
    if not data:
        print("没有采集到用量，检查 config 里是否传了 callbacks")
        return

    for name, u in data.items():
        cached = u.get("input_token_details", {}).get("cache_read", 0)
        reasoning = u.get("output_token_details", {}).get("reasoning", 0)
        print(
            f"{name:<28} 输入 {u['input_tokens']:>6}"
            f"（缓存命中 {cached}） 输出 {u['output_tokens']:>6}"
            f"（思考 {reasoning}） 合计 {u['total_tokens']:>6}"
        )

    if reset:
        usage_callback.usage_metadata.clear()


# ---------------------------------------------------------------------------
# 使用示例
# ---------------------------------------------------------------------------

model = get_model()                                 # 默认 ollama
local = get_model("ollama", fallbacks=[])           # 本地，明确不要降级
strict = get_model(temperature=0, max_tokens=500)   # 抽取类任务，稳定优先

resp = model.invoke(
    "用一句话解释什么是向量检索",
    config={"callbacks": [usage_callback]},
)
print(resp.content)
print_usage()
