"""
LLM 提供商基类测试
"""
import pytest
from abc import ABC
from src.llm.base import LLMProvider
from src.llm.models import LLMResponse, TokenUsage


class TestLLMProvider:
    """LLMProvider 抽象基类测试"""

    def test_is_abstract(self):
        """测试 LLMProvider 是抽象类"""
        assert issubclass(LLMProvider, ABC)

    def test_cannot_instantiate(self):
        """测试不能直接实例化"""
        with pytest.raises(TypeError):
            LLMProvider()

    def test_concrete_implementation(self):
        """测试具体实现可以实例化"""

        class MockProvider(LLMProvider):
            @property
            def provider_name(self) -> str:
                return "mock"

            @property
            def default_model(self) -> str:
                return "mock-model"

            async def generate(self, messages, model=None, temperature=0.7, max_tokens=500):
                return LLMResponse(
                    content="test reply",
                    provider=self.provider_name,
                    model=model or self.default_model,
                )

        provider = MockProvider()
        assert provider.provider_name == "mock"
        assert provider.default_model == "mock-model"

    @pytest.mark.asyncio
    async def test_generate_interface(self):
        """测试 generate 接口"""

        class MockProvider(LLMProvider):
            @property
            def provider_name(self) -> str:
                return "mock"

            @property
            def default_model(self) -> str:
                return "mock-model"

            async def generate(self, messages, model=None, temperature=0.7, max_tokens=500):
                return LLMResponse(
                    content="test reply",
                    provider=self.provider_name,
                    model=model or self.default_model,
                    usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
                )

        provider = MockProvider()
        response = await provider.generate([{"role": "user", "content": "hi"}])
        assert response.content == "test reply"
        assert response.provider == "mock"
        assert response.usage.total_tokens == 15
