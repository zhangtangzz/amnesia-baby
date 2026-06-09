"""
知识加载器

负责加载角色的知识库，优先从 KnowledgeStore 读取，无数据时回退到 mock
"""

from typing import Dict, Any, List, Optional
from ..knowledge.store import KnowledgeStore


class KnowledgeLoader:
    """
    知识加载器

    从 KnowledgeStore 加载角色的知识库
    """

    def __init__(self, store: Optional[KnowledgeStore] = None):
        """
        初始化加载器

        Args:
            store: 知识存储器实例，None 则创建新实例
        """
        self._store = store or KnowledgeStore()

    async def load(self, character_id: str) -> Dict[str, Any]:
        """
        加载角色知识库

        优先从 KnowledgeStore 读取，无数据时回退到 mock

        Args:
            character_id: 角色ID

        Returns:
            Dict: 包含知识库的字典
        """
        # 1. 尝试从 KnowledgeStore 读取
        kb = await self._store.load(character_id)

        if kb is not None:
            knowledge_list = []
            # 提取 profile 信息
            if kb.profile:
                if kb.profile.name:
                    knowledge_list.append({
                        "topic": "基本信息",
                        "content": f"姓名: {kb.profile.name}",
                        "source": "知识库",
                    })
                if kb.profile.occupation:
                    knowledge_list.append({
                        "topic": "职业",
                        "content": kb.profile.occupation,
                        "source": "知识库",
                    })
            # 提取 facts
            for fact in kb.facts:
                knowledge_list.append({
                    "topic": fact.category or "事实",
                    "content": fact.fact,
                    "source": "知识库",
                })

            if knowledge_list:
                return {
                    "character_id": character_id,
                    "knowledge": knowledge_list,
                }

        # 2. 回退到 mock 数据
        return await self._load_mock(character_id)

    async def _load_mock(self, character_id: str) -> Dict[str, Any]:
        """Mock 数据回退"""
        mock_data = {
            "elon": {
                "character_id": "elon",
                "knowledge": [
                    {"topic": "创业", "content": "创业让我能够实现那些看似不可能的想法", "source": "采访视频"},
                    {"topic": "技术", "content": "技术是改变世界的力量", "source": "演讲"},
                ],
            }
        }
        data = mock_data.get(character_id)
        if data:
            return {"character_id": character_id, "knowledge": data["knowledge"]}
        return {"character_id": character_id, "knowledge": []}