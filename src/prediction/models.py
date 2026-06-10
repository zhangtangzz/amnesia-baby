"""
行为预测数据模型
"""

from enum import Enum
from pydantic import BaseModel, Field


class ScenarioType(str, Enum):
    """场景类型"""
    RISK_DECISION = "risk_decision"
    SOCIAL_INTERACTION = "social_interaction"
    CONFLICT_RESOLUTION = "conflict_resolution"
    CREATIVE_PROBLEM = "creative_problem"
    LEADERSHIP = "leadership"
    STRESS_RESPONSE = "stress_response"


class BehaviorPrediction(BaseModel):
    """行为预测结果"""
    scenario: ScenarioType = Field(..., description="场景类型")
    tendency: float = Field(..., ge=0.0, le=1.0, description="行为倾向 (0=保守/被动, 1=激进/主动)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="预测置信度")
    description: str = Field(..., description="行为描述")
    reasoning: str = Field(..., description="推理依据")
