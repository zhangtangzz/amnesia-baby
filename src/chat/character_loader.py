"""
角色加载器

负责加载角色的人格画像，优先从 CharacterStore 读取
"""

from typing import Dict, Any, Optional
from ..personality.profile import PersonalityProfile
from ..personality.big_five import BigFiveProfile
from ..personality.enneagram import EnneagramProfile


class CharacterLoader:
    """
    角色加载器

    从 CharacterStore 加载角色信息，包括人格画像
    """

    def __init__(self, store=None):
        """
        初始化加载器

        Args:
            store: CharacterStore 实例，None 则延迟获取
        """
        self._store = store

    def _get_store(self):
        """获取 CharacterStore（延迟初始化）"""
        if self._store is None:
            from .character_store import CharacterStore
            from src.api.routes.characters import get_character_store
            try:
                self._store = get_character_store()
            except Exception:
                self._store = CharacterStore()
                self._store.add_defaults()
        return self._store

    async def load(self, character_id: str) -> Dict[str, Any]:
        """
        加载角色信息

        Args:
            character_id: 角色ID

        Returns:
            Dict: 包含角色信息的字典

        Raises:
            ValueError: 角色不存在
        """
        store = self._get_store()
        data = store.get(character_id)

        if data is None:
            raise ValueError(f"Character not found: {character_id}")

        # 解析人格画像
        personality = PersonalityProfile(**data.get("personality", {}))
        big_five = BigFiveProfile(**data.get("big_five", {}))
        enneagram = EnneagramProfile(**data.get("enneagram", {}))

        return {
            "character_id": data.get("character_id", character_id),
            "name": data.get("name", character_id),
            "personality": personality,
            "big_five": big_five,
            "enneagram": enneagram,
        }