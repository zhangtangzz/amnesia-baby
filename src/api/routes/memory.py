"""
记忆API路由

负责记忆相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import MemoryRequest
from src.api.models.responses import MemoryResponse, ErrorResponse
from src.memory.shared_service import get_shared_memory_service


router = APIRouter(prefix="/api/memory", tags=["记忆"])


def _get_service():
    """获取共享记忆服务"""
    return get_shared_memory_service()


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
        svc = _get_service()
        svc.add_memory(
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
        svc = _get_service()
        context = svc.get_context(character_id, current_message)

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
        svc = _get_service()
        svc.consolidate_memories(character_id)

        return MemoryResponse(
            success=True,
            message="记忆巩固成功",
            data={
                "character_id": character_id,
                "short_term_count": svc.get_short_term_count(),
                "long_term_count": svc.get_long_term_count(),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="记忆巩固失败",
            error=str(e)
        )


@router.get("/list", response_model=MemoryResponse)
async def list_characters_with_memory():
    """
    列出所有有记忆的角色

    Returns:
        MemoryResponse: 包含角色ID列表
    """
    try:
        svc = _get_service()
        all_memories = svc.short_term_memory.get_all()
        # 提取不重复的 character_id
        character_ids = list(dict.fromkeys(m.character_id for m in all_memories))
        # 每个角色的记忆条数
        counts = {}
        for m in all_memories:
            counts[m.character_id] = counts.get(m.character_id, 0) + 1

        return MemoryResponse(
            success=True,
            message="获取角色列表成功",
            data={
                "characters": [
                    {"character_id": cid, "count": counts[cid]}
                    for cid in character_ids
                ],
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取角色列表失败",
            error=str(e)
        )


@router.get("/history/{character_id}", response_model=MemoryResponse)
async def get_history(character_id: str):
    """
    获取指定角色的对话历史

    Args:
        character_id: 角色ID

    Returns:
        MemoryResponse: 对话历史列表
    """
    try:
        svc = _get_service()
        all_memories = svc.short_term_memory.get_all()
        character_memories = [m for m in all_memories if m.character_id == character_id]

        # 序列化（datetime → ISO 字符串）
        history = []
        for m in character_memories:
            d = m.model_dump()
            if hasattr(d.get("timestamp"), "isoformat"):
                d["timestamp"] = d["timestamp"].isoformat()
            history.append(d)

        return MemoryResponse(
            success=True,
            message="获取对话历史成功",
            data={
                "character_id": character_id,
                "history": history,
                "count": len(character_memories),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取对话历史失败",
            error=str(e)
        )


@router.delete("/{character_id}", response_model=MemoryResponse)
async def clear_history(character_id: str):
    """
    清空指定角色的对话历史

    Args:
        character_id: 角色ID

    Returns:
        MemoryResponse: 操作结果
    """
    try:
        svc = _get_service()
        all_memories = svc.short_term_memory.get_all()
        # 保留不属于该角色的记忆
        remaining = [m for m in all_memories if m.character_id != character_id]
        removed_count = len(all_memories) - len(remaining)

        # 清空并重新添加
        svc.short_term_memory.clear()
        for m in remaining:
            svc.short_term_memory.add(m)

        svc._save_to_file()

        return MemoryResponse(
            success=True,
            message=f"已清空 {removed_count} 条记忆",
            data={
                "character_id": character_id,
                "removed_count": removed_count,
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="清空历史失败",
            error=str(e)
        )
