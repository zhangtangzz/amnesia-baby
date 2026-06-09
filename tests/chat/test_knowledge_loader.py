"""
KnowledgeLoader 测试
"""

import pytest
from src.chat.knowledge_loader import KnowledgeLoader
from src.knowledge.store import KnowledgeStore
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeLoader:
    """KnowledgeLoader 测试"""

    @pytest.fixture
    def loader(self):
        """创建 loader 实例"""
        return KnowledgeLoader()

    def test_loader_initialization(self, loader):
        """测试 loader 初始化"""
        assert loader is not None
        assert hasattr(loader, 'load')

    @pytest.mark.asyncio
    async def test_load_returns_knowledge(self):
        """测试从 store 加载返回知识数据"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        # 存入知识
        kb = KnowledgeBase(
            character_id="elon",
            profile=KnowledgeProfile(name="Elon Musk"),
            facts=[Fact(fact="创业让我能够实现那些看似不可能的想法", category="创业", confidence=0.9)],
        )
        await store.save("elon", kb)

        result = await loader.load("elon")
        assert isinstance(result, dict)
        assert "character_id" in result
        assert "knowledge" in result
        assert isinstance(result["knowledge"], list)

    @pytest.mark.asyncio
    async def test_load_knowledge_list(self):
        """测试加载知识列表"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        kb = KnowledgeBase(
            character_id="elon",
            profile=KnowledgeProfile(name="Elon Musk"),
            facts=[
                Fact(fact="创业让我能够实现那些看似不可能的想法", category="创业", confidence=0.9),
                Fact(fact="技术是改变世界的力量", category="技术", confidence=0.85),
            ],
        )
        await store.save("elon", kb)

        result = await loader.load("elon")
        knowledge = result["knowledge"]
        assert len(knowledge) >= 2

    @pytest.mark.asyncio
    async def test_load_empty_knowledge(self):
        """测试未知角色回退到 mock（elon 有 mock 数据）"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        # elon 有 mock 数据，应该回退
        result = await loader.load("elon")
        assert len(result["knowledge"]) > 0

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self):
        """测试完全未知角色返回空知识"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        result = await loader.load("nonexistent")
        assert result["knowledge"] == []

    @pytest.mark.asyncio
    async def test_load_from_store_overrides_mock(self):
        """测试 store 数据优先于 mock"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        kb = KnowledgeBase(
            character_id="elon",
            profile=KnowledgeProfile(name="自定义角色"),
            facts=[Fact(fact="自定义知识", category="custom", confidence=0.9)],
        )
        await store.save("elon", kb)

        result = await loader.load("elon")
        # 应该返回 store 数据而非 mock
        assert any("自定义" in k["content"] for k in result["knowledge"])