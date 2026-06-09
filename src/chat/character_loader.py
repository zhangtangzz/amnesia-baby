"""
角色加载器

负责加载角色的人格画像
"""

from typing import Dict, Any, Optional
from ..personality.profile import PersonalityProfile
from ..personality.big_five import BigFiveProfile
from ..personality.enneagram import EnneagramProfile


class CharacterLoader:
    """
    角色加载器
    
    从数据源加载角色信息，包括人格画像
    """
    
    def __init__(self):
        """初始化加载器"""
        pass
    
    async def load(self, character_id: str) -> Dict[str, Any]:
        """
        加载角色信息
        
        Args:
            character_id: 角色ID
            
        Returns:
            Dict: 包含角色信息的字典
            
        Raises:
            ValueError: 角色不存在或数据无效
        """
        # 从数据源加载
        data = await self._load_from_source(character_id)
        
        if data is None:
            raise ValueError(f"Character not found: {character_id}")
        
        # 验证数据结构
        if "personality" not in data:
            raise ValueError(f"Invalid character data: missing personality")
        
        # 解析人格画像
        personality = PersonalityProfile(**data["personality"])
        big_five = BigFiveProfile(**data.get("big_five", {}))
        enneagram = EnneagramProfile(**data.get("enneagram", {}))
        
        return {
            "character_id": data.get("character_id", character_id),
            "name": data.get("name", ""),
            "personality": personality,
            "big_five": big_five,
            "enneagram": enneagram,
        }
    
    async def _load_from_source(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        从数据源加载角色数据
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[Dict]: 角色数据，不存在返回 None
        """
        # TODO: 实现实际的数据源加载逻辑
        # 这里返回模拟数据用于测试
        mock_data = {
            "elon": {
                "character_id": "elon",
                "name": "Elon Musk",
                "personality": {
                    "achievement_drive": 0.9,
                    "curiosity": 0.8,
                    "risk_preference": 0.85,
                },
                "big_five": {
                    "openness": 0.8,
                    "conscientiousness": 0.7,
                    "extraversion": 0.75,
                },
                "enneagram": {
                    "type8": 0.4,
                    "type3": 0.3,
                    "type7": 0.2,
                },
            }
        }
        return mock_data.get(character_id)