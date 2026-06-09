import pytest
from src.memory.retriever import MemoryRetriever
from src.memory.models import MemoryItem


class TestMemoryRetriever:
    """MemoryRetriever 测试"""

    @pytest.fixture
    def retriever(self):
        """创建 retriever 实例"""
        return MemoryRetriever()

    def test_retriever_initialization(self, retriever):
        """测试 retriever 初始化"""
        assert retriever is not None
        assert hasattr(retriever, 'retrieve')

    def test_retrieve_memories(self, retriever):
        """测试检索记忆"""
        # 创建记忆
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon", importance=0.8),
            MemoryItem(content="用户喜欢火星计划", character_id="elon", importance=0.9),
            MemoryItem(content="用户不喜欢传统汽车", character_id="elon", importance=0.6),
        ]
        
        # 检索记忆
        query = "SpaceX"
        results = retriever.retrieve(memories, query, top_k=2)
        
        # 验证结果
        assert len(results) > 0
        assert any("SpaceX" in r.content for r in results)

    def test_retrieve_empty_memories(self, retriever):
        """测试检索空记忆"""
        query = "test"
        results = retriever.retrieve([], query, top_k=1)
        assert len(results) == 0

    def test_retrieve_with_importance(self, retriever):
        """测试按重要度检索记忆"""
        memories = [
            MemoryItem(content="低重要度", character_id="elon", importance=0.3),
            MemoryItem(content="高重要度", character_id="elon", importance=0.9),
        ]
        
        query = "重要度"
        results = retriever.retrieve(memories, query, min_importance=0.5)
        
        # 验证只返回高重要度记忆
        assert len(results) == 1
        assert results[0].content == "高重要度"

    def test_retrieve_no_match(self, retriever):
        """测试无匹配检索"""
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon"),
        ]
        
        query = "不存在的内容"
        results = retriever.retrieve(memories, query, top_k=1)
        assert len(results) == 0
