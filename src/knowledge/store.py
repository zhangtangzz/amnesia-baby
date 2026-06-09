"""
知识存储器

负责存储和加载知识库
"""

from typing import Dict, Optional
from .models import KnowledgeBase


class KnowledgeStore:
    """
    知识存储器
    
    存储和加载知识库
    """
    
    def __init__(self):
        """初始化存储器"""
        # 内存存储（简化版本）
        self._storage: Dict[str, KnowledgeBase] = {}
    
    async def save(self, character_id: str, knowledge_base: KnowledgeBase) -> None:
        """
        保存知识库
        
        Args:
            character_id: 角色ID
            knowledge_base: 知识库
        """
        self._storage[character_id] = knowledge_base
    
    async def load(self, character_id: str) -> Optional[KnowledgeBase]:
        """
        加载知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[KnowledgeBase]: 知识库，不存在返回 None
        """
        return self._storage.get(character_id)
    
    async def delete(self, character_id: str) -> bool:
        """
        删除知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            bool: 是否删除成功
        """
        if character_id in self._storage:
            del self._storage[character_id]
            return True
        return False
    
    async def exists(self, character_id: str) -> bool:
        """
        检查知识库是否存在
        
        Args:
            character_id: 角色ID
            
        Returns:
            bool: 是否存在
        """
        return character_id in self._storage
