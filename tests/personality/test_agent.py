"""
PersonalityAgent 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.personality.agent import PersonalityAgent
from src.personality.evidence import PersonalityEvidence
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestPersonalityAgent:
    """PersonalityAgent 测试"""
    
    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        return PersonalityAgent()
    
    @pytest.fixture
    def sample_evidence(self):
        """示例证据"""
        return [
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="创业最大的风险是不创业",
                source="采访视频",
                confidence=0.88,
            ),
            PersonalityEvidence(
                trait="achievement_drive",
                score=0.85,
                evidence="我总是追求卓越",
                source="人物自传",
                confidence=0.90,
            ),
            PersonalityEvidence(
                trait="curiosity",
                score=0.78,
                evidence="我喜欢探索未知领域",
                source="博客文章",
                confidence=0.75,
            ),
        ]
    
    def test_agent_initialization(self, agent):
        """测试 agent 初始化"""
        assert agent is not None
        assert hasattr(agent, 'analyze')
    
    @pytest.mark.asyncio
    async def test_analyze_returns_profile(self, agent, sample_evidence):
        """测试分析返回人格画像"""
        result = await agent.analyze(sample_evidence)
        assert isinstance(result, dict)
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result
    
    @pytest.mark.asyncio
    async def test_analyze_personality_scores(self, agent, sample_evidence):
        """测试人格分数"""
        result = await agent.analyze(sample_evidence)
        personality = result["personality"]
        assert 0.0 <= personality["risk_preference"] <= 1.0
        assert 0.0 <= personality["achievement_drive"] <= 1.0
        assert 0.0 <= personality["curiosity"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_big_five_scores(self, agent, sample_evidence):
        """测试大五人格分数"""
        result = await agent.analyze(sample_evidence)
        big_five = result["big_five"]
        assert 0.0 <= big_five["openness"] <= 1.0
        assert 0.0 <= big_five["conscientiousness"] <= 1.0
        assert 0.0 <= big_five["extraversion"] <= 1.0
        assert 0.0 <= big_five["agreeableness"] <= 1.0
        assert 0.0 <= big_five["neuroticism"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_enneagram_top3(self, agent, sample_evidence):
        """测试九型人格前三"""
        result = await agent.analyze(sample_evidence)
        enneagram_top3 = result["enneagram_top3"]
        assert len(enneagram_top3) == 3
        for type_name, score in enneagram_top3.items():
            assert 0.0 <= score <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_empty_evidence(self, agent):
        """测试空证据"""
        result = await agent.analyze([])
        assert isinstance(result, dict)
        assert "personality" in result