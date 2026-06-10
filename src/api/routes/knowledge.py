"""
知识库API路由

负责知识库相关API接口
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from src.api.models.requests import KnowledgeRequest
from src.api.models.responses import KnowledgeResponse, ErrorResponse
from src.knowledge.service import KnowledgeService
from src.knowledge.shared_store import get_shared_store
from src.knowledge.file_parser import parse_file, SUPPORTED_EXTENSIONS

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


# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = SUPPORTED_EXTENSIONS
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB (pdf/docx 可能较大)


@router.post("/upload", response_model=KnowledgeResponse)
async def upload_knowledge_file(
    file: UploadFile = File(...),
    source: str = Form(default="file_upload"),
    character_id: Optional[str] = Form(default=None),
):
    """
    上传素材文件并处理为知识

    支持 .txt, .md, .csv, .docx, .pdf 格式，最大 10MB

    Args:
        file: 上传的文件
        source: 素材来源
        character_id: 角色ID

    Returns:
        KnowledgeResponse: 知识库响应
    """
    try:
        # 检查文件扩展名
        filename = file.filename or "unknown.txt"
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            return ErrorResponse(
                success=False,
                message="文件格式不支持",
                error=f"仅支持 {', '.join(ALLOWED_EXTENSIONS)} 格式，当前: {ext}",
            )

        # 读取文件内容
        content_bytes = await file.read()

        # 检查文件大小
        if len(content_bytes) > MAX_FILE_SIZE:
            return ErrorResponse(
                success=False,
                message="文件过大",
                error=f"文件大小超过限制 (最大 {MAX_FILE_SIZE // 1024 // 1024}MB)",
            )

        # 解析文件内容
        text = parse_file(content_bytes, filename)
        if not text or not text.strip():
            return ErrorResponse(
                success=False,
                message="文件内容为空",
                error="上传的文件不包含有效文本内容",
            )
        text = text.strip()

        # 调用知识处理服务
        result = await knowledge_service.process(text, source or filename, character_id)

        return KnowledgeResponse(
            success=True,
            message="文件知识处理成功",
            data={
                "filename": filename,
                "file_size": len(content_bytes),
                "profile": result.profile.model_dump(),
                "facts": [f.model_dump() for f in result.facts],
                "evidence": [e.model_dump() for e in result.evidence],
            },
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="文件上传处理失败",
            error=str(e),
        )


@router.get("/list", response_model=KnowledgeResponse)
async def list_knowledge_bases():
    """
    列出所有知识库

    Returns:
        KnowledgeResponse: 知识库列表
    """
    try:
        store = get_shared_store()
        bases = []
        for cid, kb in store._storage.items():
            bases.append({
                "character_id": cid,
                "profile": kb.profile.model_dump(),
                "facts_count": len(kb.facts),
                "evidence_count": len(kb.evidence),
                "relationships_count": len(kb.relationships),
            })

        return KnowledgeResponse(
            success=True,
            message="获取知识库列表成功",
            data={"bases": bases, "count": len(bases)},
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取知识库列表失败",
            error=str(e),
        )


@router.get("/detail/{character_id}", response_model=KnowledgeResponse)
async def get_knowledge_detail(character_id: str):
    """
    获取知识库详情（含全部 facts 和 evidence）

    Args:
        character_id: 角色ID

    Returns:
        KnowledgeResponse: 知识库详情
    """
    try:
        kb = await knowledge_service.load(character_id)
        if kb is None:
            return ErrorResponse(
                success=False,
                message=f"知识库不存在: {character_id}",
            )

        return KnowledgeResponse(
            success=True,
            message="获取知识库详情成功",
            data={
                "character_id": character_id,
                "profile": kb.profile.model_dump(),
                "facts": [f.model_dump() for f in kb.facts],
                "evidence": [e.model_dump() for e in kb.evidence],
                "relationships": [r.model_dump() for r in kb.relationships],
                "events": [ev.model_dump() for ev in kb.events],
            },
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取知识库详情失败",
            error=str(e),
        )


@router.delete("/{character_id}", response_model=KnowledgeResponse)
async def delete_knowledge_base(character_id: str):
    """
    删除知识库

    Args:
        character_id: 角色ID

    Returns:
        KnowledgeResponse: 操作结果
    """
    try:
        store = get_shared_store()
        if not await store.exists(character_id):
            return ErrorResponse(
                success=False,
                message=f"知识库不存在: {character_id}",
            )

        await store.delete(character_id)
        store._save_to_file()

        return KnowledgeResponse(
            success=True,
            message="知识库删除成功",
            data={"character_id": character_id},
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="知识库删除失败",
            error=str(e),
        )
