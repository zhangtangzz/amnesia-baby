"""
EnneagramProfile 测试
"""

import pytest
from pydantic import ValidationError
from src.personality.enneagram import EnneagramProfile


class TestEnneagramProfile:
    """EnneagramProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建九型人格"""
        profile = EnneagramProfile(
            type1=0.10,
            type2=0.08,
            type3=0.30,
            type4=0.05,
            type5=0.12,
            type6=0.07,
            type7=0.18,
            type8=0.41,
            type9=0.09,
        )
        assert profile.type8 == 0.41
        assert profile.type3 == 0.30
        assert profile.type7 == 0.18
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建九型人格"""
        profile = EnneagramProfile()
        assert profile.type1 == 0.111
        assert profile.type2 == 0.111
        assert profile.type3 == 0.111
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            EnneagramProfile(type1=1.5)
        
        with pytest.raises(ValidationError):
            EnneagramProfile(type1=-0.1)
    
    def test_get_top3(self):
        """测试获取前三人格类型"""
        profile = EnneagramProfile(
            type1=0.10,
            type2=0.08,
            type3=0.30,
            type4=0.05,
            type5=0.12,
            type6=0.07,
            type7=0.18,
            type8=0.41,
            type9=0.09,
        )
        top3 = profile.get_top3()
        assert len(top3) == 3
        assert top3[0][0] == "type8"
        assert top3[1][0] == "type3"
        assert top3[2][0] == "type7"
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = EnneagramProfile(type8=0.41)
        data = profile.model_dump()
        assert data["type8"] == 0.41
        assert "type1" in data
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = EnneagramProfile(type8=0.41)
        json_str = profile.model_dump_json()
        assert '"type8":0.41' in json_str