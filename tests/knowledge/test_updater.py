import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.updater import KnowledgeUpdater
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeUpdater:
    """KnowledgeUpdater 测试"""

    @pytest.fixture
    def updater(self):
        """创建 updater 实例"""
        return KnowledgeUpdater()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", occupation="工程师"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[
                Fact(fact="毕业于清华大学", category="education", confidence=0.92),
            ],
            timeline=[],
            evidence=[],
        )

    def test_updater_initialization(self, updater):
        """测试 updater 初始化"""
        assert updater is not None
        assert hasattr(updater, 'update_profile')
        assert hasattr(updater, 'add_fact')

    def test_update_profile(self, updater, mock_knowledge_base):
        """测试更新基础信息"""
        new_data = {"occupation": "创业者"}
        updater.update_profile(mock_knowledge_base, new_data)
        assert mock_knowledge_base.profile.occupation == "创业者"

    def test_add_fact(self, updater, mock_knowledge_base):
        """测试添加事实"""
        fact = Fact(fact="创立某科技公司", category="career", confidence=0.94)
        updater.add_fact(mock_knowledge_base, fact)
        assert len(mock_knowledge_base.facts) == 2

    def test_update_fact_confidence(self, updater, mock_knowledge_base):
        """测试更新事实置信度"""
        fact_index = 0
        new_confidence = 0.98
        updater.update_fact_confidence(mock_knowledge_base, fact_index, new_confidence)
        assert mock_knowledge_base.facts[0].confidence == 0.98

    def test_update_fact_confidence_invalid_index(self, updater, mock_knowledge_base):
        """测试更新事实置信度无效索引"""
        fact_index = 999
        new_confidence = 0.98
        with pytest.raises(IndexError):
            updater.update_fact_confidence(mock_knowledge_base, fact_index, new_confidence)
