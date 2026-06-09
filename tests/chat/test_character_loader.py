"""
CharacterLoader 测试
"""

import pytest
from src.chat.character_loader import CharacterLoader
from src.chat.character_store import CharacterStore
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestCharacterLoader:
    """CharacterLoader 测试"""

    @pytest.fixture
    def store(self):
        """创建带默认角色的 store"""
        s = CharacterStore()
        s.add_defaults()
        return s

    @pytest.fixture
    def loader(self, store):
        """创建 loader 实例"""
        return CharacterLoader(store=store)

    def test_loader_initialization(self, loader):
        """测试 loader 初始化"""
        assert loader is not None
        assert hasattr(loader, 'load')

    @pytest.mark.asyncio
    async def test_load_returns_character(self, loader):
        """测试加载返回角色数据"""
        result = await loader.load("elon")
        assert isinstance(result, dict)
        assert "character_id" in result
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram" in result

    @pytest.mark.asyncio
    async def test_load_personality_profile(self, loader):
        """测试加载人格画像"""
        result = await loader.load("elon")
        personality = result["personality"]
        assert isinstance(personality, PersonalityProfile)
        assert personality.achievement_drive == 0.9

    @pytest.mark.asyncio
    async def test_load_big_five_profile(self, loader):
        """测试加载大五人格"""
        result = await loader.load("elon")
        big_five = result["big_five"]
        assert isinstance(big_five, BigFiveProfile)
        assert big_five.openness == 0.8

    @pytest.mark.asyncio
    async def test_load_enneagram_profile(self, loader):
        """测试加载九型人格"""
        result = await loader.load("elon")
        enneagram = result["enneagram"]
        assert isinstance(enneagram, EnneagramProfile)
        assert enneagram.type8 == 0.4

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, loader):
        """测试加载不存在的角色"""
        with pytest.raises(ValueError):
            await loader.load("nonexistent")

    @pytest.mark.asyncio
    async def test_load_custom_character(self, store):
        """测试加载自定义角色"""
        store.create(
            character_id="custom",
            name="自定义角色",
            personality={"curiosity": 0.95},
        )
        loader = CharacterLoader(store=store)
        result = await loader.load("custom")
        assert result["name"] == "自定义角色"
        assert result["personality"].curiosity == 0.95