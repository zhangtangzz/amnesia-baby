"""
大五人格数据模型
"""

from pydantic import BaseModel, Field, ConfigDict


class BigFiveProfile(BaseModel):
    """
    大五人格（Big Five / OCEAN）
    
    包含 5 个人格维度，每个维度取值范围 0.0 ~ 1.0
    """
    
    openness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="开放性"
    )
    
    conscientiousness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="尽责性"
    )
    
    extraversion: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="外向性"
    )
    
    agreeableness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="宜人性"
    )
    
    neuroticism: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="神经质"
    )
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "openness": 0.75,
            "conscientiousness": 0.80,
            "extraversion": 0.72,
            "agreeableness": 0.65,
            "neuroticism": 0.30,
        }
    })