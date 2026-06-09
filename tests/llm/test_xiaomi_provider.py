"""
小米 MIMO 提供商测试（Anthropic 协议）
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.llm.xiaomi_provider import XiaomiProvider
from src.llm.models import LLMResponse, TokenUsage


class TestXiaomiProvider:
    """XiaomiProvider 测试"""

    def test_provider_name(self):
        """测试提供商名称"""
        with patch("src.llm.xiaomi_provider.anthropic"):
            provider = XiaomiProvider(api_key="test-key")
            assert provider.provider_name == "xiaomi"

    def test_default_model(self):
        """测试默认模型"""
        with patch("src.llm.xiaomi_provider.anthropic"):
            provider = XiaomiProvider(api_key="test-key")
            assert provider.default_model == "mimo-v2.5-pro"

    def test_custom_model(self):
        """测试自定义模型"""
        with patch("src.llm.xiaomi_provider.anthropic"):
            provider = XiaomiProvider(api_key="test-key", model="mimo-v2-lite")
            assert provider.default_model == "mimo-v2-lite"

    def test_default_base_url(self):
        """测试默认 base_url"""
        with patch("src.llm.xiaomi_provider.anthropic"):
            provider = XiaomiProvider(api_key="test-key")
            assert "xiaomimimo" in provider._base_url

    @pytest.mark.asyncio
    async def test_generate_returns_response(self):
        """测试 generate 返回 LLMResponse"""
        mock_content = MagicMock()
        mock_content.text = "Hello from MIMO!"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 5

        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage
        mock_response.model = "mimo-v2.5-pro"

        with patch("src.llm.xiaomi_provider.anthropic") as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.AsyncAnthropic.return_value = mock_client

            provider = XiaomiProvider(api_key="test-key")
            result = await provider.generate([{"role": "user", "content": "hi"}])

            assert isinstance(result, LLMResponse)
            assert result.content == "Hello from MIMO!"
            assert result.provider == "xiaomi"
            assert result.usage.prompt_tokens == 10
            assert result.usage.completion_tokens == 5

    @pytest.mark.asyncio
    async def test_generate_separates_system_prompt(self):
        """测试 system 消息被提取为单独参数"""
        mock_content = MagicMock()
        mock_content.text = "ok"
        mock_usage = MagicMock()
        mock_usage.input_tokens = 5
        mock_usage.output_tokens = 2
        mock_response = MagicMock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage
        mock_response.model = "mimo-v2.5-pro"

        with patch("src.llm.xiaomi_provider.anthropic") as mock_anthropic:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic.AsyncAnthropic.return_value = mock_client

            provider = XiaomiProvider(api_key="test-key")
            messages = [
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "hi"},
            ]
            await provider.generate(messages)

            call_args = mock_client.messages.create.call_args
            # system 应该作为单独参数传入
            assert call_args.kwargs.get("system") == "You are helpful"
            # messages 中不应该包含 system
            sent_messages = call_args.kwargs.get("messages", [])
            assert all(m["role"] != "system" for m in sent_messages)

    @pytest.mark.asyncio
    async def test_generate_empty_messages_raises(self):
        """测试空消息列表"""
        with patch("src.llm.xiaomi_provider.anthropic"):
            provider = XiaomiProvider(api_key="test-key")
            with pytest.raises(ValueError, match="Messages cannot be empty"):
                await provider.generate([])
