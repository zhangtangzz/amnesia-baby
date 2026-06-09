"""
聊天API路由

负责聊天相关API接口，支持真实 LLM 调用
"""

from fastapi import APIRouter
from src.api.models.requests import ChatRequest
from src.api.models.responses import ChatResponse, ErrorResponse
from src.config import get_settings
from src.llm.router import LLMRouter
from src.llm.retry import RetryableLLMProvider
from src.llm.token_tracker import TokenTracker

router = APIRouter(prefix="/api/chat", tags=["聊天"])

# 全局 token 统计器
token_tracker = TokenTracker()


def _get_llm_router(provider: str = None, model: str = None) -> RetryableLLMProvider:
    """
    获取 LLM 路由器（带重试）

    Args:
        provider: 指定提供商
        model: 指定模型

    Returns:
        RetryableLLMProvider
    """
    settings = get_settings()
    provider_name = provider or settings.llm_provider

    # 根据提供商获取 API Key
    api_keys = {
        "openai": settings.openai_api_key,
        "deepseek": settings.deepseek_api_key,
        "qwen": settings.qwen_api_key,
        "xiaomi": settings.xiaomi_api_key,
    }
    api_key = api_keys.get(provider_name, settings.openai_api_key)

    # 小米使用独立配置
    if provider_name == "xiaomi":
        from src.llm.xiaomi_provider import XiaomiProvider
        llm_provider = XiaomiProvider(
            api_key=api_key,
            base_url=settings.xiaomi_api_base,
            model=model or settings.xiaomi_model,
        )
    else:
        router_instance = LLMRouter(
            default_provider=provider_name,
            api_key=api_key,
            model=model or settings.llm_model,
        )
        llm_provider = router_instance.get_provider()

    # 创建降级提供商（如果配置了）
    fallback = None
    if settings.llm_fallback_provider and settings.llm_fallback_provider != provider_name:
        fallback_key = api_keys.get(settings.llm_fallback_provider, "")
        if fallback_key:
            fallback_router = LLMRouter(
                default_provider=settings.llm_fallback_provider,
                api_key=fallback_key,
            )
            fallback = fallback_router.get_provider()

    return RetryableLLMProvider(
        provider=llm_provider,
        max_retries=settings.llm_max_retries,
        fallback_provider=fallback,
    )


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

        # 使用真实 LLM
        llm = _get_llm_router(provider=request.provider, model=request.model)
        messages = []
        if request.context:
            messages.append({"role": "system", "content": request.context})
        messages.append({"role": "user", "content": request.message})

        response = await llm.generate(messages)

        # 记录 token 使用
        token_tracker.record(response.usage, provider=response.provider, model=response.model)

        return ChatResponse(
            success=True,
            message="消息发送成功",
            data={
                "reply": response.content,
                "character_id": request.character_id,
                "provider": response.provider,
                "model": response.model,
                "usage": response.usage.model_dump(),
            }
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
        return ChatResponse(
            success=True,
            message="获取聊天历史成功",
            data={
                "character_id": character_id,
                "history": [],
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
        "history": token_tracker.get_history()[-10:],  # 最近10条
    }
