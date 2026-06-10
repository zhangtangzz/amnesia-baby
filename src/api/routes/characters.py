"""
角色管理 API
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from src.chat.character_store import CharacterStore

router = APIRouter(prefix="/api/characters", tags=["角色管理"])

# 全局角色存储（含默认角色）
_character_store = CharacterStore()
_character_store.add_defaults()


class CharacterCreateRequest(BaseModel):
    """创建角色请求"""
    character_id: str = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    avatar: str = Field(default="👤", description="头像emoji")
    description: str = Field(default="", description="角色描述")
    personality: Optional[Dict[str, float]] = Field(default=None, description="人格特征")


class CharacterUpdateRequest(BaseModel):
    """更新角色请求（所有字段可选）"""
    name: Optional[str] = Field(default=None, description="角色名称")
    avatar: Optional[str] = Field(default=None, description="头像emoji")
    description: Optional[str] = Field(default=None, description="角色描述")
    personality: Optional[Dict[str, float]] = Field(default=None, description="人格特征")


class CharacterResponse(BaseModel):
    """角色响应"""
    success: bool
    message: str = ""
    data: Optional[Any] = None


def get_character_store() -> CharacterStore:
    """获取角色存储"""
    return _character_store


@router.get("/list", response_model=CharacterResponse)
async def list_characters():
    """列出所有角色"""
    chars = _character_store.list_all()
    return CharacterResponse(success=True, data=chars)


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: str):
    """获取角色详情"""
    char = _character_store.get(character_id)
    if char is None:
        return CharacterResponse(success=False, message=f"角色不存在: {character_id}")
    return CharacterResponse(success=True, data=char)


@router.post("/create", response_model=CharacterResponse)
async def create_character(request: CharacterCreateRequest):
    """创建角色"""
    if _character_store.get(request.character_id):
        return CharacterResponse(success=False, message=f"角色ID已存在: {request.character_id}")

    char = _character_store.create(
        character_id=request.character_id,
        name=request.name,
        avatar=request.avatar,
        description=request.description,
        personality=request.personality,
    )
    return CharacterResponse(success=True, message="角色创建成功", data=char)


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(character_id: str, request: CharacterUpdateRequest):
    """更新角色（部分更新）"""
    # 只传非 None 的字段
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    if not updates:
        return CharacterResponse(success=False, message="没有需要更新的字段")

    char = _character_store.update(character_id, **updates)
    if char is None:
        return CharacterResponse(success=False, message=f"角色不存在: {character_id}")
    return CharacterResponse(success=True, message="角色更新成功", data=char)


@router.delete("/{character_id}", response_model=CharacterResponse)
async def delete_character(character_id: str):
    """删除角色"""
    if _character_store.delete(character_id):
        return CharacterResponse(success=True, message="角色删除成功")
    return CharacterResponse(success=False, message=f"角色不存在: {character_id}")
