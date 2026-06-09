"""
LLM 数据模型测试
"""
import pytest
from src.llm.models import TokenUsage, LLMResponse


class TestTokenUsage:
    """TokenUsage 测试"""

    def test_creation(self):
        """测试创建 TokenUsage"""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        assert usage.prompt_tokens == 100
        assert usage.completion_tokens == 50
        assert usage.total_tokens == 150

    def test_default_values(self):
        """测试默认值"""
        usage = TokenUsage()
        assert usage.prompt_tokens == 0
        assert usage.completion_tokens == 0
        assert usage.total_tokens == 0

    def test_auto_total(self):
        """测试自动计算 total"""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        assert usage.total_tokens == 150

    def test_serialization(self):
        """测试序列化"""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        data = usage.model_dump()
        assert data["prompt_tokens"] == 100
        assert data["completion_tokens"] == 50
        assert data["total_tokens"] == 150


class TestLLMResponse:
    """LLMResponse 测试"""

    def test_creation(self):
        """测试创建 LLMResponse"""
        response = LLMResponse(
            content="Hello",
            provider="openai",
            model="gpt-3.5-turbo",
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )
        assert response.content == "Hello"
        assert response.provider == "openai"
        assert response.model == "gpt-3.5-turbo"
        assert response.usage.total_tokens == 15

    def test_default_usage(self):
        """测试默认 usage"""
        response = LLMResponse(content="Hi", provider="openai", model="gpt-3.5-turbo")
        assert response.usage.total_tokens == 0

    def test_serialization(self):
        """测试序列化"""
        response = LLMResponse(
            content="Hi",
            provider="openai",
            model="gpt-3.5-turbo",
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )
        data = response.model_dump()
        assert data["content"] == "Hi"
        assert data["provider"] == "openai"
        assert "usage" in data
