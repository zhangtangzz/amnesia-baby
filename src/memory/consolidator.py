"""
记忆巩固器

负责将短期记忆巩固为长期记忆
"""

from typing import List, Optional
from .models import MemoryItem


class MemoryConsolidator:
    """
    记忆巩固器
    
    将短期记忆巩固为长期记忆
    """
    
    def __init__(self):
        """初始化巩固器"""
        pass
    
    def consolidate(
        self,
        memories: List[MemoryItem],
        min_importance: float = 0.0,
        merge_similar: bool = False,
    ) -> List[MemoryItem]:
        """
        巩固记忆
        
        Args:
            memories: 记忆列表
            min_importance: 最小重要度
            merge_similar: 是否合并相似记忆
            
        Returns:
            List[MemoryItem]: 巩固后的记忆
        """
        if not memories:
            return []
        
        # 过滤重要度
        filtered = [m for m in memories if m.importance >= min_importance]
        
        if merge_similar:
            # 合并相似记忆（简化版本：按内容前缀合并）
            filtered = self._merge_similar(filtered)
        
        # 按重要度排序
        filtered.sort(key=lambda x: x.importance, reverse=True)
        
        return filtered
    
    def _merge_similar(self, memories: List[MemoryItem]) -> List[MemoryItem]:
        """
        合并相似记忆
        
        Args:
            memories: 记忆列表
            
        Returns:
            List[MemoryItem]: 合并后的记忆
        """
        if not memories:
            return []
        
        merged = []
        used = set()
        
        for i, mem1 in enumerate(memories):
            if i in used:
                continue
            
            # 查找相似记忆
            similar = [mem1]
            for j, mem2 in enumerate(memories):
                if j != i and j not in used:
                    if self._is_similar(mem1.content, mem2.content):
                        similar.append(mem2)
                        used.add(j)
            
            # 选择最重要的记忆
            best = max(similar, key=lambda x: x.importance)
            merged.append(best)
            used.add(i)
        
        return merged
    
    def _is_similar(self, text1: str, text2: str) -> bool:
        """
        判断两个文本是否相似
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            bool: 是否相似
        """
        # 简化版本：检查是否有共同关键词
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
        
        # 计算交集比例
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) > 0.5
