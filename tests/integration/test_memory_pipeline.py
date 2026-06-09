import pytest
from src.memory.service import MemoryService


class TestMemoryPipeline:
    """记忆系统流水线集成测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return MemoryService()

    def test_full_pipeline(self, service):
        """测试完整流水线"""
        # 添加记忆
        service.add_memory(
            character_id="elon",
            content="用户喜欢SpaceX",
            memory_type="conversation",
            importance=0.8,
        )
        service.add_memory(
            character_id="elon",
            content="用户喜欢火星计划",
            memory_type="conversation",
            importance=0.9,
        )
        
        # 获取上下文
        context = service.get_context("elon", "你为什么喜欢SpaceX？", max_context=5)
        
        # 验证结果
        assert isinstance(context, list)
        assert len(context) > 0
        assert any("SpaceX" in c for c in context)
        
        # 巩固记忆
        service.consolidate_memories("elon")
        
        # 验证长期记忆
        assert service.get_long_term_count() > 0
        
        # 搜索长期记忆
        results = service.search_long_term("SpaceX", top_k=2)
        assert len(results) > 0
