"""
上下文构建器

负责构建对话上下文
"""

from typing import List
from .models import MemoryItem


class ContextBuilder:
    """
    上下文构建器
    
    构建对话上下文
    """
    
    def __init__(self):
        """初始化构建器"""
        pass
    
    def build(
        self,
        memories: List[MemoryItem],
        current_message: str,
        max_context: int = 10,
    ) -> List[str]:
        """
        构建上下文
        
        Args:
            memories: 记忆列表
            current_message: 当前消息
            max_context: 最大上下文数量
            
        Returns:
            List[str]: 上下文列表
        """
        context = []
        
        # 添加记忆作为上下文
        for memory in memories[-max_context:]:
            context.append(memory.content)
        
        # 添加当前消息
        context.append(current_message)
        
        return context
    
    def build_with_summary(
        self,
        memories: List[MemoryItem],
        current_message: str,
        max_context: int = 10,
    ) -> List[str]:
        """
        构建带摘要的上下文
        
        Args:
            memories: 记忆列表
            current_message: 当前消息
            max_context: 最大上下文数量
            
        Returns:
            List[str]: 上下文列表
        """
        context = []
        
        # 添加记忆摘要
        if memories:
            summary = self._summarize_memories(memories)
            context.append(summary)
        
        # 添加当前消息
        context.append(current_message)
        
        return context
    
    def _summarize_memories(self, memories: List[MemoryItem]) -> str:
        """
        摘要记忆
        
        Args:
            memories: 记忆列表
            
        Returns:
            str: 摘要
        """
        if not memories:
            return ""
        
        # 简化版本：连接所有记忆内容
        contents = [m.content for m in memories]
        return "相关记忆：" + "；".join(contents)
