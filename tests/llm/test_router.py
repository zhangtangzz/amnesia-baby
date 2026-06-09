"""
LLM 路由器测试
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.llm.router import LLMRouter
from src.llm.openai_provider import OpenAIProvider
from src.llm.deepseek_provider import DeepSeekProvider
from src.llm.qwen_provider import QwenProvider
from src.llm.models import LLMResponse, TokenUsage


class TestLLMRouter:
    """LLMRouter 测试"""

    def test_initialization(self):
        """测试路由器初始化"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="openai", api_key="test-key")
            assert router.get_provider_name() == "openai"

    def test_get_provider_openai(self):
        """测试获取 OpenAI 提供商"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="openai", api_key="test-key")
            provider = router.get_provider()
            assert isinstance(provider, OpenAIProvider)

    def test_get_provider_deepseek(self):
        """测试获取 DeepSeek 提供商"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="deepseek", api_key="test-key")
            provider = router.get_provider()
            assert isinstance(provider, DeepSeekProvider)

    def test_get_provider_qwen(self):
        """测试获取 Qwen 提供商"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="qwen", api_key="test-key")
            provider = router.get_provider()
            assert isinstance(provider, QwenProvider)

    def test_switch_provider(self):
        """测试切换提供商"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="openai", api_key="test-key")
            router.switch_provider("deepseek")
            assert router.get_provider_name() == "deepseek"
            assert isinstance(router.get_provider(), DeepSeekProvider)

    def test_invalid_provider_raises(self):
        """测试无效提供商"""
        with patch("src.llm.openai_provider.openai"):
            router = LLMRouter(default_provider="openai", api_key="test-key")
            with pytest.raises(ValueError, match="Unknown provider"):
                router.switch_provider("invalid")

    @pytest.mark.asyncio
    async def test_generate_delegates_to_provider(self):
        """测试 generate 委托给提供商"""
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

            router = LLMRouter(default_provider="openai", api_key="test-key")
            result = await router.generate([{"role": "user", "content": "hi"}])

            assert isinstance(result, LLMResponse)
            assert result.content == "Hello!"

    def test_list_providers(self):
        """测试列出所有提供商"""
        providers = LLMRouter.list_providers()
        assert "openai" in providers
        assert "deepseek" in providers
        assert "qwen" in providers
