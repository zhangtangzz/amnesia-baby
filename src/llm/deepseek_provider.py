"""
DeepSeek 提供商实现

DeepSeek API 兼容 OpenAI 接口
"""

from .openai_provider import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    """
    DeepSeek LLM 提供商

    继承 OpenAIProvider，使用 DeepSeek API 端点
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com/v1",
        model: str = "deepseek-chat",
    ):
        super().__init__(api_key=api_key, base_url=base_url, model=model)

    @property
    def provider_name(self) -> str:
        return "deepseek"
