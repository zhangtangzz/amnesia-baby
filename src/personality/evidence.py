"""
人格证据数据模型
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from enum import Enum


class PersonalityTrait(str, Enum):
    """人格维度枚举"""
    ACHIEVEMENT_DRIVE = "achievement_drive"
    CURIOSITY = "curiosity"
    RISK_PREFERENCE = "risk_preference"
    SECURITY_NEED = "security_need"
    DOMINANCE = "dominance"
    EMPATHY = "empathy"
    INDEPENDENCE = "independence"
    RESPONSIBILITY = "responsibility"
    CREATIVITY = "creativity"
    SOCIAL_NEED = "social_need"


class PersonalityEvidence(BaseModel):
    """
    人格证据
    
    素材解析层与人格建模层之间的数据桥梁
    """
    
    trait: PersonalityTrait = Field(
        ...,
        description="人格维度"
    )
    
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="证据强度"
    )
    
    evidence: str = Field(
        ...,
        min_length=1,
        description="原始证据"
    )
    
    source: str = Field(
        ...,
        min_length=1,
        description="证据来源"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="置信度"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="扩展信息"
    )
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "trait": "risk_preference",
            "score": 0.91,
            "evidence": "创业最大的风险是不创业",
            "source": "采访视频",
            "confidence": 0.88,
            "metadata": {
                "timestamp": "12:33",
                "speaker": "角色本人",
            },
        }
    })