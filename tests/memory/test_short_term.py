import pytest
from src.memory.short_term import ShortTermMemory
from src.memory.models import MemoryItem


class TestShortTermMemory:
    """ShortTermMemory 测试"""

    @pytest.fixture
    def memory(self):
        """创建 memory 实例"""
        return ShortTermMemory(max_size=10)

    def test_memory_initialization(self, memory):
        """测试 memory 初始化"""
        assert memory is not None
        assert hasattr(memory, 'add')
        assert hasattr(memory, 'get_recent')

    def test_add_memory(self, memory):
        """测试添加记忆"""
        item = MemoryItem(
            content="我喜欢SpaceX",
            character_id="elon",
        )
        memory.add(item)
        assert memory.count() == 1

    def test_get_recent_memories(self, memory):
        """测试获取最近记忆"""
        # 添加多个记忆
        for i in range(5):
            item = MemoryItem(
                content=f"消息{i}",
                character_id="elon",
            )
            memory.add(item)
        
        # 获取最近3条
        recent = memory.get_recent(3)
        assert len(recent) == 3
        assert recent[0].content == "消息2"
        assert recent[2].content == "消息4"

    def test_get_recent_empty(self, memory):
        """测试获取空记忆"""
        recent = memory.get_recent(3)
        assert len(recent) == 0

    def test_memory_max_size(self, memory):
        """测试记忆最大容量"""
        # 添加超过最大容量的记忆
        for i in range(15):
            item = MemoryItem(
                content=f"消息{i}",
                character_id="elon",
            )
            memory.add(item)
        
        # 验证不超过最大容量
        assert memory.count() == 10

    def test_clear_memory(self, memory):
        """测试清空记忆"""
        item = MemoryItem(
            content="测试内容",
            character_id="elon",
        )
        memory.add(item)
        
        memory.clear()
        assert memory.count() == 0
