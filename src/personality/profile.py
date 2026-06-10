"""
人格画像数据模型
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PersonalityProfile(BaseModel):
    """
    人格画像
    
    包含 10 个人格维度，每个维度取值范围 0.0 ~ 1.0
    """
    
    achievement_drive: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="成就驱动"
    )
    
    curiosity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="好奇心"
    )
    
    risk_preference: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="风险偏好"
    )
    
    security_need: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="安全需求"
    )
    
    dominance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="支配性"
    )
    
    empathy: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="共情能力"
    )
    
    independence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="独立性"
    )
    
    responsibility: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="责任感"
    )
    
    creativity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="创造力"
    )
    
    social_need: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="社交需求"
    )
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
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
    })