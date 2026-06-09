"""
PersonalityEvidence 测试
"""

import pytest
from pydantic import ValidationError
from src.personality.evidence import PersonalityEvidence


class TestPersonalityEvidence:
    """PersonalityEvidence 测试"""
    
    def test_create_evidence_with_valid_data(self):
        """测试使用有效数据创建证据"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        assert evidence.trait == "risk_preference"
        assert evidence.score == 0.91
        assert evidence.evidence == "创业最大的风险是不创业"
        assert evidence.source == "采访视频"
        assert evidence.confidence == 0.88
    
    def test_create_evidence_with_metadata(self):
        """测试使用元数据创建证据"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
            metadata={"timestamp": "12:33", "speaker": "角色本人"},
        )
        assert evidence.metadata["timestamp"] == "12:33"
        assert evidence.metadata["speaker"] == "角色本人"
    
    def test_invalid_trait_validation(self):
        """测试无效的人格维度"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="invalid_trait",
                score=0.91,
                evidence="test",
                source="test",
                confidence=0.88,
            )
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=1.5,
                evidence="test",
                source="test",
                confidence=0.88,
            )
        
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=-0.1,
                evidence="test",
                source="test",
                confidence=0.88,
            )
    
    def test_confidence_range_validation(self):
        """测试置信度范围验证"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="test",
                source="test",
                confidence=1.5,
            )
        
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="test",
                source="test",
                confidence=-0.1,
            )
    
    def test_evidence_serialization(self):
        """测试序列化"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        data = evidence.model_dump()
        assert data["trait"] == "risk_preference"
        assert data["score"] == 0.91
    
    def test_evidence_deserialization(self):
        """测试反序列化"""
        data = {
            "trait": "risk_preference",
            "score": 0.91,
            "evidence": "创业最大的风险是不创业",
            "source": "采访视频",
            "confidence": 0.88,
        }
        evidence = PersonalityEvidence(**data)
        assert evidence.trait == "risk_preference"
    
    def test_evidence_to_json(self):
        """测试导出为 JSON"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        json_str = evidence.model_dump_json()
        assert '"trait":"risk_preference"' in json_str