"""
API响应模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class BaseResponse(BaseModel):
    """基础响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="操作成功", description="消息")


class PersonalityResponse(BaseResponse):
    """人格分析响应"""
    data: Optional[Dict[str, Any]] = Field(default=None, description="数据")


class ChatResponse(BaseResponse):
    """聊天响应"""
    data: Optional[Dict[str, Any]] = Field(default=None, description="数据")


class KnowledgeResponse(BaseResponse):
    """知识库响应"""
    data: Optional[Dict[str, Any]] = Field(default=None, description="数据")


class MemoryResponse(BaseResponse):
    """记忆响应"""
    data: Optional[Dict[str, Any]] = Field(default=None, description="数据")


class VectorSearchResponse(BaseResponse):
    """向量检索响应"""
    data: Optional[Dict[str, Any]] = Field(default=None, description="数据")


class ErrorResponse(BaseResponse):
    """错误响应"""
    success: bool = Field(default=False, description="是否成功")
    error: Optional[str] = Field(default=None, description="错误信息")
