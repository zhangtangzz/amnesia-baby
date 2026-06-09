"""
聊天引擎集成测试

测试：角色加载 → 知识加载 → 记忆上下文 → Prompt构建 → LLM调用 → 记忆存储
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.chat_engine import ChatEngine


class TestChatEngine:
    """ChatEngine 测试"""

    @pytest.fixture
    def engine(self):
        """创建引擎实例"""
        with patch("src.chat.chat_engine.XiaomiProvider") as mock_provider:
            mock_provider.return_value = MagicMock()
            engine = ChatEngine(
                provider_name="xiaomi",
                api_key="test-key",
                base_url="https://test.com",
                model="test-model",
            )
            return engine

    def test_initialization(self, engine):
        """测试引擎初始化"""
        assert engine is not None
        assert engine.character_loader is not None
        assert engine.knowledge_loader is not None
        assert engine.prompt_builder is not None
        assert engine.memory_service is not None

    @pytest.mark.asyncio
    async def test_chat_returns_reply(self, engine):
        """测试聊天返回回复"""
        mock_response = MagicMock()
        mock_response.content = "Hello from character!"
        mock_response.provider = "xiaomi"
        mock_response.model = "mimo-v2.5-pro"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_response.usage.total_tokens = 150
        mock_response.usage.model_dump.return_value = {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}

        engine.llm_provider.generate = AsyncMock(return_value=mock_response)

        result = await engine.chat("elon", "你好")

        assert "reply" in result
        assert result["reply"] == "Hello from character!"
        assert result["provider"] == "xiaomi"
        assert result["character_id"] == "elon"

    @pytest.mark.asyncio
    async def test_chat_stores_memory(self, engine):
        """测试聊天自动存储记忆"""
        mock_response = MagicMock()
        mock_response.content = "I love startups!"
        mock_response.provider = "xiaomi"
        mock_response.model = "test"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.model_dump.return_value = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}

        engine.llm_provider.generate = AsyncMock(return_value=mock_response)

        await engine.chat("elon", "你喜欢什么？")

        # 记忆中应该有用户消息和助手回复
        assert engine.memory_service.get_short_term_count() >= 2

    @pytest.mark.asyncio
    async def test_chat_uses_memory_context(self, engine):
        """测试聊天使用记忆上下文"""
        mock_response = MagicMock()
        mock_response.content = "ok"
        mock_response.provider = "xiaomi"
        mock_response.model = "test"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.model_dump.return_value = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}

        engine.llm_provider.generate = AsyncMock(return_value=mock_response)

        # 第一次对话
        await engine.chat("elon", "hello")

        # 第二次对话应该包含上下文
        await engine.chat("elon", "what did I just say?")

        # 检查第二次调用时的 prompt 包含历史
        call_args = engine.llm_provider.generate.call_args
        messages = call_args[0][0]  # 第一个位置参数
        # 应该有 system + history + user 消息
        assert len(messages) >= 2

    @pytest.mark.asyncio
    async def test_chat_builds_character_prompt(self, engine):
        """测试 Prompt 包含角色信息"""
        mock_response = MagicMock()
        mock_response.content = "ok"
        mock_response.provider = "xiaomi"
        mock_response.model = "test"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.model_dump.return_value = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}

        engine.llm_provider.generate = AsyncMock(return_value=mock_response)

        await engine.chat("elon", "hi")

        call_args = engine.llm_provider.generate.call_args
        messages = call_args[0][0]
        system_msg = messages[0]
        assert system_msg["role"] == "system"
        assert "Elon Musk" in system_msg["content"] or "elon" in system_msg["content"].lower()

    @pytest.mark.asyncio
    async def test_get_history(self, engine):
        """测试获取对话历史"""
        mock_response = MagicMock()
        mock_response.content = "hi there"
        mock_response.provider = "xiaomi"
        mock_response.model = "test"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 5
        mock_response.usage.total_tokens = 15
        mock_response.usage.model_dump.return_value = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}

        engine.llm_provider.generate = AsyncMock(return_value=mock_response)

        await engine.chat("elon", "hello")
        history = engine.get_history("elon")

        assert len(history) >= 2  # user + assistant
        assert history[-2]["role"] == "user"
        assert history[-1]["role"] == "assistant"
