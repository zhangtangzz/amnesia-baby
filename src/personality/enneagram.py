"""
九型人格数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Tuple


class EnneagramProfile(BaseModel):
    """
    九型人格（Enneagram）
    
    包含 9 种人格类型，每个类型取值范围 0.0 ~ 1.0
    """
    
    type1: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="完美主义者"
    )
    
    type2: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="助人者"
    )
    
    type3: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="成就者"
    )
    
    type4: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="个人主义者"
    )
    
    type5: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="观察者"
    )
    
    type6: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="忠诚者"
    )
    
    type7: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="热情者"
    )
    
    type8: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="挑战者"
    )
    
    type9: float = Field(
        default=0.112,
        ge=0.0,
        le=1.0,
        description="和平者"
    )
    
    def get_top3(self) -> List[Tuple[str, float]]:
        """
        获取前三人格类型
        
        Returns:
            List[Tuple[str, float]]: [(类型名, 分数), ...]
        """
        scores = {
            "type1": self.type1,
            "type2": self.type2,
            "type3": self.type3,
            "type4": self.type4,
            "type5": self.type5,
            "type6": self.type6,
            "type7": self.type7,
            "type8": self.type8,
            "type9": self.type9,
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:3]
    
    class Config:
        """Pydantic 配置"""
        json_schema_extra = {
            "example": {
                "type1": 0.10,
                "type2": 0.08,
                "type3": 0.30,
                "type4": 0.05,
                "type5": 0.12,
                "type6": 0.07,
                "type7": 0.18,
                "type8": 0.41,
                "type9": 0.09,
            }
        }