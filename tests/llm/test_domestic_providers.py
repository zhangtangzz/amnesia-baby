"""
国产 LLM 提供商测试（DeepSeek / Qwen）
"""
import pytest
from unittest.mock import patch
from src.llm.deepseek_provider import DeepSeekProvider
from src.llm.qwen_provider import QwenProvider


class TestDeepSeekProvider:
    """DeepSeekProvider 测试"""

    def test_provider_name(self):
        """测试提供商名称"""
        with patch("src.llm.openai_provider.openai"):
            provider = DeepSeekProvider(api_key="test-key")
            assert provider.provider_name == "deepseek"

    def test_default_model(self):
        """测试默认模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = DeepSeekProvider(api_key="test-key")
            assert provider.default_model == "deepseek-chat"

    def test_custom_model(self):
        """测试自定义模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = DeepSeekProvider(api_key="test-key", model="deepseek-coder")
            assert provider.default_model == "deepseek-coder"

    def test_default_base_url(self):
        """测试默认 base_url"""
        with patch("src.llm.openai_provider.openai"):
            provider = DeepSeekProvider(api_key="test-key")
            assert "deepseek" in provider._base_url

    def test_inherits_openai_provider(self):
        """测试继承 OpenAIProvider"""
        from src.llm.openai_provider import OpenAIProvider
        assert issubclass(DeepSeekProvider, OpenAIProvider)


class TestQwenProvider:
    """QwenProvider 测试"""

    def test_provider_name(self):
        """测试提供商名称"""
        with patch("src.llm.openai_provider.openai"):
            provider = QwenProvider(api_key="test-key")
            assert provider.provider_name == "qwen"

    def test_default_model(self):
        """测试默认模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = QwenProvider(api_key="test-key")
            assert provider.default_model == "qwen-turbo"

    def test_custom_model(self):
        """测试自定义模型"""
        with patch("src.llm.openai_provider.openai"):
            provider = QwenProvider(api_key="test-key", model="qwen-plus")
            assert provider.default_model == "qwen-plus"

    def test_default_base_url(self):
        """测试默认 base_url"""
        with patch("src.llm.openai_provider.openai"):
            provider = QwenProvider(api_key="test-key")
            assert "dashscope" in provider._base_url or "qwen" in provider._base_url

    def test_inherits_openai_provider(self):
        """测试继承 OpenAIProvider"""
        from src.llm.openai_provider import OpenAIProvider
        assert issubclass(QwenProvider, OpenAIProvider)
