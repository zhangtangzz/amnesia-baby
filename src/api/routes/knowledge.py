"""
知识库API路由

负责知识库相关API接口
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
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


# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = {".txt", ".md", ".csv"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/upload", response_model=KnowledgeResponse)
async def upload_knowledge_file(
    file: UploadFile = File(...),
    source: str = Form(default="file_upload"),
    character_id: Optional[str] = Form(default=None),
):
    """
    上传素材文件并处理为知识

    支持 .txt, .md, .csv 格式，最大 5MB

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

        # 解码为文本
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = content_bytes.decode("gbk")
            except UnicodeDecodeError:
                text = content_bytes.decode("utf-8", errors="replace")

        # 空文件检查
        text = text.strip()
        if not text:
            return ErrorResponse(
                success=False,
                message="文件内容为空",
                error="上传的文件不包含有效文本内容",
            )

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
