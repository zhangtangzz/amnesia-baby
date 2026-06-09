"""
知识更新器

负责更新知识库
"""

from typing import Dict, Any
from .models import KnowledgeBase, Fact


class KnowledgeUpdater:
    """
    知识更新器
    
    更新知识库中的信息
    """
    
    def __init__(self):
        """初始化更新器"""
        pass
    
    def update_profile(self, knowledge_base: KnowledgeBase, new_data: Dict[str, Any]) -> None:
        """
        更新基础信息
        
        Args:
            knowledge_base: 知识库
            new_data: 新数据
        """
        for key, value in new_data.items():
            if hasattr(knowledge_base.profile, key):
                setattr(knowledge_base.profile, key, value)
    
    def add_fact(self, knowledge_base: KnowledgeBase, fact: Fact) -> None:
        """
        添加事实
        
        Args:
            knowledge_base: 知识库
            fact: 事实
        """
        knowledge_base.facts.append(fact)
    
    def update_fact_confidence(self, knowledge_base: KnowledgeBase, fact_index: int, new_confidence: float) -> None:
        """
        更新事实置信度
        
        Args:
            knowledge_base: 知识库
            fact_index: 事实索引
            new_confidence: 新置信度
            
        Raises:
            IndexError: 索引无效
        """
        if fact_index < 0 or fact_index >= len(knowledge_base.facts):
            raise IndexError(f"Fact index out of range: {fact_index}")
        
        knowledge_base.facts[fact_index].confidence = new_confidence
