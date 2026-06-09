"""
通义千问 (Qwen) 提供商实现

通义千问 API 兼容 OpenAI 接口
"""

from .openai_provider import OpenAIProvider


class QwenProvider(OpenAIProvider):
    """
    通义千问 LLM 提供商

    继承 OpenAIProvider，使用阿里云 DashScope 端点
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        model: str = "qwen-turbo",
    ):
        super().__init__(api_key=api_key, base_url=base_url, model=model)

    @property
    def provider_name(self) -> str:
        return "qwen"
