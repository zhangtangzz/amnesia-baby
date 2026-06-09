import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.store import KnowledgeStore
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeStore:
    """KnowledgeStore 测试"""

    @pytest.fixture
    def store(self):
        """创建 store 实例"""
        return KnowledgeStore()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", education="清华大学"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[],
            timeline=[],
            evidence=[],
        )

    def test_store_initialization(self, store):
        """测试 store 初始化"""
        assert store is not None
        assert hasattr(store, 'save')
        assert hasattr(store, 'load')

    @pytest.mark.asyncio
    async def test_save_knowledge_base(self, store, mock_knowledge_base):
        """测试保存知识库"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)
        # 验证保存成功（无异常）

    @pytest.mark.asyncio
    async def test_load_knowledge_base(self, store, mock_knowledge_base):
        """测试加载知识库"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)

        result = await store.load(character_id)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, store):
        """测试加载不存在的角色"""
        result = await store.load("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_save_and_load_consistency(self, store, mock_knowledge_base):
        """测试保存和加载一致性"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)

        result = await store.load(character_id)
        assert result.profile.name == mock_knowledge_base.profile.name
        assert result.profile.education == mock_knowledge_base.profile.education
