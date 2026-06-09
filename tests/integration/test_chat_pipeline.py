"""
聊天流水线集成测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.chat_agent import ChatAgent
from src.chat.character_loader import CharacterLoader
from src.chat.knowledge_loader import KnowledgeLoader
from src.chat.prompt_builder import PromptBuilder
from src.chat.llm_service import LLMService


class TestChatPipeline:
    """聊天流水线集成测试"""

    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        with patch('src.chat.chat_agent.ChatService') as mock_service:
            mock_service.return_value = MagicMock()
            agent = ChatAgent()
            return agent

    @pytest.mark.asyncio
    async def test_full_pipeline(self, agent):
        """测试完整流水线"""
        # 模拟数据
        mock_character = {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": MagicMock(),
            "big_five": MagicMock(),
            "enneagram": MagicMock(),
        }
        mock_knowledge = {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
            ],
        }
        mock_reply = "创业让我能够实现那些看似不可能的想法"

        # 模拟依赖
        agent.chat_service.character_loader.load = AsyncMock(return_value=mock_character)
        agent.chat_service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        agent.chat_service.prompt_builder.build = MagicMock(return_value="test prompt")
        agent.chat_service.llm_service.generate = AsyncMock(return_value=mock_reply)
        agent.chat_service.chat = AsyncMock(return_value={"reply": mock_reply})

        # 执行测试
        result = await agent.chat("elon", "你为什么喜欢创业？")

        # 验证结果
        assert "reply" in result
        assert result["reply"] == mock_reply

        # 验证调用
        agent.chat_service.chat.assert_called_once_with("elon", "你为什么喜欢创业？")