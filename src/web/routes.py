"""
Web 页面路由

提供前端 HTML 页面
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter(tags=["页面"])

# 模板目录
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/chat", response_class=None)
async def chat_page(request: Request):
    """聊天页面"""
    return templates.TemplateResponse(request, "chat.html")


@router.get("/knowledge", response_class=None)
async def knowledge_page(request: Request):
    """知识库管理页面"""
    return templates.TemplateResponse(request, "knowledge.html")


@router.get("/profile", response_class=None)
async def profile_page(request: Request):
    """角色画像页面"""
    return templates.TemplateResponse(request, "profile.html")
