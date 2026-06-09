"""
LLMService 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.llm_service import LLMService


class TestLLMService:
    """LLMService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        with patch('src.chat.llm_service.openai.AsyncOpenAI') as mock_client:
            mock_client.return_value = MagicMock()
            service = LLMService()
            return service

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'generate')

    @pytest.mark.asyncio
    async def test_generate_returns_response(self, service):
        """测试生成返回响应"""
        prompt = "你为什么喜欢创业？"

        # 模拟 LLM 响应
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "创业让我能够实现那些看似不可能的想法"

        with patch.object(service, '_call_llm', return_value=mock_response):
            result = await service.generate(prompt)
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_generate_with_context(self, service):
        """测试生成带上下文"""
        prompt = "你为什么喜欢创业？"
        context = "Elon Musk"

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "创业让我能够实现那些看似不可能的想法"

        with patch.object(service, '_call_llm', return_value=mock_response):
            result = await service.generate(prompt, context=context)
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_generate_empty_prompt(self, service):
        """测试生成空 prompt"""
        with pytest.raises(ValueError):
            await service.generate("")

    @pytest.mark.asyncio
    async def test_generate_handles_error(self, service):
        """测试生成处理错误"""
        prompt = "你为什么喜欢创业？"

        with patch.object(service, '_call_llm', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                await service.generate(prompt)