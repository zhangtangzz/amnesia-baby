import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.query import KnowledgeQuery
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeQuery:
    """KnowledgeQuery 测试"""

    @pytest.fixture
    def query(self):
        """创建 query 实例"""
        return KnowledgeQuery()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", education="清华大学"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[
                Fact(fact="毕业于清华大学", category="education", confidence=0.92),
                Fact(fact="创立某科技公司", category="career", confidence=0.94),
            ],
            timeline=[],
            evidence=[],
        )

    def test_query_initialization(self, query):
        """测试 query 初始化"""
        assert query is not None
        assert hasattr(query, 'search_facts')

    def test_search_facts(self, query, mock_knowledge_base):
        """测试搜索事实"""
        keyword = "清华"
        results = query.search_facts(mock_knowledge_base, keyword)
        assert len(results) > 0
        assert any("清华" in fact.fact for fact in results)

    def test_search_facts_no_match(self, query, mock_knowledge_base):
        """测试搜索无匹配事实"""
        keyword = "不存在"
        results = query.search_facts(mock_knowledge_base, keyword)
        assert len(results) == 0

    def test_get_facts_by_category(self, query, mock_knowledge_base):
        """测试按类别获取事实"""
        category = "education"
        results = query.get_facts_by_category(mock_knowledge_base, category)
        assert len(results) > 0
        assert all(fact.category == category for fact in results)

    def test_get_facts_by_category_no_match(self, query, mock_knowledge_base):
        """测试按类别获取无匹配事实"""
        category = "不存在"
        results = query.get_facts_by_category(mock_knowledge_base, category)
        assert len(results) == 0

    def test_get_profile(self, query, mock_knowledge_base):
        """测试获取基础信息"""
        profile = query.get_profile(mock_knowledge_base)
        assert profile.name == "张三"
        assert profile.education == "清华大学"
