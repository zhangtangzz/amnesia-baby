"""
ChatAgent 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.chat_agent import ChatAgent
from src.chat.chat_service import ChatService


class TestChatAgent:
    """ChatAgent 测试"""

    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        with patch('src.chat.chat_agent.ChatService') as mock_service:
            mock_service.return_value = MagicMock()
            agent = ChatAgent()
            return agent

    @pytest.fixture
    def mock_reply(self):
        """模拟回复"""
        return {"reply": "创业让我能够实现那些看似不可能的想法"}

    def test_agent_initialization(self, agent):
        """测试 agent 初始化"""
        assert agent is not None
        assert hasattr(agent, 'chat')

    @pytest.mark.asyncio
    async def test_chat_returns_reply(self, agent, mock_reply):
        """测试聊天返回回复"""
        agent.chat_service.chat = AsyncMock(return_value=mock_reply)

        result = await agent.chat("elon", "你为什么喜欢创业？")
        assert isinstance(result, dict)
        assert "reply" in result
        assert result["reply"] == mock_reply["reply"]

    @pytest.mark.asyncio
    async def test_chat_with_character_id(self, agent, mock_reply):
        """测试聊天带角色ID"""
        agent.chat_service.chat = AsyncMock(return_value=mock_reply)

        result = await agent.chat("elon", "你为什么喜欢创业？")
        agent.chat_service.chat.assert_called_once_with("elon", "你为什么喜欢创业？")

    @pytest.mark.asyncio
    async def test_chat_handles_error(self, agent):
        """测试聊天处理错误"""
        agent.chat_service.chat = AsyncMock(side_effect=Exception("Chat Error"))

        with pytest.raises(Exception):
            await agent.chat("elon", "test")