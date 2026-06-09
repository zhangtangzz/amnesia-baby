import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.service import KnowledgeService
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeService:
    """KnowledgeService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return KnowledgeService()

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

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'process')
        assert hasattr(service, 'query')

    @pytest.mark.asyncio
    async def test_process_returns_knowledge_base(self, service):
        """测试处理返回知识库"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await service.process(text, source)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_process_saves_to_store(self, service):
        """测试处理保存到存储"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"
        character_id = "test_char"

        result = await service.process(text, source, character_id)
        loaded = await service.load(character_id)
        assert loaded is not None
        assert loaded.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_query_facts(self, service, mock_knowledge_base):
        """测试查询事实"""
        character_id = "test_char"
        await service.save(character_id, mock_knowledge_base)

        results = await service.query_facts(character_id, "张三")
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, service):
        """测试加载不存在的角色"""
        result = await service.load("nonexistent")
        assert result is None
