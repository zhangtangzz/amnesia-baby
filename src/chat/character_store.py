"""
角色存储

管理角色的创建、查询、更新、删除
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class CharacterStore:
    """
    角色存储器

    内存存储角色数据，支持 CRUD 操作
    """

    def __init__(self):
        """初始化"""
        self._storage: Dict[str, Dict[str, Any]] = {}

    def create(
        self,
        character_id: str,
        name: str,
        avatar: str = "👤",
        description: str = "",
        personality: Optional[Dict[str, float]] = None,
        big_five: Optional[Dict[str, float]] = None,
        enneagram: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        创建角色

        Args:
            character_id: 角色ID
            name: 角色名称
            avatar: 头像 emoji
            description: 描述
            personality: 人格特征
            big_five: 大五人格
            enneagram: 九型人格

        Returns:
            Dict: 角色数据
        """
        char = {
            "character_id": character_id,
            "name": name,
            "avatar": avatar,
            "description": description,
            "personality": personality or {},
            "big_five": big_five or {},
            "enneagram": enneagram or {},
            "created_at": datetime.now().isoformat(),
        }
        self._storage[character_id] = char
        return char

    def get(self, character_id: str) -> Optional[Dict[str, Any]]:
        """获取角色"""
        return self._storage.get(character_id)

    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有角色"""
        return list(self._storage.values())

    def update(self, character_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        更新角色

        Args:
            character_id: 角色ID
            **kwargs: 要更新的字段

        Returns:
            Optional[Dict]: 更新后的角色，不存在返回 None
        """
        char = self._storage.get(character_id)
        if char is None:
            return None
        for key, value in kwargs.items():
            if key in char and key != "character_id":
                char[key] = value
        return char

    def delete(self, character_id: str) -> bool:
        """删除角色"""
        if character_id in self._storage:
            del self._storage[character_id]
            return True
        return False

    def count(self) -> int:
        """角色数量"""
        return len(self._storage)

    def add_defaults(self):
        """添加默认角色"""
        self.create(
            character_id="elon",
            name="Elon Musk",
            avatar="🚀",
            description="SpaceX 和 Tesla 创始人",
            personality={"achievement_drive": 0.9, "curiosity": 0.8, "risk_preference": 0.85},
            big_five={"openness": 0.8, "conscientiousness": 0.7, "extraversion": 0.75},
            enneagram={"type8": 0.4, "type3": 0.3, "type7": 0.2},
        )
        self.create(
            character_id="zhangsan",
            name="张三",
            avatar="👨‍💼",
            description="普通创业者",
            personality={"achievement_drive": 0.7, "curiosity": 0.6, "empathy": 0.7},
        )
