"""
LLM 提供商抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from .models import LLMResponse


class LLMProvider(ABC):
    """
    LLM 提供商抽象基类

    所有 LLM 提供商必须实现此接口
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商名称"""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """默认模型名称"""
        ...

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """
        生成回复（非流式）

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model: 模型名称，None 则使用默认
            temperature: 温度
            max_tokens: 最大 token 数

        Returns:
            LLMResponse
        """
        ...

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> AsyncIterator[str]:
        """
        流式生成回复（默认实现：调用 generate 后一次性返回）

        子类可覆盖实现真正的流式输出
        """
        response = await self.generate(messages, model, temperature, max_tokens)
        yield response.content
