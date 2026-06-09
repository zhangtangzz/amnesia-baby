import pytest
from src.memory.context import ContextBuilder
from src.memory.models import MemoryItem


class TestContextBuilder:
    """ContextBuilder 测试"""

    @pytest.fixture
    def builder(self):
        """创建 builder 实例"""
        return ContextBuilder()

    def test_builder_initialization(self, builder):
        """测试 builder 初始化"""
        assert builder is not None
        assert hasattr(builder, 'build')

    def test_build_context(self, builder):
        """测试构建上下文"""
        # 创建记忆
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon"),
            MemoryItem(content="用户喜欢火星计划", character_id="elon"),
        ]
        
        # 构建上下文
        current_message = "你为什么喜欢SpaceX？"
        context = builder.build(memories, current_message)
        
        # 验证结果
        assert isinstance(context, list)
        assert len(context) > 0
        assert any("SpaceX" in c for c in context)

    def test_build_context_empty_memories(self, builder):
        """测试构建空记忆上下文"""
        current_message = "你好"
        context = builder.build([], current_message)
        
        # 验证结果
        assert isinstance(context, list)
        assert len(context) > 0

    def test_build_context_with_limit(self, builder):
        """测试限制上下文数量"""
        # 创建多个记忆
        memories = [MemoryItem(content=f"记忆{i}", character_id="elon") for i in range(10)]
        
        # 构建上下文
        current_message = "你好"
        context = builder.build(memories, current_message, max_context=3)
        
        # 验证结果（3条记忆 + 1条当前消息 = 4）
        assert len(context) == 4

    def test_build_context_format(self, builder):
        """测试上下文格式"""
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon"),
        ]
        
        current_message = "你为什么喜欢SpaceX？"
        context = builder.build(memories, current_message)
        
        # 验证格式
        assert isinstance(context, list)
        for item in context:
            assert isinstance(item, str)
