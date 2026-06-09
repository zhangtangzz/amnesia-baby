"""
BigFiveProfile 测试
"""

import pytest
from pydantic import ValidationError
from src.personality.big_five import BigFiveProfile


class TestBigFiveProfile:
    """BigFiveProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建大五人格"""
        profile = BigFiveProfile(
            openness=0.75,
            conscientiousness=0.80,
            extraversion=0.72,
            agreeableness=0.65,
            neuroticism=0.30,
        )
        assert profile.openness == 0.75
        assert profile.conscientiousness == 0.80
        assert profile.extraversion == 0.72
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建大五人格"""
        profile = BigFiveProfile()
        assert profile.openness == 0.5
        assert profile.conscientiousness == 0.5
        assert profile.extraversion == 0.5
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            BigFiveProfile(openness=1.5)
        
        with pytest.raises(ValidationError):
            BigFiveProfile(openness=-0.1)
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = BigFiveProfile(openness=0.75)
        data = profile.model_dump()
        assert data["openness"] == 0.75
        assert "conscientiousness" in data
    
    def test_profile_deserialization(self):
        """测试反序列化"""
        data = {
            "openness": 0.75,
            "conscientiousness": 0.80,
            "extraversion": 0.72,
            "agreeableness": 0.65,
            "neuroticism": 0.30,
        }
        profile = BigFiveProfile(**data)
        assert profile.openness == 0.75
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = BigFiveProfile(openness=0.75)
        json_str = profile.model_dump_json()
        assert '"openness":0.75' in json_str