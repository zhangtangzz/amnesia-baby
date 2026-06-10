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


class TestContextBuilderSummary:
    """build_with_summary 测试"""

    @pytest.fixture
    def builder(self):
        return ContextBuilder()

    def test_build_with_summary_basic(self, builder):
        """测试带摘要的上下文构建"""
        memories = [
            MemoryItem(content="用户喜欢SpaceX", character_id="elon"),
            MemoryItem(content="用户喜欢火星计划", character_id="elon"),
        ]
        context = builder.build_with_summary(memories, "你好", max_context=5)
        assert isinstance(context, list)
        assert len(context) == 2  # summary + current message
        assert "相关记忆" in context[0]
        assert "你好" in context[1]

    def test_build_with_summary_contains_all_memories(self, builder):
        """测试摘要包含所有记忆内容"""
        memories = [
            MemoryItem(content="喜欢SpaceX", character_id="elon"),
            MemoryItem(content="住在美国", character_id="elon"),
        ]
        context = builder.build_with_summary(memories, "test", max_context=10)
        summary = context[0]
        assert "SpaceX" in summary
        assert "美国" in summary

    def test_build_with_summary_empty_memories(self, builder):
        """测试空记忆的摘要构建"""
        context = builder.build_with_summary([], "你好", max_context=5)
        assert isinstance(context, list)
        # 空记忆时只有当前消息
        assert len(context) == 1
        assert context[0] == "你好"

    def test_summarize_memories_empty(self, builder):
        """测试空记忆摘要"""
        result = builder._summarize_memories([])
        assert result == ""

    def test_summarize_memories_single(self, builder):
        """测试单条记忆摘要"""
        memories = [MemoryItem(content="喜欢SpaceX", character_id="elon")]
        result = builder._summarize_memories(memories)
        assert "相关记忆" in result
        assert "SpaceX" in result

    def test_summarize_memories_multiple(self, builder):
        """测试多条记忆摘要"""
        memories = [
            MemoryItem(content="喜欢SpaceX", character_id="elon"),
            MemoryItem(content="住在美国", character_id="elon"),
            MemoryItem(content="创办了Tesla", character_id="elon"),
        ]
        result = builder._summarize_memories(memories)
        assert "SpaceX" in result
        assert "美国" in result
        assert "Tesla" in result
        # 多条记忆用分号连接
        assert "；" in result
