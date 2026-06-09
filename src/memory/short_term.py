"""
短期记忆

负责存储短期记忆
"""

from typing import List, Optional
from collections import deque
from .models import MemoryItem


class ShortTermMemory:
    """
    短期记忆
    
    存储和检索短期记忆
    """
    
    def __init__(self, max_size: int = 100):
        """
        初始化短期记忆
        
        Args:
            max_size: 最大容量
        """
        self.max_size = max_size
        self._memories: deque[MemoryItem] = deque(maxlen=max_size)
    
    def add(self, item: MemoryItem) -> None:
        """
        添加记忆
        
        Args:
            item: 记忆项
        """
        self._memories.append(item)
    
    def get_recent(self, count: int = 5) -> List[MemoryItem]:
        """
        获取最近的记忆
        
        Args:
            count: 获取数量
            
        Returns:
            List[MemoryItem]: 记忆列表
        """
        memories = list(self._memories)
        return memories[-count:] if len(memories) >= count else memories
    
    def count(self) -> int:
        """
        获取记忆数量
        
        Returns:
            int: 记忆数量
        """
        return len(self._memories)
    
    def clear(self) -> None:
        """
        清空记忆
        """
        self._memories.clear()
    
    def get_all(self) -> List[MemoryItem]:
        """
        获取所有记忆
        
        Returns:
            List[MemoryItem]: 所有记忆
        """
        return list(self._memories)
