"""
聊天引擎

完整对话流水线：角色加载 → 知识加载 → 记忆上下文 → Prompt构建 → LLM调用 → 记忆存储
"""

from typing import Dict, Any, List, Optional
from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from ..memory.service import MemoryService
from ..memory.shared_service import get_shared_memory_service
from ..knowledge.shared_store import get_shared_store
from ..llm.xiaomi_provider import XiaomiProvider
from ..llm.base import LLMProvider
from ..llm.models import LLMResponse


class ChatEngine:
    """
    聊天引擎

    将角色人格、知识库、记忆系统、LLM 完整串联
    """

    def __init__(
        self,
        provider_name: str = "xiaomi",
        api_key: str = "",
        base_url: str = "https://token-plan-cn.xiaomimimo.com/anthropic",
        model: str = "mimo-v2.5-pro",
        llm_provider: Optional[LLMProvider] = None,
        memory_service: Optional[MemoryService] = None,
    ):
        """
        初始化引擎

        Args:
            provider_name: 提供商名称
            api_key: API Key
            base_url: API Base URL
            model: 模型名称
            llm_provider: 可选的外部 LLM 提供商实例
            memory_service: 可选的外部 MemoryService 实例
        """
        self.character_loader = CharacterLoader()
        self.knowledge_loader = KnowledgeLoader(store=get_shared_store())
        self.prompt_builder = PromptBuilder()
        self.memory_service = memory_service or get_shared_memory_service()

        # 创建或使用外部 LLM 提供商
        if llm_provider:
            self.llm_provider = llm_provider
        elif provider_name == "xiaomi":
            self.llm_provider = XiaomiProvider(
                api_key=api_key,
                base_url=base_url,
                model=model,
            )
        else:
            from ..llm.router import LLMRouter
            router = LLMRouter(default_provider=provider_name, api_key=api_key, model=model)
            self.llm_provider = router.get_provider()

    async def chat(
        self,
        character_id: str,
        message: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        角色聊天

        Args:
            character_id: 角色ID
            message: 用户消息
            context: 额外上下文

        Returns:
            Dict: 包含回复、provider、model、usage 等
        """
        # 1. 加载角色信息
        try:
            character = await self.character_loader.load(character_id)
        except ValueError:
            character = {"character_id": character_id, "name": character_id, "personality": None}

        # 2. 加载知识库
        try:
            knowledge = await self.knowledge_loader.load(character_id)
        except ValueError:
            knowledge = {"character_id": character_id, "knowledge": []}

        # 3. 获取记忆上下文
        memory_context = self.memory_service.get_context(
            character_id=character_id,
            current_message=message,
            max_context=10,
        )

        # 4. 构建 system prompt（角色人格 + 知识）
        system_prompt = self.prompt_builder.build(character, knowledge, message)

        # 5. 构建完整消息列表
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

        # 添加记忆上下文作为历史对话
        for ctx in memory_context[:-1]:  # 排除最后一条（当前消息）
            if ctx.startswith("用户:"):
                messages.append({"role": "user", "content": ctx[3:].strip()})
            elif ctx.startswith("助手:"):
                messages.append({"role": "assistant", "content": ctx[3:].strip()})

        # 添加当前用户消息
        messages.append({"role": "user", "content": message})

        # 6. 调用 LLM
        response: LLMResponse = await self.llm_provider.generate(messages)

        # 7. 存储记忆（用户消息 + 助手回复）
        self.memory_service.add_memory(
            character_id=character_id,
            content=f"用户: {message}",
            memory_type="conversation",
            importance=0.5,
        )
        self.memory_service.add_memory(
            character_id=character_id,
            content=f"助手: {response.content}",
            memory_type="conversation",
            importance=0.5,
        )

        return {
            "reply": response.content,
            "character_id": character_id,
            "provider": response.provider,
            "model": response.model,
            "usage": response.usage.model_dump(),
        }

    def get_history(self, character_id: str) -> List[Dict[str, str]]:
        """
        获取对话历史

        Args:
            character_id: 角色ID

        Returns:
            List[Dict]: 消息列表
        """
        context = self.memory_service.get_context(
            character_id=character_id,
            current_message="",
            max_context=50,
        )

        history = []
        for ctx in context:
            if ctx.startswith("用户:"):
                history.append({"role": "user", "content": ctx[3:].strip()})
            elif ctx.startswith("助手:"):
                history.append({"role": "assistant", "content": ctx[3:].strip()})

        return history
