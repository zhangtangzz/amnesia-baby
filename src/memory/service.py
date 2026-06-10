"""
记忆服务

负责协调记忆系统操作，支持 JSON 文件持久化
"""

import logging
from typing import List, Optional
from .models import MemoryItem
from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from .consolidator import MemoryConsolidator
from .context import ContextBuilder
from .retriever import MemoryRetriever
from ..storage.database import save_json, load_json

logger = logging.getLogger(__name__)


class MemoryService:
    """
    记忆服务

    协调记忆系统操作：存储 -> 巩固 -> 检索 -> 上下文构建
    支持 JSON 文件持久化
    """

    def __init__(self, short_term_size: int = 100, persist: bool = True):
        """
        初始化服务

        Args:
            short_term_size: 短期记忆容量
            persist: 是否持久化到文件
        """
        self._persist = persist
        self.short_term_memory = ShortTermMemory(max_size=short_term_size)
        self.long_term_memory = LongTermMemory()
        self.consolidator = MemoryConsolidator()
        self.context_builder = ContextBuilder()
        self.retriever = MemoryRetriever()

        if persist:
            self._load_from_file()

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
        self._save_to_file()

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
        # 获取短期记忆（过滤角色）
        all_short = self.short_term_memory.get_all()
        character_memories = [m for m in all_short if m.character_id == character_id]
        recent = character_memories[-max_context:] if len(character_memories) >= max_context else character_memories

        # 构建上下文
        context = self.context_builder.build(recent, current_message, max_context)

        return context

    def consolidate_memories(self, character_id: str) -> None:
        """
        巩固记忆

        Args:
            character_id: 角色ID
        """
        # 获取该角色的短期记忆
        all_short = self.short_term_memory.get_all()
        character_memories = [m for m in all_short if m.character_id == character_id]

        # 巩固记忆
        consolidated = self.consolidator.consolidate(character_memories, min_importance=0.5)

        # 添加到长期记忆
        for item in consolidated:
            self.long_term_memory.add(item)

        self._save_to_file()

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

    def _serialize_item(self, item: MemoryItem) -> dict:
        """将 MemoryItem 序列化为可 JSON 化的字典"""
        data = item.model_dump()
        # datetime 转为 ISO 字符串
        if "timestamp" in data and hasattr(data["timestamp"], "isoformat"):
            data["timestamp"] = data["timestamp"].isoformat()
        return data

    def _save_to_file(self) -> None:
        """保存记忆到 JSON 文件"""
        if not self._persist:
            return
        data = {
            "short_term": [self._serialize_item(m) for m in self.short_term_memory.get_all()],
            "long_term": [self._serialize_item(m) for m in self.long_term_memory.get_all()],
        }
        save_json("memory", data)

    def _load_from_file(self) -> None:
        """从 JSON 文件加载记忆"""
        data = load_json("memory")
        if not data or not isinstance(data, dict):
            return

        # 加载短期记忆
        for item_data in data.get("short_term", []):
            try:
                item = MemoryItem(**item_data)
                self.short_term_memory.add(item)
            except Exception as e:
                logger.warning(f"Failed to load short-term memory item: {e}")

        # 加载长期记忆
        for item_data in data.get("long_term", []):
            try:
                item = MemoryItem(**item_data)
                self.long_term_memory.add(item)
            except Exception as e:
                logger.warning(f"Failed to load long-term memory item: {e}")
