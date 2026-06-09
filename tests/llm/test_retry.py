"""
重试与降级机制测试
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.llm.retry import RetryableLLMProvider
from src.llm.models import LLMResponse, TokenUsage


class MockProvider:
    """Mock LLM 提供商"""

    def __init__(self, name="mock", fail_count=0):
        self._name = name
        self._fail_count = fail_count
        self._call_count = 0

    @property
    def provider_name(self):
        return self._name

    @property
    def default_model(self):
        return "mock-model"

    async def generate(self, messages, model=None, temperature=0.7, max_tokens=500):
        self._call_count += 1
        if self._call_count <= self._fail_count:
            raise Exception(f"{self._name} failed")
        return LLMResponse(
            content="success",
            provider=self._name,
            model=self.default_model,
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )


class TestRetryableLLMProvider:
    """RetryableLLMProvider 测试"""

    @pytest.mark.asyncio
    async def test_no_retry_on_success(self):
        """测试成功时不重试"""
        provider = MockProvider(fail_count=0)
        retryable = RetryableLLMProvider(provider, max_retries=3)

        result = await retryable.generate([{"role": "user", "content": "hi"}])
        assert result.content == "success"
        assert provider._call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_failure(self):
        """测试失败后重试成功"""
        provider = MockProvider(fail_count=2)
        retryable = RetryableLLMProvider(provider, max_retries=3)

        result = await retryable.generate([{"role": "user", "content": "hi"}])
        assert result.content == "success"
        assert provider._call_count == 3  # 失败2次 + 成功1次

    @pytest.mark.asyncio
    async def test_all_retries_fail_raises(self):
        """测试所有重试都失败"""
        provider = MockProvider(fail_count=5)
        retryable = RetryableLLMProvider(provider, max_retries=3)

        with pytest.raises(Exception):
            await retryable.generate([{"role": "user", "content": "hi"}])

    @pytest.mark.asyncio
    async def test_fallback_provider(self):
        """测试降级到备用提供商"""
        primary = MockProvider(name="primary", fail_count=5)
        fallback = MockProvider(name="fallback", fail_count=0)
        retryable = RetryableLLMProvider(primary, max_retries=2, fallback_provider=fallback)

        result = await retryable.generate([{"role": "user", "content": "hi"}])
        assert result.content == "success"
        assert result.provider == "fallback"

    @pytest.mark.asyncio
    async def test_fallback_not_used_on_success(self):
        """测试主提供商成功时不使用降级"""
        primary = MockProvider(name="primary", fail_count=0)
        fallback = MockProvider(name="fallback", fail_count=0)
        retryable = RetryableLLMProvider(primary, max_retries=2, fallback_provider=fallback)

        result = await retryable.generate([{"role": "user", "content": "hi"}])
        assert result.provider == "primary"
        assert fallback._call_count == 0

    @pytest.mark.asyncio
    async def test_fallback_also_fails_raises(self):
        """测试降级提供商也失败"""
        primary = MockProvider(name="primary", fail_count=5)
        fallback = MockProvider(name="fallback", fail_count=5)
        retryable = RetryableLLMProvider(primary, max_retries=2, fallback_provider=fallback)

        with pytest.raises(Exception):
            await retryable.generate([{"role": "user", "content": "hi"}])
