"""
人格建模流水线集成测试
"""

import pytest
from src.material.text_parser import TextMaterialParser
from src.personality.agent import PersonalityAgent


class TestPersonalityPipeline:
    """人格建模流水线集成测试"""
    
    @pytest.fixture
    def parser(self):
        """创建解析器"""
        return TextMaterialParser()
    
    @pytest.fixture
    def agent(self):
        """创建 agent"""
        return PersonalityAgent()
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, parser, agent):
        """测试完整流水线"""
        # 输入文本
        text = "创业最大的风险是不创业"
        source = "采访视频"
        
        # 解析文本
        evidence_list = await parser.parse(text, source)
        assert len(evidence_list) > 0
        
        # 分析人格
        result = await agent.analyze(evidence_list)
        
        # 验证结果结构
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result
        
        # 验证人格分数
        personality = result["personality"]
        assert 0.0 <= personality["risk_preference"] <= 1.0
        
        # 验证大五人格
        big_five = result["big_five"]
        assert 0.0 <= big_five["openness"] <= 1.0
        assert 0.0 <= big_five["conscientiousness"] <= 1.0
        assert 0.0 <= big_five["extraversion"] <= 1.0
        assert 0.0 <= big_five["agreeableness"] <= 1.0
        assert 0.0 <= big_five["neuroticism"] <= 1.0
        
        # 验证九型人格
        enneagram_top3 = result["enneagram_top3"]
        assert len(enneagram_top3) == 3
        for type_name, score in enneagram_top3.items():
            assert 0.0 <= score <= 1.0
    
    @pytest.mark.asyncio
    async def test_pipeline_with_multiple_texts(self, parser, agent):
        """测试多文本流水线"""
        texts = [
            ("创业最大的风险是不创业", "采访视频"),
            ("我总是追求卓越", "人物自传"),
            ("我喜欢探索未知领域", "博客文章"),
        ]
        
        all_evidence = []
        for text, source in texts:
            evidence = await parser.parse(text, source)
            all_evidence.extend(evidence)
        
        result = await agent.analyze(all_evidence)
        
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result