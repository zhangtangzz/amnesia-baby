"""
记忆API路由

负责记忆相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import MemoryRequest
from src.api.models.responses import MemoryResponse, ErrorResponse
from src.memory.service import MemoryService

router = APIRouter(prefix="/api/memory", tags=["记忆"])

# 初始化服务
memory_service = MemoryService()


@router.post("/add", response_model=MemoryResponse)
async def add_memory(request: MemoryRequest):
    """
    添加记忆
    
    Args:
        request: 记忆请求
        
    Returns:
        MemoryResponse: 记忆响应
    """
    try:
        # 添加记忆
        memory_service.add_memory(
            character_id=request.character_id,
            content=request.content,
            memory_type=request.memory_type,
            importance=request.importance,
        )
        
        return MemoryResponse(
            success=True,
            message="记忆添加成功",
            data={
                "character_id": request.character_id,
                "content": request.content,
                "memory_type": request.memory_type,
                "importance": request.importance,
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="记忆添加失败",
            error=str(e)
        )


@router.get("/context/{character_id}", response_model=MemoryResponse)
async def get_context(character_id: str, current_message: str = ""):
    """
    获取上下文
    
    Args:
        character_id: 角色ID
        current_message: 当前消息
        
    Returns:
        MemoryResponse: 记忆响应
    """
    try:
        # 获取上下文
        context = memory_service.get_context(character_id, current_message)
        
        return MemoryResponse(
            success=True,
            message="获取上下文成功",
            data={
                "character_id": character_id,
                "context": context,
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取上下文失败",
            error=str(e)
        )


@router.post("/consolidate/{character_id}", response_model=MemoryResponse)
async def consolidate_memories(character_id: str):
    """
    巩固记忆
    
    Args:
        character_id: 角色ID
        
    Returns:
        MemoryResponse: 记忆响应
    """
    try:
        # 巩固记忆
        memory_service.consolidate_memories(character_id)
        
        return MemoryResponse(
            success=True,
            message="记忆巩固成功",
            data={
                "character_id": character_id,
                "short_term_count": memory_service.get_short_term_count(),
                "long_term_count": memory_service.get_long_term_count(),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="记忆巩固失败",
            error=str(e)
        )
