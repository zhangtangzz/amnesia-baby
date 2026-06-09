import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.service import KnowledgeService
from src.knowledge.models import KnowledgeBase


class TestKnowledgePipeline:
    """知识库流水线集成测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return KnowledgeService()

    @pytest.mark.asyncio
    async def test_full_pipeline(self, service):
        """测试完整流水线"""
        # 输入文本
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"
        character_id = "test_char"

        # 处理文本
        knowledge_base = await service.process(text, source, character_id)

        # 验证结果
        assert isinstance(knowledge_base, KnowledgeBase)
        assert knowledge_base.profile.name == "张三"
        assert knowledge_base.profile.education == "清华大学"
        assert knowledge_base.profile.occupation == "创业者"
        assert len(knowledge_base.facts) > 0
        assert len(knowledge_base.evidence) > 0

        # 查询知识
        facts = await service.query_facts(character_id, "清华")
        assert len(facts) > 0
        assert any("清华" in fact.fact for fact in facts)

        # 加载知识
        loaded = await service.load(character_id)
        assert loaded is not None
        assert loaded.profile.name == "张三"
