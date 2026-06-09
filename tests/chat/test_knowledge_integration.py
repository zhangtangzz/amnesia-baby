"""
知识库 ↔ 对话 集成测试
"""
import pytest
from src.chat.knowledge_loader import KnowledgeLoader
from src.knowledge.store import KnowledgeStore
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeIntegration:
    """知识库与对话集成测试"""

    @pytest.mark.asyncio
    async def test_loader_reads_from_store(self):
        """测试知识加载器从知识存储读取数据"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        # 存入知识
        kb = KnowledgeBase(
            character_id="test_char",
            profile=KnowledgeProfile(name="测试角色", occupation="科学家"),
            facts=[
                Fact(fact="毕业于MIT", category="education", confidence=0.9),
                Fact(fact="研究量子物理", category="career", confidence=0.85),
            ],
        )
        await store.save("test_char", kb)

        # 加载器应该能读到
        data = await loader.load("test_char")
        assert data["character_id"] == "test_char"
        assert len(data["knowledge"]) >= 2

    @pytest.mark.asyncio
    async def test_loader_fallback_to_mock(self):
        """测试无存储数据时回退到 mock"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        # 没有存入数据，加载 "elon" 应回退到 mock
        data = await loader.load("elon")
        assert data["character_id"] == "elon"
        assert len(data["knowledge"]) > 0

    @pytest.mark.asyncio
    async def test_loader_unknown_character_returns_empty(self):
        """测试未知角色返回空知识"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        data = await loader.load("unknown_char")
        assert data["character_id"] == "unknown_char"
        assert data["knowledge"] == []

    @pytest.mark.asyncio
    async def test_shared_store_between_service_and_loader(self):
        """测试知识服务和加载器共享同一个存储"""
        store = KnowledgeStore()
        loader = KnowledgeLoader(store=store)

        # 直接存入
        kb = KnowledgeBase(
            character_id="shared_test",
            profile=KnowledgeProfile(name="共享测试"),
            facts=[Fact(fact="喜欢编程", category="interest", confidence=0.8)],
        )
        await store.save("shared_test", kb)

        # 加载器能读到
        data = await loader.load("shared_test")
        assert any("编程" in k["content"] for k in data["knowledge"])
