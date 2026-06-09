"""
OpenAI 提供商实现
"""

from typing import List, Dict, Optional, AsyncIterator
import openai
from .base import LLMProvider
from .models import LLMResponse, TokenUsage


class OpenAIProvider(LLMProvider):
    """
    OpenAI LLM 提供商

    基于 openai SDK 调用 OpenAI 兼容 API
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-3.5-turbo",
    ):
        """
        初始化 OpenAI 提供商

        Args:
            api_key: API Key
            base_url: API Base URL
            model: 默认模型
        """
        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def default_model(self) -> str:
        return self._model

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """
        生成回复

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度
            max_tokens: 最大 token 数

        Returns:
            LLMResponse
        """
        if not messages:
            raise ValueError("Messages cannot be empty")

        response = await self.client.chat.completions.create(
            model=model or self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        usage = response.usage

        return LLMResponse(
            content=choice.message.content,
            provider=self.provider_name,
            model=model or self._model,
            usage=TokenUsage(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            ),
            finish_reason=choice.finish_reason,
        )

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> AsyncIterator[str]:
        """
        流式生成回复

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度
            max_tokens: 最大 token 数

        Yields:
            str: 文本 chunk
        """
        if not messages:
            raise ValueError("Messages cannot be empty")

        response = await self.client.chat.completions.create(
            model=model or self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
