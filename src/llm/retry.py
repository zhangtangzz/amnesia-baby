"""
重试与降级机制

提供 LLM 调用失败的自动重试和降级策略
"""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from .base import LLMProvider
from .models import LLMResponse

logger = logging.getLogger(__name__)


class RetryableLLMProvider:
    """
    可重试的 LLM 提供商包装器

    特性：
    - 自动重试（指数退避）
    - 降级到备用提供商
    """

    def __init__(
        self,
        provider: LLMProvider,
        max_retries: int = 3,
        fallback_provider: Optional[LLMProvider] = None,
        base_delay: float = 0.1,
    ):
        """
        初始化

        Args:
            provider: 主提供商
            max_retries: 最大重试次数
            fallback_provider: 降级提供商
            base_delay: 重试基础延迟（秒）
        """
        self._provider = provider
        self._max_retries = max_retries
        self._fallback = fallback_provider
        self._base_delay = base_delay

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """
        生成回复（带重试和降级）

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度
            max_tokens: 最大 token 数

        Returns:
            LLMResponse

        Raises:
            Exception: 主提供商和降级提供商都失败
        """
        # 尝试主提供商
        last_error = None
        for attempt in range(self._max_retries):
            try:
                return await self._provider.generate(
                    messages, model=model, temperature=temperature, max_tokens=max_tokens
                )
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Provider {self._provider.provider_name} attempt {attempt + 1}/{self._max_retries} failed: {e}"
                )
                if attempt < self._max_retries - 1:
                    delay = self._base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)

        # 主提供商失败，尝试降级
        if self._fallback:
            logger.info(f"Falling back to {self._fallback.provider_name}")
            try:
                return await self._fallback.generate(
                    messages, model=model, temperature=temperature, max_tokens=max_tokens
                )
            except Exception as fallback_error:
                logger.error(f"Fallback provider {self._fallback.provider_name} also failed: {fallback_error}")
                raise fallback_error

        raise last_error
