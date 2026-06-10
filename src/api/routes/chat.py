"""
聊天API路由

负责聊天相关API接口，支持角色人格 + 记忆 + 多轮对话 + SSE 流式输出
"""

import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.api.models.requests import ChatRequest
from src.api.models.responses import ChatResponse, ErrorResponse
from src.config import get_settings
from src.chat.chat_engine import ChatEngine
from src.llm.token_tracker import TokenTracker

router = APIRouter(prefix="/api/chat", tags=["聊天"])

# 全局实例（延迟初始化）
_chat_engine = None
token_tracker = TokenTracker()


def _get_chat_engine() -> ChatEngine:
    """获取全局聊天引擎实例"""
    global _chat_engine
    if _chat_engine is None:
        settings = get_settings()
        _chat_engine = ChatEngine(
            provider_name=settings.llm_provider,
            api_key=settings.xiaomi_api_key or settings.openai_api_key or settings.deepseek_api_key,
            base_url=settings.xiaomi_api_base,
            model=settings.xiaomi_model if settings.llm_provider == "xiaomi" else settings.llm_model,
        )
    return _chat_engine


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    发送消息

    Args:
        request: 聊天请求

    Returns:
        ChatResponse: 聊天响应
    """
    try:
        settings = get_settings()

        # 检查是否配置了 API Key
        api_keys = {
            "openai": settings.openai_api_key,
            "deepseek": settings.deepseek_api_key,
            "qwen": settings.qwen_api_key,
            "xiaomi": settings.xiaomi_api_key,
        }
        provider_name = request.provider or settings.llm_provider
        has_api_key = bool(api_keys.get(provider_name, ""))

        if not has_api_key:
            # 无 API Key，返回 mock 响应
            return ChatResponse(
                success=True,
                message="消息发送成功（mock模式）",
                data={
                    "reply": f"你好！我是{request.character_id}，很高兴认识你！",
                    "character_id": request.character_id,
                    "provider": "mock",
                    "model": "mock",
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                }
            )

        # 使用聊天引擎（角色人格 + 知识 + 记忆 + LLM）
        engine = _get_chat_engine()
        result = await engine.chat(
            character_id=request.character_id,
            message=request.message,
            context=request.context,
        )

        # 记录 token 使用
        from src.llm.models import TokenUsage
        usage = TokenUsage(**result["usage"])
        token_tracker.record(usage, provider=result["provider"], model=result["model"])

        return ChatResponse(
            success=True,
            message="消息发送成功",
            data=result,
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="消息发送失败",
            error=str(e)
        )


@router.get("/history/{character_id}", response_model=ChatResponse)
async def get_chat_history(character_id: str):
    """
    获取聊天历史

    Args:
        character_id: 角色ID

    Returns:
        ChatResponse: 聊天历史响应
    """
    try:
        engine = _get_chat_engine()
        history = engine.get_history(character_id)

        return ChatResponse(
            success=True,
            message="获取聊天历史成功",
            data={
                "character_id": character_id,
                "history": history,
                "count": len(history),
            }
        )
    except Exception as e:
        return ErrorResponse(
            success=False,
            message="获取聊天历史失败",
            error=str(e)
        )


@router.get("/stats")
async def get_token_stats():
    """
    获取 Token 使用统计

    Returns:
        Dict: Token 统计信息
    """
    return {
        "success": True,
        "data": token_tracker.summary(),
        "history": token_tracker.get_history()[-10:],
    }


@router.get("/stream")
async def stream_chat(character_id: str, message: str, provider: str = ""):
    """
    SSE 流式聊天

    Args:
        character_id: 角色ID
        message: 用户消息
        provider: LLM 提供商名称

    Returns:
        StreamingResponse: SSE 流式响应
    """
    settings = get_settings()

    # 检查 API Key
    api_keys = {
        "openai": settings.openai_api_key,
        "deepseek": settings.deepseek_api_key,
        "qwen": settings.qwen_api_key,
        "xiaomi": settings.xiaomi_api_key,
    }
    provider_name = provider or settings.llm_provider
    has_api_key = bool(api_keys.get(provider_name, ""))

    async def event_generator():
        """SSE 事件生成器"""
        if not has_api_key:
            # Mock 模式：模拟流式输出
            mock_reply = f"你好！我是{character_id}，很高兴认识你！"
            for char in mock_reply:
                yield f"data: {json.dumps({'type': 'chunk', 'content': char}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'provider': 'mock', 'model': 'mock'}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
            return

        try:
            engine = _get_chat_engine()
            async for chunk in engine.stream(character_id=character_id, message=message):
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"

            yield f"data: {json.dumps({'type': 'done', 'provider': provider_name}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
