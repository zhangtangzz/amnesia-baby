import pytest
from src.memory.long_term import LongTermMemory
from src.memory.models import MemoryItem


class TestLongTermMemory:
    """LongTermMemory 测试"""

    @pytest.fixture
    def memory(self):
        """创建 memory 实例"""
        return LongTermMemory()

    def test_memory_initialization(self, memory):
        """测试 memory 初始化"""
        assert memory is not None
        assert hasattr(memory, 'add')
        assert hasattr(memory, 'search')

    def test_add_memory(self, memory):
        """测试添加记忆"""
        item = MemoryItem(
            content="用户对SpaceX感兴趣",
            character_id="elon",
            importance=0.8,
        )
        memory.add(item)
        assert memory.count() == 1

    def test_search_memories(self, memory):
        """测试搜索记忆"""
        # 添加多个记忆
        items = [
            MemoryItem(content="用户对SpaceX感兴趣", character_id="elon", importance=0.8),
            MemoryItem(content="用户喜欢火星计划", character_id="elon", importance=0.9),
            MemoryItem(content="用户不喜欢传统汽车", character_id="elon", importance=0.6),
        ]
        for item in items:
            memory.add(item)
        
        # 搜索
        results = memory.search("SpaceX", top_k=2)
        assert len(results) > 0
        assert any("SpaceX" in r.content for r in results)

    def test_search_empty_memory(self, memory):
        """测试搜索空记忆"""
        results = memory.search("test", top_k=1)
        assert len(results) == 0

    def test_get_by_importance(self, memory):
        """测试按重要度获取记忆"""
        # 添加多个记忆
        items = [
            MemoryItem(content="低重要度", character_id="elon", importance=0.3),
            MemoryItem(content="中重要度", character_id="elon", importance=0.5),
            MemoryItem(content="高重要度", character_id="elon", importance=0.9),
        ]
        for item in items:
            memory.add(item)
        
        # 获取高重要度记忆
        results = memory.get_by_importance(min_importance=0.7)
        assert len(results) == 1
        assert results[0].content == "高重要度"

    def test_delete_memory(self, memory):
        """测试删除记忆"""
        item = MemoryItem(
            content="测试内容",
            character_id="elon",
        )
        memory.add(item)
        
        memory.delete(item)
        assert memory.count() == 0
