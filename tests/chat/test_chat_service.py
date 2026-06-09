"""
ChatService 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.chat_service import ChatService
from src.chat.character_loader import CharacterLoader
from src.chat.knowledge_loader import KnowledgeLoader
from src.chat.prompt_builder import PromptBuilder
from src.chat.llm_service import LLMService


class TestChatService:
    """ChatService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        with patch('src.chat.chat_service.LLMService') as mock_llm:
            mock_llm.return_value = MagicMock()
            service = ChatService()
            return service

    @pytest.fixture
    def mock_character(self):
        """模拟角色数据"""
        return {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": MagicMock(),
            "big_five": MagicMock(),
            "enneagram": MagicMock(),
        }

    @pytest.fixture
    def mock_knowledge(self):
        """模拟知识数据"""
        return {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
            ],
        }

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'chat')

    @pytest.mark.asyncio
    async def test_chat_returns_reply(self, service, mock_character, mock_knowledge):
        """测试聊天返回回复"""
        # 模拟依赖
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")

        result = await service.chat("elon", "你为什么喜欢创业？")
        assert isinstance(result, dict)
        assert "reply" in result
        assert result["reply"] == "test reply"

    @pytest.mark.asyncio
    async def test_chat_with_character_id(self, service, mock_character, mock_knowledge):
        """测试聊天带角色ID"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")

        result = await service.chat("elon", "你为什么喜欢创业？")
        service.character_loader.load.assert_called_once_with("elon")

    @pytest.mark.asyncio
    async def test_chat_with_message(self, service, mock_character, mock_knowledge):
        """测试聊天带消息"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")

        message = "你为什么喜欢创业？"
        result = await service.chat("elon", message)
        service.prompt_builder.build.assert_called_once_with(
            mock_character, mock_knowledge, message
        )

    @pytest.mark.asyncio
    async def test_chat_handles_character_not_found(self, service):
        """测试聊天处理角色不存在"""
        service.character_loader.load = AsyncMock(side_effect=ValueError("Character not found"))

        with pytest.raises(ValueError):
            await service.chat("nonexistent", "test")

    @pytest.mark.asyncio
    async def test_chat_handles_llm_error(self, service, mock_character, mock_knowledge):
        """测试聊天处理 LLM 错误"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(side_effect=Exception("LLM Error"))

        with pytest.raises(Exception):
            await service.chat("elon", "test")