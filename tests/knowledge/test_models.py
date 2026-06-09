import pytest
from pydantic import ValidationError
from src.knowledge.models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
)


class TestKnowledgeModels:
    """知识库数据模型测试"""

    def test_knowledge_profile_creation(self):
        """测试基础信息创建"""
        profile = KnowledgeProfile(
            name="张三",
            occupation="创业者",
            education="清华大学",
        )
        assert profile.name == "张三"
        assert profile.occupation == "创业者"
        assert profile.education == "清华大学"

    def test_relationship_creation(self):
        """测试人物关系创建"""
        rel = Relationship(
            name="李四",
            relationship="朋友",
            closeness=0.85,
            description="大学室友",
        )
        assert rel.name == "李四"
        assert rel.relationship == "朋友"
        assert rel.closeness == 0.85

    def test_event_creation(self):
        """测试重要事件创建"""
        event = Event(
            title="第一次创业失败",
            time="2019",
            impact=0.95,
        )
        assert event.title == "第一次创业失败"
        assert event.time == "2019"
        assert event.impact == 0.95

    def test_belief_creation(self):
        """测试观点体系创建"""
        belief = Belief(
            topic="创业",
            stance="支持",
            confidence=0.88,
        )
        assert belief.topic == "创业"
        assert belief.stance == "支持"
        assert belief.confidence == 0.88

    def test_fact_creation(self):
        """测试事实库创建"""
        fact = Fact(
            fact="创立某科技公司",
            category="career",
            confidence=0.94,
        )
        assert fact.fact == "创立某科技公司"
        assert fact.category == "career"
        assert fact.confidence == 0.94

    def test_timeline_creation(self):
        """测试人生时间轴创建"""
        timeline = Timeline(
            year="2020",
            events=["创业", "获得融资"],
        )
        assert timeline.year == "2020"
        assert len(timeline.events) == 2

    def test_evidence_creation(self):
        """测试证据库创建"""
        evidence = Evidence(
            source_type="video",
            source_name="人物采访",
            content="我从大学开始创业",
            confidence=0.91,
        )
        assert evidence.source_type == "video"
        assert evidence.source_name == "人物采访"
        assert evidence.content == "我从大学开始创业"

    def test_knowledge_base_creation(self):
        """测试知识库创建"""
        kb = KnowledgeBase(
            profile=KnowledgeProfile(name="张三"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[],
            timeline=[],
            evidence=[],
        )
        assert kb.profile.name == "张三"
        assert kb.relationships == []

    def test_relationship_closeness_validation(self):
        """测试关系亲密度验证"""
        with pytest.raises(ValidationError):
            Relationship(name="test", relationship="test", closeness=1.5)

    def test_event_impact_validation(self):
        """测试事件影响度验证"""
        with pytest.raises(ValidationError):
            Event(title="test", impact=1.5)

    def test_belief_confidence_validation(self):
        """测试观点置信度验证"""
        with pytest.raises(ValidationError):
            Belief(topic="test", stance="test", confidence=1.5)

    def test_fact_confidence_validation(self):
        """测试事实置信度验证"""
        with pytest.raises(ValidationError):
            Fact(fact="test", category="test", confidence=1.5)

    def test_evidence_confidence_validation(self):
        """测试证据置信度验证"""
        with pytest.raises(ValidationError):
            Evidence(source_type="test", source_name="test", content="test", confidence=1.5)
