import pytest
from src.memory.consolidator import MemoryConsolidator
from src.memory.models import MemoryItem


class TestMemoryConsolidator:
    """MemoryConsolidator 测试"""

    @pytest.fixture
    def consolidator(self):
        """创建 consolidator 实例"""
        return MemoryConsolidator()

    def test_consolidator_initialization(self, consolidator):
        """测试 consolidator 初始化"""
        assert consolidator is not None
        assert hasattr(consolidator, 'consolidate')

    def test_consolidate_memories(self, consolidator):
        """测试巩固记忆"""
        # 创建短期记忆
        short_term_memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon", importance=0.8),
            MemoryItem(content="用户喜欢火星计划", character_id="elon", importance=0.9),
            MemoryItem(content="用户不喜欢传统汽车", character_id="elon", importance=0.6),
        ]
        
        # 巩固记忆
        consolidated = consolidator.consolidate(short_term_memories)
        
        # 验证结果
        assert len(consolidated) > 0
        assert all(isinstance(m, MemoryItem) for m in consolidated)

    def test_consolidate_empty_memories(self, consolidator):
        """测试巩固空记忆"""
        consolidated = consolidator.consolidate([])
        assert len(consolidated) == 0

    def test_consolidate_high_importance(self, consolidator):
        """测试巩固高重要度记忆"""
        # 创建记忆
        memories = [
            MemoryItem(content="高重要度", character_id="elon", importance=0.9),
            MemoryItem(content="低重要度", character_id="elon", importance=0.1),
        ]
        
        # 巩固记忆
        consolidated = consolidator.consolidate(memories, min_importance=0.5)
        
        # 验证只保留高重要度记忆
        assert len(consolidated) == 1
        assert consolidated[0].content == "高重要度"

    def test_consolidate_merge_similar(self, consolidator):
        """测试合并相似记忆"""
        # 创建相似记忆
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon", importance=0.8),
            MemoryItem(content="用户对SpaceX感兴趣", character_id="elon", importance=0.7),
        ]
        
        # 巩固记忆
        consolidated = consolidator.consolidate(memories, merge_similar=True)
        
        # 验证合并结果
        assert len(consolidated) > 0
