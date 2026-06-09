"""
知识库API路由

负责知识库相关API接口
"""

from fastapi import APIRouter, HTTPException
from src.api.models.requests import KnowledgeRequest
from src.api.models.responses import KnowledgeResponse, ErrorResponse
from src.knowledge.service import KnowledgeService

router = APIRouter(prefix="/api/knowledge", tags=["知识库"])

# 初始化服务
knowledge_service = KnowledgeService()


@router.post("/process", response_model=KnowledgeResponse)
async def process_knowledge(request: KnowledgeRequest):
    """
    处理知识
    
    Args:
        request: 知识库请求
        
    Returns:
        KnowledgeResponse: 知识库响应
    """
    try:
        # 处理知识
        result = await knowledge_service.process(
            request.text,
            request.source,
            request.character_id
        )
        
        return KnowledgeResponse(
            success=True,
            message="知识处理成功",
            data={
                "profile": result.profile.model_dump(),
                "facts": [f.model_dump() for f in result.facts],
                "evidence": [e.model_dump() for e in result.evidence],
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="知识处理失败",
            error=str(e)
        )


@router.get("/query/{character_id}", response_model=KnowledgeResponse)
async def query_knowledge(character_id: str, keyword: str = ""):
    """
    查询知识
    
    Args:
        character_id: 角色ID
        keyword: 关键词
        
    Returns:
        KnowledgeResponse: 知识库响应
    """
    try:
        # 查询知识
        facts = await knowledge_service.query_facts(character_id, keyword)
        
        return KnowledgeResponse(
            success=True,
            message="知识查询成功",
            data={
                "character_id": character_id,
                "keyword": keyword,
                "facts": [f.model_dump() for f in facts],
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="知识查询失败",
            error=str(e)
        )


@router.get("/base/{character_id}", response_model=KnowledgeResponse)
async def get_knowledge_base(character_id: str):
    """
    获取知识库
    
    Args:
        character_id: 角色ID
        
    Returns:
        KnowledgeResponse: 知识库响应
    """
    try:
        # 加载知识库
        knowledge_base = await knowledge_service.load(character_id)
        
        if knowledge_base is None:
            return KnowledgeResponse(
                success=True,
                message="知识库不存在",
                data={
                    "character_id": character_id,
                    "exists": False,
                }
            )
        
        return KnowledgeResponse(
            success=True,
            message="获取知识库成功",
            data={
                "character_id": character_id,
                "exists": True,
                "profile": knowledge_base.profile.model_dump(),
                "facts_count": len(knowledge_base.facts),
                "evidence_count": len(knowledge_base.evidence),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取知识库失败",
            error=str(e)
        )
