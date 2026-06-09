import pytest
from src.memory.service import MemoryService
from src.memory.models import MemoryItem


class TestMemoryService:
    """MemoryService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return MemoryService()

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'add_memory')
        assert hasattr(service, 'get_context')

    def test_add_memory(self, service):
        """测试添加记忆"""
        service.add_memory(
            character_id="elon",
            content="我喜欢SpaceX",
            memory_type="conversation",
            importance=0.8,
        )
        
        # 验证记忆被添加
        context = service.get_context("elon", "SpaceX")
        assert len(context) > 0

    def test_get_context(self, service):
        """测试获取上下文"""
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
        context = service.get_context("elon", "SpaceX", max_context=5)
        
        # 验证结果
        assert isinstance(context, list)
        assert len(context) > 0

    def test_get_context_empty(self, service):
        """测试获取空上下文"""
        context = service.get_context("elon", "test", max_context=5)
        assert isinstance(context, list)
        assert len(context) > 0

    def test_consolidate_memories(self, service):
        """测试巩固记忆"""
        # 添加短期记忆
        for i in range(15):
            service.add_memory(
                character_id="elon",
                content=f"消息{i}",
                memory_type="conversation",
                importance=0.5 + i * 0.03,
            )
        
        # 巩固记忆
        service.consolidate_memories("elon")
        
        # 验证长期记忆
        assert service.long_term_memory.count() > 0
