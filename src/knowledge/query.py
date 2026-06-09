"""
知识查询器

负责查询知识库
"""

from typing import List
from .models import KnowledgeBase, KnowledgeProfile, Fact


class KnowledgeQuery:
    """
    知识查询器
    
    查询知识库中的信息
    """
    
    def __init__(self):
        """初始化查询器"""
        pass
    
    def search_facts(self, knowledge_base: KnowledgeBase, keyword: str) -> List[Fact]:
        """
        搜索事实
        
        Args:
            knowledge_base: 知识库
            keyword: 关键词
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        results = []
        for fact in knowledge_base.facts:
            if keyword in fact.fact:
                results.append(fact)
        return results
    
    def get_facts_by_category(self, knowledge_base: KnowledgeBase, category: str) -> List[Fact]:
        """
        按类别获取事实
        
        Args:
            knowledge_base: 知识库
            category: 类别
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        results = []
        for fact in knowledge_base.facts:
            if fact.category == category:
                results.append(fact)
        return results
    
    def get_profile(self, knowledge_base: KnowledgeBase) -> KnowledgeProfile:
        """
        获取基础信息
        
        Args:
            knowledge_base: 知识库
            
        Returns:
            KnowledgeProfile: 基础信息
        """
        return knowledge_base.profile
