"""
记忆服务

负责协调记忆系统操作
"""

from typing import List, Optional
from .models import MemoryItem
from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from .consolidator import MemoryConsolidator
from .context import ContextBuilder
from .retriever import MemoryRetriever


class MemoryService:
    """
    记忆服务
    
    协调记忆系统操作：存储 -> 巩固 -> 检索 -> 上下文构建
    """
    
    def __init__(self, short_term_size: int = 100):
        """
        初始化服务
        
        Args:
            short_term_size: 短期记忆容量
        """
        self.short_term_memory = ShortTermMemory(max_size=short_term_size)
        self.long_term_memory = LongTermMemory()
        self.consolidator = MemoryConsolidator()
        self.context_builder = ContextBuilder()
        self.retriever = MemoryRetriever()
    
    def add_memory(
        self,
        character_id: str,
        content: str,
        memory_type: str = "conversation",
        importance: float = 0.5,
        metadata: Optional[dict] = None,
    ) -> None:
        """
        添加记忆
        
        Args:
            character_id: 角色ID
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要度
            metadata: 元数据
        """
        item = MemoryItem(
            content=content,
            character_id=character_id,
            memory_type=memory_type,
            importance=importance,
            metadata=metadata or {},
        )
        self.short_term_memory.add(item)
    
    def get_context(
        self,
        character_id: str,
        current_message: str,
        max_context: int = 10,
    ) -> List[str]:
        """
        获取上下文
        
        Args:
            character_id: 角色ID
            current_message: 当前消息
            max_context: 最大上下文数量
            
        Returns:
            List[str]: 上下文列表
        """
        # 获取短期记忆
        short_term = self.short_term_memory.get_recent(max_context)
        
        # 构建上下文
        context = self.context_builder.build(short_term, current_message, max_context)
        
        return context
    
    def consolidate_memories(self, character_id: str) -> None:
        """
        巩固记忆
        
        Args:
            character_id: 角色ID
        """
        # 获取所有短期记忆
        short_term = self.short_term_memory.get_all()
        
        # 巩固记忆
        consolidated = self.consolidator.consolidate(short_term, min_importance=0.5)
        
        # 添加到长期记忆
        for item in consolidated:
            self.long_term_memory.add(item)
    
    def search_long_term(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """
        搜索长期记忆
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
            
        Returns:
            List[MemoryItem]: 搜索结果
        """
        return self.long_term_memory.search(query, top_k)
    
    def get_short_term_count(self) -> int:
        """
        获取短期记忆数量
        
        Returns:
            int: 记忆数量
        """
        return self.short_term_memory.count()
    
    def get_long_term_count(self) -> int:
        """
        获取长期记忆数量
        
        Returns:
            int: 记忆数量
        """
        return self.long_term_memory.count()
