"""
Chat Agent

负责角色聊天的核心逻辑
"""

from typing import Dict, Any
from .chat_service import ChatService


class ChatAgent:
    """
    Chat Agent
    
    角色聊天的核心入口
    """
    
    def __init__(self):
        """初始化 agent"""
        self.chat_service = ChatService()
    
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
        return await self.chat_service.chat(character_id, message)