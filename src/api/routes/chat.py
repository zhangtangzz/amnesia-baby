"""
聊天API路由

负责聊天相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import ChatRequest
from src.api.models.responses import ChatResponse, ErrorResponse

router = APIRouter(prefix="/api/chat", tags=["聊天"])


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    发送消息
    
    Args:
        request: 聊天请求
        
    Returns:
        ChatResponse: 聊天响应
    """
    try:
        # 简化版本：模拟聊天响应
        return ChatResponse(
            success=True,
            message="消息发送成功",
            data={
                "reply": f"你好！我是{request.character_id}，很高兴认识你！",
                "character_id": request.character_id,
                "timestamp": "2026-06-09T20:20:00",
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="消息发送失败",
            error=str(e)
        )


@router.get("/history/{character_id}", response_model=ChatResponse)
async def get_chat_history(character_id: str):
    """
    获取聊天历史
    
    Args:
        character_id: 角色ID
        
    Returns:
        ChatResponse: 聊天历史响应
    """
    try:
        # 简化版本：返回空历史
        return ChatResponse(
            success=True,
            message="获取聊天历史成功",
            data={
                "character_id": character_id,
                "history": [],
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取聊天历史失败",
            error=str(e)
        )
