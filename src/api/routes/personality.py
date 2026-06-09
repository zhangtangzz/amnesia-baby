"""
人格API路由

负责人格相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import PersonalityRequest
from src.api.models.responses import PersonalityResponse, ErrorResponse
from src.personality.agent import PersonalityAgent
from src.material.text_parser import TextMaterialParser

router = APIRouter(prefix="/api/personality", tags=["人格"])

# 初始化服务
personality_agent = PersonalityAgent()
text_parser = TextMaterialParser()


@router.post("/analyze", response_model=PersonalityResponse)
async def analyze_personality(request: PersonalityRequest):
    """
    分析人格
    
    Args:
        request: 人格分析请求
        
    Returns:
        PersonalityResponse: 人格分析响应
    """
    try:
        # 解析文本
        evidence_list = await text_parser.parse(request.text, request.source)
        
        # 分析人格
        result = await personality_agent.analyze(evidence_list)
        
        return PersonalityResponse(
            success=True,
            message="人格分析成功",
            data=result
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="人格分析失败",
            error=str(e)
        )


@router.get("/profile/{character_id}", response_model=PersonalityResponse)
async def get_personality_profile(character_id: str):
    """
    获取人格画像
    
    Args:
        character_id: 角色ID
        
    Returns:
        PersonalityResponse: 人格画像响应
    """
    try:
        # 简化版本：返回默认人格画像
        from src.personality.profile import PersonalityProfile
        from src.personality.big_five import BigFiveProfile
        from src.personality.enneagram import EnneagramProfile
        
        return PersonalityResponse(
            success=True,
            message="获取人格画像成功",
            data={
                "character_id": character_id,
                "personality": PersonalityProfile().model_dump(),
                "big_five": BigFiveProfile().model_dump(),
                "enneagram": EnneagramProfile().model_dump(),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取人格画像失败",
            error=str(e)
        )
