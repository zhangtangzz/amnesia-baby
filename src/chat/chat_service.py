"""
聊天服务

负责协调角色聊天流程
"""

from typing import Dict, Any
from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from .llm_service import LLMService


class ChatService:
    """
    聊天服务
    
    协调角色聊天流程：加载角色 -> 加载知识 -> 构建Prompt -> 调用LLM
    """
    
    def __init__(self):
        """初始化服务"""
        self.character_loader = CharacterLoader()
        self.knowledge_loader = KnowledgeLoader()
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService()
    
    async def chat(self, character_id: str, message: str) -> Dict[str, Any]:
        """
        角色聊天
        
        Args:
            character_id: 角色ID
            message: 用户消息
            
        Returns:
            Dict: 包含回复的字典
            
        Raises:
            ValueError: 角色不存在
            Exception: LLM 调用失败
        """
        # 加载角色信息
        character = await self.character_loader.load(character_id)
        
        # 加载知识库
        knowledge = await self.knowledge_loader.load(character_id)
        
        # 构建 Prompt
        prompt = self.prompt_builder.build(character, knowledge, message)
        
        # 调用 LLM 生成回复
        reply = await self.llm_service.generate(prompt)
        
        return {
            "reply": reply,
        }