"""
TextMaterialParser 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.material.text_parser import TextMaterialParser
from src.personality.evidence import PersonalityEvidence


class TestTextMaterialParser:
    """TextMaterialParser 测试"""
    
    @pytest.fixture
    def parser(self):
        """创建 parser 实例"""
        return TextMaterialParser()
    
    def test_parser_initialization(self, parser):
        """测试 parser 初始化"""
        assert parser is not None
        assert hasattr(parser, 'parse')
    
    @pytest.mark.asyncio
    async def test_parse_returns_evidence_list(self, parser):
        """测试解析返回证据列表"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(e, PersonalityEvidence) for e in result)
    
    @pytest.mark.asyncio
    async def test_parse_with_source(self, parser):
        """测试解析包含来源"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert evidence.source == "采访视频"
    
    @pytest.mark.asyncio
    async def test_parse_empty_text(self, parser):
        """测试解析空文本"""
        result = await parser.parse("", source="test")
        assert isinstance(result, list)
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_parse_validates_trait(self, parser):
        """测试解析验证人格维度"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert evidence.trait.value in [
                "achievement_drive",
                "curiosity",
                "risk_preference",
                "security_need",
                "dominance",
                "empathy",
                "independence",
                "responsibility",
                "creativity",
                "social_need",
            ]
    
    @pytest.mark.asyncio
    async def test_parse_validates_score(self, parser):
        """测试解析验证分数"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert 0.0 <= evidence.score <= 1.0
    
    @pytest.mark.asyncio
    async def test_parse_validates_confidence(self, parser):
        """测试解析验证置信度"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert 0.0 <= evidence.confidence <= 1.0