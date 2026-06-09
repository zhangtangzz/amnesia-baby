import pytest
from src.memory.models import MemoryItem


class TestMemoryModels:
    """记忆数据模型测试"""

    def test_memory_item_creation(self):
        """测试记忆项创建"""
        item = MemoryItem(
            content="我喜欢SpaceX",
            character_id="elon",
            memory_type="conversation",
            importance=0.8,
        )
        assert item.content == "我喜欢SpaceX"
        assert item.character_id == "elon"
        assert item.memory_type == "conversation"
        assert item.importance == 0.8

    def test_memory_item_default_values(self):
        """测试记忆项默认值"""
        item = MemoryItem(
            content="测试内容",
            character_id="test_char",
        )
        assert item.memory_type == "conversation"
        assert item.importance == 0.5
        assert item.metadata == {}

    def test_memory_item_importance_validation(self):
        """测试重要度验证"""
        item = MemoryItem(
            content="测试内容",
            character_id="test_char",
            importance=0.95,
        )
        assert item.importance == 0.95
