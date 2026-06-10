"""
长期记忆

负责存储长期记忆
"""

from typing import List, Optional
from .models import MemoryItem


class LongTermMemory:
    """
    长期记忆
    
    存储和检索长期记忆
    """
    
    def __init__(self):
        """初始化长期记忆"""
        self._memories: List[MemoryItem] = []
    
    def add(self, item: MemoryItem) -> None:
        """
        添加记忆
        
        Args:
            item: 记忆项
        """
        self._memories.append(item)
    
    def search(self, keyword: str, top_k: int = 5) -> List[MemoryItem]:
        """
        搜索记忆
        
        Args:
            keyword: 关键词
            top_k: 返回前k个结果
            
        Returns:
            List[MemoryItem]: 记忆列表
        """
        results = []
        for memory in self._memories:
            if keyword.lower() in memory.content.lower():
                results.append(memory)
        
        # 按重要度排序
        results.sort(key=lambda x: x.importance, reverse=True)
        
        return results[:top_k]
    
    def get_by_importance(self, min_importance: float = 0.5) -> List[MemoryItem]:
        """
        按重要度获取记忆
        
        Args:
            min_importance: 最小重要度
            
        Returns:
            List[MemoryItem]: 记忆列表
        """
        results = [m for m in self._memories if m.importance >= min_importance]
        results.sort(key=lambda x: x.importance, reverse=True)
        return results
    
    def count(self) -> int:
        """
        获取记忆数量
        
        Returns:
            int: 记忆数量
        """
        return len(self._memories)
    
    def delete(self, item: MemoryItem) -> None:
        """
        删除记忆
        
        Args:
            item: 记忆项
        """
        if item in self._memories:
            self._memories.remove(item)
    
    def get_all(self) -> List[MemoryItem]:
        """
        获取所有记忆

        Returns:
            List[MemoryItem]: 所有记忆
        """
        return self._memories.copy()

    def clear(self) -> None:
        """
        清空记忆
        """
        self._memories.clear()
