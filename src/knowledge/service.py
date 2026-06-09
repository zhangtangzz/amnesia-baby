"""
知识服务

负责协调知识库操作
"""

from typing import List, Optional
from .models import KnowledgeBase, Fact
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore
from .query import KnowledgeQuery
from .shared_store import get_shared_store


class KnowledgeService:
    """
    知识服务

    协调知识库操作：提取 -> 存储 -> 查询
    """

    def __init__(self):
        """初始化服务"""
        self.extractor = KnowledgeExtractor()
        self.store = get_shared_store()
        self.query = KnowledgeQuery()
    
    async def process(self, text: str, source: str, character_id: Optional[str] = None) -> KnowledgeBase:
        """
        处理文本，提取知识
        
        Args:
            text: 文本内容
            source: 来源名称
            character_id: 角色ID（可选）
            
        Returns:
            KnowledgeBase: 知识库
        """
        # 提取知识
        knowledge_base = await self.extractor.extract(text, source)
        
        # 保存到存储
        if character_id:
            await self.store.save(character_id, knowledge_base)
        
        return knowledge_base
    
    async def save(self, character_id: str, knowledge_base: KnowledgeBase) -> None:
        """
        保存知识库
        
        Args:
            character_id: 角色ID
            knowledge_base: 知识库
        """
        await self.store.save(character_id, knowledge_base)
    
    async def load(self, character_id: str) -> Optional[KnowledgeBase]:
        """
        加载知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[KnowledgeBase]: 知识库，不存在返回 None
        """
        return await self.store.load(character_id)
    
    async def query_facts(self, character_id: str, keyword: str) -> List[Fact]:
        """
        查询事实
        
        Args:
            character_id: 角色ID
            keyword: 关键词
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        knowledge_base = await self.store.load(character_id)
        if knowledge_base is None:
            return []
        return self.query.search_facts(knowledge_base, keyword)
