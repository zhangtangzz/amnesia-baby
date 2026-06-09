import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.extractor import KnowledgeExtractor
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeExtractor:
    """KnowledgeExtractor 测试"""

    @pytest.fixture
    def extractor(self):
        """创建 extractor 实例"""
        return KnowledgeExtractor()

    def test_extractor_initialization(self, extractor):
        """测试 extractor 初始化"""
        assert extractor is not None
        assert hasattr(extractor, 'extract')

    @pytest.mark.asyncio
    async def test_extract_returns_knowledge_base(self, extractor):
        """测试提取返回知识库"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_extract_profile(self, extractor):
        """测试提取基础信息"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert result.profile.name == "张三"
        assert result.profile.education == "清华大学"
        assert result.profile.occupation == "创业者"

    @pytest.mark.asyncio
    async def test_extract_facts(self, extractor):
        """测试提取事实"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert len(result.facts) > 0
        for fact in result.facts:
            assert fact.fact is not None
            assert fact.category is not None
            assert 0.0 <= fact.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_extract_evidence(self, extractor):
        """测试提取证据"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert len(result.evidence) > 0
        for evidence in result.evidence:
            assert evidence.source_type is not None
            assert evidence.source_name is not None
            assert evidence.content is not None

    @pytest.mark.asyncio
    async def test_extract_empty_text(self, extractor):
        """测试提取空文本"""
        text = ""
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert isinstance(result, KnowledgeBase)
