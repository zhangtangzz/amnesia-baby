"""
API请求模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PersonalityRequest(BaseModel):
    """人格分析请求"""
    text: str = Field(..., description="文本内容")
    source: str = Field(default="user_input", description="来源")


class ChatRequest(BaseModel):
    """聊天请求"""
    character_id: str = Field(..., description="角色ID")
    message: str = Field(..., description="消息内容")
    context: Optional[str] = Field(default=None, description="上下文")
    provider: Optional[str] = Field(default=None, description="LLM提供商 (openai/deepseek/qwen)")
    model: Optional[str] = Field(default=None, description="模型名称")


class KnowledgeRequest(BaseModel):
    """知识库请求"""
    text: str = Field(..., description="文本内容")
    source: str = Field(default="user_input", description="来源")
    character_id: Optional[str] = Field(default=None, description="角色ID")


class MemoryRequest(BaseModel):
    """记忆请求"""
    character_id: str = Field(..., description="角色ID")
    content: str = Field(..., description="记忆内容")
    memory_type: str = Field(default="conversation", description="记忆类型")
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="重要度")


class VectorSearchRequest(BaseModel):
    """向量检索请求"""
    query: str = Field(..., description="查询文本")
    top_k: int = Field(default=5, ge=1, le=100, description="返回数量")
    threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="相似度阈值")
