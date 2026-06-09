"""
流式响应测试
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.llm.openai_provider import OpenAIProvider
from src.llm.models import LLMResponse, TokenUsage


class TestStreaming:
    """流式响应测试"""

    @pytest.mark.asyncio
    async def test_stream_yields_chunks(self):
        """测试流式输出返回 chunk"""
        # Mock stream chunks
        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "Hello"
        chunk1.choices[0].finish_reason = None

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = " World"
        chunk2.choices[0].finish_reason = "stop"

        # Mock usage chunk
        usage_chunk = MagicMock()
        usage_chunk.choices = [MagicMock()]
        usage_chunk.choices[0].delta.content = None
        usage_chunk.choices[0].finish_reason = "stop"
        usage_chunk.usage = MagicMock()
        usage_chunk.usage.prompt_tokens = 10
        usage_chunk.usage.completion_tokens = 5
        usage_chunk.usage.total_tokens = 15

        async def mock_stream():
            yield chunk1
            yield chunk2
            yield usage_chunk

        with patch("src.llm.openai_provider.openai") as mock_openai:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_stream())
            mock_openai.AsyncOpenAI.return_value = mock_client

            provider = OpenAIProvider(api_key="test-key")
            chunks = []
            async for chunk in provider.stream([{"role": "user", "content": "hi"}]):
                chunks.append(chunk)

            assert "Hello" in chunks
            assert " World" in chunks

    @pytest.mark.asyncio
    async def test_base_stream_fallback(self):
        """测试基类 stream 默认调用 generate"""
        from src.llm.base import LLMProvider

        class SimpleProvider(LLMProvider):
            @property
            def provider_name(self):
                return "simple"

            @property
            def default_model(self):
                return "simple-model"

            async def generate(self, messages, model=None, temperature=0.7, max_tokens=500):
                return LLMResponse(
                    content="fallback content",
                    provider="simple",
                    model="simple-model",
                )

        provider = SimpleProvider()
        chunks = []
        async for chunk in provider.stream([{"role": "user", "content": "hi"}]):
            chunks.append(chunk)

        assert chunks == ["fallback content"]
