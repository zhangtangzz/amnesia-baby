"""
CharacterLoader 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.character_loader import CharacterLoader
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestCharacterLoader:
    """CharacterLoader 测试"""
    
    @pytest.fixture
    def loader(self):
        """创建 loader 实例"""
        return CharacterLoader()
    
    @pytest.fixture
    def mock_character_data(self):
        """模拟角色数据"""
        return {
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
    
    def test_loader_initialization(self, loader):
        """测试 loader 初始化"""
        assert loader is not None
        assert hasattr(loader, 'load')
    
    @pytest.mark.asyncio
    async def test_load_returns_character(self, loader, mock_character_data):
        """测试加载返回角色数据"""
        # 模拟数据源
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        assert isinstance(result, dict)
        assert "character_id" in result
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram" in result
    
    @pytest.mark.asyncio
    async def test_load_personality_profile(self, loader, mock_character_data):
        """测试加载人格画像"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        personality = result["personality"]
        assert isinstance(personality, PersonalityProfile)
        assert personality.achievement_drive == 0.9
    
    @pytest.mark.asyncio
    async def test_load_big_five_profile(self, loader, mock_character_data):
        """测试加载大五人格"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        big_five = result["big_five"]
        assert isinstance(big_five, BigFiveProfile)
        assert big_five.openness == 0.8
    
    @pytest.mark.asyncio
    async def test_load_enneagram_profile(self, loader, mock_character_data):
        """测试加载九型人格"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        enneagram = result["enneagram"]
        assert isinstance(enneagram, EnneagramProfile)
        assert enneagram.type8 == 0.4
    
    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, loader):
        """测试加载不存在的角色"""
        loader._load_from_source = AsyncMock(return_value=None)
        
        with pytest.raises(ValueError):
            await loader.load("nonexistent")
    
    @pytest.mark.asyncio
    async def test_load_invalid_data(self, loader):
        """测试加载无效数据"""
        loader._load_from_source = AsyncMock(return_value={"invalid": "data"})
        
        with pytest.raises(ValueError):
            await loader.load("elon")