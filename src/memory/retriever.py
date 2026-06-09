"""
记忆检索器

负责检索记忆
"""

from typing import List, Optional
from .models import MemoryItem


class MemoryRetriever:
    """
    记忆检索器
    
    检索相关记忆
    """
    
    def __init__(self):
        """初始化检索器"""
        pass
    
    def retrieve(
        self,
        memories: List[MemoryItem],
        query: str,
        top_k: int = 5,
        min_importance: float = 0.0,
    ) -> List[MemoryItem]:
        """
        检索记忆
        
        Args:
            memories: 记忆列表
            query: 查询文本
            top_k: 返回前k个结果
            min_importance: 最小重要度
            
        Returns:
            List[MemoryItem]: 检索结果
        """
        if not memories or not query:
            return []
        
        # 过滤重要度
        filtered = [m for m in memories if m.importance >= min_importance]
        
        # 搜索匹配
        results = []
        for memory in filtered:
            if self._is_match(memory.content, query):
                results.append(memory)
        
        # 按重要度排序
        results.sort(key=lambda x: x.importance, reverse=True)
        
        return results[:top_k]
    
    def _is_match(self, content: str, query: str) -> bool:
        """
        判断是否匹配
        
        Args:
            content: 内容
            query: 查询
            
        Returns:
            bool: 是否匹配
        """
        # 简化版本：检查查询是否在内容中
        return query.lower() in content.lower()
    
    def retrieve_by_type(
        self,
        memories: List[MemoryItem],
        memory_type: str,
        top_k: int = 5,
    ) -> List[MemoryItem]:
        """
        按类型检索记忆
        
        Args:
            memories: 记忆列表
            memory_type: 记忆类型
            top_k: 返回前k个结果
            
        Returns:
            List[MemoryItem]: 检索结果
        """
        results = [m for m in memories if m.memory_type == memory_type]
        results.sort(key=lambda x: x.importance, reverse=True)
        return results[:top_k]
