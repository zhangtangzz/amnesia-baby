"""
行为预测 API 路由
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from src.prediction.predictor import BehaviorPredictor
from src.prediction.models import ScenarioType
from src.personality.profile import PersonalityProfile
from src.api.models.responses import BaseResponse
from src.chat.character_store import CharacterStore
from src.api.routes.characters import get_character_store

router = APIRouter(prefix="/api/predict", tags=["行为预测"])

predictor = BehaviorPredictor()


class PredictRequest(BaseModel):
    """预测请求"""
    personality: Optional[Dict[str, float]] = Field(default=None, description="人格特征")
    character_id: Optional[str] = Field(default=None, description="角色ID（与personality二选一）")
    scenario: str = Field(default="risk_decision", description="场景类型")


class PredictAllRequest(BaseModel):
    """批量预测请求"""
    personality: Optional[Dict[str, float]] = Field(default=None, description="人格特征")
    character_id: Optional[str] = Field(default=None, description="角色ID")


def _resolve_personality(
    personality: Optional[Dict[str, float]],
    character_id: Optional[str],
) -> PersonalityProfile:
    """解析人格画像（从请求或角色存储）"""
    if personality:
        return PersonalityProfile(**personality)
    if character_id:
        store = get_character_store()
        char = store.get(character_id)
        if char and char.get("personality"):
            return PersonalityProfile(**char["personality"])
        # 角色不存在或无人格，返回默认
        return PersonalityProfile()
    return PersonalityProfile()


@router.post("")
async def predict_behavior(request: PredictRequest):
    """预测单一场景行为"""
    try:
        # 解析场景
        try:
            scenario = ScenarioType(request.scenario)
        except ValueError:
            return {
                "success": False,
                "message": f"无效的场景类型: {request.scenario}",
                "error": f"支持的场景: {[s.value for s in ScenarioType]}",
            }

        personality = _resolve_personality(request.personality, request.character_id)
        result = predictor.predict(personality, scenario)

        return {
            "success": True,
            "message": "预测成功",
            "data": result.model_dump(),
        }
    except Exception as e:
        return {"success": False, "message": "预测失败", "error": str(e)}


@router.post("/all")
async def predict_all_behaviors(request: PredictAllRequest):
    """预测所有场景行为"""
    try:
        personality = _resolve_personality(request.personality, request.character_id)
        results = predictor.predict_all(personality)

        return {
            "success": True,
            "message": "预测成功",
            "data": {
                "predictions": [r.model_dump() for r in results],
                "count": len(results),
            },
        }
    except Exception as e:
        return {"success": False, "message": "预测失败", "error": str(e)}
