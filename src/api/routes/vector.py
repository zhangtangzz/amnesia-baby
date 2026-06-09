"""
向量检索API路由

负责向量检索相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import VectorSearchRequest
from src.api.models.responses import VectorSearchResponse, ErrorResponse
from src.vector.service import VectorSearchService

router = APIRouter(prefix="/api/vector", tags=["向量检索"])

# 初始化服务
vector_service = VectorSearchService()


@router.post("/add", response_model=VectorSearchResponse)
async def add_document(request: dict):
    """
    添加文档
    
    Args:
        request: 请求数据
        
    Returns:
        VectorSearchResponse: 向量检索响应
    """
    try:
        # 添加文档
        doc_id = request.get("doc_id", f"doc_{vector_service.count() + 1}")
        text = request.get("text", "")
        metadata = request.get("metadata", {})
        
        vector_service.add_document(doc_id, text, metadata)
        
        return VectorSearchResponse(
            success=True,
            message="文档添加成功",
            data={
                "doc_id": doc_id,
                "text": text,
                "total_count": vector_service.count(),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="文档添加失败",
            error=str(e)
        )


@router.post("/search", response_model=VectorSearchResponse)
async def search_documents(request: VectorSearchRequest):
    """
    搜索文档
    
    Args:
        request: 向量检索请求
        
    Returns:
        VectorSearchResponse: 向量检索响应
    """
    try:
        # 搜索文档
        results = vector_service.search(
            request.query,
            top_k=request.top_k,
            threshold=request.threshold,
        )
        
        return VectorSearchResponse(
            success=True,
            message="搜索成功",
            data={
                "query": request.query,
                "results": [
                    {
                        "doc_id": r.doc_id,
                        "score": r.score,
                        "metadata": r.metadata,
                    }
                    for r in results
                ],
                "total_count": len(results),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="搜索失败",
            error=str(e)
        )


@router.get("/count", response_model=VectorSearchResponse)
async def get_vector_count():
    """
    获取向量数量
    
    Returns:
        VectorSearchResponse: 向量检索响应
    """
    try:
        return VectorSearchResponse(
            success=True,
            message="获取向量数量成功",
            data={
                "count": vector_service.count(),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取向量数量失败",
            error=str(e)
        )
