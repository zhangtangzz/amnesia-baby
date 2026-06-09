"""
记忆数据模型
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class MemoryItem(BaseModel):
    """记忆项"""
    content: str = Field(..., description="记忆内容")
    character_id: str = Field(..., description="角色ID")
    memory_type: str = Field(default="conversation", description="记忆类型")
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="重要度")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    metadata: Dict[str, Any] = Field(default={}, description="元数据")
