"""
PersonalityProfile 测试
"""

import pytest
from pydantic import ValidationError
from src.personality.profile import PersonalityProfile


class TestPersonalityProfile:
    """PersonalityProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建画像"""
        profile = PersonalityProfile(
            achievement_drive=0.8,
            curiosity=0.7,
            risk_preference=0.6,
            security_need=0.4,
            dominance=0.5,
            empathy=0.9,
            independence=0.7,
            responsibility=0.8,
            creativity=0.6,
            social_need=0.5,
        )
        assert profile.achievement_drive == 0.8
        assert profile.curiosity == 0.7
        assert profile.risk_preference == 0.6
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建画像"""
        profile = PersonalityProfile()
        assert profile.achievement_drive == 0.5
        assert profile.curiosity == 0.5
        assert profile.risk_preference == 0.5
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            PersonalityProfile(achievement_drive=1.5)
        
        with pytest.raises(ValidationError):
            PersonalityProfile(achievement_drive=-0.1)
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = PersonalityProfile(achievement_drive=0.8)
        data = profile.model_dump()
        assert data["achievement_drive"] == 0.8
        assert "curiosity" in data
    
    def test_profile_deserialization(self):
        """测试反序列化"""
        data = {
            "achievement_drive": 0.8,
            "curiosity": 0.7,
            "risk_preference": 0.6,
            "security_need": 0.4,
            "dominance": 0.5,
            "empathy": 0.9,
            "independence": 0.7,
            "responsibility": 0.8,
            "creativity": 0.6,
            "social_need": 0.5,
        }
        profile = PersonalityProfile(**data)
        assert profile.achievement_drive == 0.8
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = PersonalityProfile(achievement_drive=0.8)
        json_str = profile.model_dump_json()
        assert '"achievement_drive":0.8' in json_str