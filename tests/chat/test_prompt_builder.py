"""
PromptBuilder 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.prompt_builder import PromptBuilder
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestPromptBuilder:
    """PromptBuilder 测试"""
    
    @pytest.fixture
    def builder(self):
        """创建 builder 实例"""
        return PromptBuilder()
    
    @pytest.fixture
    def mock_character(self):
        """模拟角色数据"""
        return {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": PersonalityProfile(
                achievement_drive=0.9,
                curiosity=0.8,
                risk_preference=0.85,
            ),
            "big_five": BigFiveProfile(openness=0.8),
            "enneagram": EnneagramProfile(type8=0.4),
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
    
    def test_builder_initialization(self, builder):
        """测试 builder 初始化"""
        assert builder is not None
        assert hasattr(builder, 'build')
    
    def test_build_returns_prompt(self, builder, mock_character, mock_knowledge):
        """测试构建返回 prompt"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_build_includes_personality(self, builder, mock_character, mock_knowledge):
        """测试构建包含人格信息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert "Elon Musk" in result
        assert "成就驱动" in result or "achievement_drive" in result
    
    def test_build_includes_knowledge(self, builder, mock_character, mock_knowledge):
        """测试构建包含知识信息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert "创业" in result
        assert "创业让我能够实现那些看似不可能的想法" in result
    
    def test_build_includes_message(self, builder, mock_character, mock_knowledge):
        """测试构建包含用户消息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert message in result
    
    def test_build_empty_knowledge(self, builder, mock_character):
        """测试构建空知识"""
        empty_knowledge = {"character_id": "elon", "knowledge": []}
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, empty_knowledge, message)
        assert isinstance(result, str)
        assert len(result) > 0