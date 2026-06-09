"""
向量检索数据模型
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class SearchResult(BaseModel):
    """搜索结果"""
    doc_id: str = Field(..., description="文档ID")
    score: float = Field(..., description="相似度分数")
    metadata: Dict[str, Any] = Field(default={}, description="元数据")
