"""
知识存储器

负责存储和加载知识库，支持持久化
"""

from typing import Dict, Optional
from .models import KnowledgeBase
from ..storage.database import save_json, load_json


class KnowledgeStore:
    """
    知识存储器

    内存存储 + JSON 文件持久化
    """

    def __init__(self, persist: bool = True):
        """
        初始化存储器

        Args:
            persist: 是否持久化到文件
        """
        self._persist = persist
        self._storage: Dict[str, KnowledgeBase] = {}
        if persist:
            self._load_from_file()

    async def save(self, character_id: str, knowledge_base: KnowledgeBase) -> None:
        """
        保存知识库

        Args:
            character_id: 角色ID
            knowledge_base: 知识库
        """
        self._storage[character_id] = knowledge_base
        self._save_to_file()

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

    def _save_to_file(self):
        """保存到文件"""
        if self._persist:
            data = {}
            for cid, kb in self._storage.items():
                data[cid] = kb.model_dump()
            save_json("knowledge", data)

    def _load_from_file(self):
        """从文件加载"""
        data = load_json("knowledge")
        if data and isinstance(data, dict):
            for cid, kb_data in data.items():
                try:
                    self._storage[cid] = KnowledgeBase(**kb_data)
                except Exception:
                    pass
