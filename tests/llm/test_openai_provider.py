"""
OpenAI 提供商测试
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.llm.openai_provider import OpenAIProvider
from src.llm.models import LLMResponse, TokenUsage


class TestOpenAIProvider:
    """OpenAIProvider 测试"""

    def test_provider_name(self):
        """测试提供商名称"""
        with patch("src.llm.openai_provider.openai"):
            provider = OpenAIProvider(api_key="test-key")
            assert provider.provider_name == "openai"

    def test_default_model(self):
        """测试默认模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = OpenAIProvider(api_key="test-key")
            assert provider.default_model == "gpt-3.5-turbo"

    def test_custom_model(self):
        """测试自定义模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = OpenAIProvider(api_key="test-key", model="gpt-4o")
            assert provider.default_model == "gpt-4o"

    @pytest.mark.asyncio
    async def test_generate_returns_response(self):
        """测试 generate 返回 LLMResponse"""
        mock_choice = MagicMock()
        mock_choice.message.content = "Hello!"
        mock_choice.finish_reason = "stop"

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 10
        mock_usage.completion_tokens = 5
        mock_usage.total_tokens = 15

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.usage = mock_usage

        with patch("src.llm.openai_provider.openai") as mock_openai:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_openai.AsyncOpenAI.return_value = mock_client

            provider = OpenAIProvider(api_key="test-key")
            result = await provider.generate([{"role": "user", "content": "hi"}])

            assert isinstance(result, LLMResponse)
            assert result.content == "Hello!"
            assert result.provider == "openai"
            assert result.usage.total_tokens == 15

    @pytest.mark.asyncio
    async def test_generate_passes_parameters(self):
        """测试参数传递"""
        mock_choice = MagicMock()
        mock_choice.message.content = "Hi"
        mock_choice.finish_reason = "stop"

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 5
        mock_usage.completion_tokens = 3
        mock_usage.total_tokens = 8

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_response.usage = mock_usage

        with patch("src.llm.openai_provider.openai") as mock_openai:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_openai.AsyncOpenAI.return_value = mock_client

            provider = OpenAIProvider(api_key="test-key")
            messages = [{"role": "system", "content": "You are helpful"}, {"role": "user", "content": "hi"}]
            await provider.generate(messages, model="gpt-4", temperature=0.5, max_tokens=100)

            call_args = mock_client.chat.completions.create.call_args
            assert call_args.kwargs["model"] == "gpt-4"
            assert call_args.kwargs["temperature"] == 0.5
            assert call_args.kwargs["max_tokens"] == 100

    @pytest.mark.asyncio
    async def test_generate_empty_messages_raises(self):
        """测试空消息列表"""
        with patch("src.llm.openai_provider.openai"):
            provider = OpenAIProvider(api_key="test-key")
            with pytest.raises(ValueError, match="Messages cannot be empty"):
                await provider.generate([])
