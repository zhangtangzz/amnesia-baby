"""
小米 MIMO 提供商实现

基于 Anthropic 协议，通过小米 MIMO 代理访问大模型
"""

from typing import List, Dict, Optional, Any
import anthropic
from .base import LLMProvider
from .models import LLMResponse, TokenUsage


class XiaomiProvider(LLMProvider):
    """
    小米 MIMO LLM 提供商

    使用 Anthropic SDK 调用小米 MIMO 代理
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://token-plan-cn.xiaomimimo.com/anthropic",
        model: str = "mimo-v2.5-pro",
    ):
        """
        初始化小米提供商

        Args:
            api_key: API Key (tp-xxx)
            base_url: API Base URL
            model: 默认模型
        """
        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key,
            base_url=base_url,
        )

    @property
    def provider_name(self) -> str:
        return "xiaomi"

    @property
    def default_model(self) -> str:
        return self._model

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """
        生成回复

        Anthropic 协议中 system 是单独参数，不在 messages 里

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

        # 提取 system prompt
        system_prompt = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg)

        # 构建调用参数
        kwargs: Dict[str, Any] = {
            "model": model or self._model,
            "messages": user_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = await self.client.messages.create(**kwargs)

        # 提取内容
        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text

        # 提取 usage
        usage = response.usage
        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=response.model or (model or self._model),
            usage=TokenUsage(
                prompt_tokens=usage.input_tokens,
                completion_tokens=usage.output_tokens,
            ),
        )
