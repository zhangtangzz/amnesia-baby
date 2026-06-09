"""
角色存储测试
"""
import pytest
from src.chat.character_store import CharacterStore


def make_store():
    """创建测试用 store（不持久化）"""
    return CharacterStore(persist=False)


class TestCharacterStore:
    """CharacterStore 测试"""

    def test_initialization(self):
        """测试初始化"""
        store = make_store()
        assert store.count() == 0

    def test_create_character(self):
        """测试创建角色"""
        store = make_store()
        char = store.create(
            character_id="test_char",
            name="测试角色",
            avatar="🧑",
            description="一个测试角色",
            personality={"achievement_drive": 0.8, "curiosity": 0.7},
        )
        assert char["character_id"] == "test_char"
        assert char["name"] == "测试角色"
        assert char["avatar"] == "🧑"

    def test_get_character(self):
        """测试获取角色"""
        store = make_store()
        store.create(character_id="c1", name="角色1", avatar="😊")
        char = store.get("c1")
        assert char is not None
        assert char["name"] == "角色1"

    def test_get_nonexistent_returns_none(self):
        """测试获取不存在的角色"""
        store = make_store()
        assert store.get("nonexistent") is None

    def test_list_characters(self):
        """测试列出所有角色"""
        store = make_store()
        store.create(character_id="c1", name="角色1", avatar="😊")
        store.create(character_id="c2", name="角色2", avatar="🚀")
        chars = store.list_all()
        assert len(chars) == 2

    def test_delete_character(self):
        """测试删除角色"""
        store = make_store()
        store.create(character_id="c1", name="角色1", avatar="😊")
        assert store.delete("c1") is True
        assert store.get("c1") is None
        assert store.count() == 0

    def test_delete_nonexistent_returns_false(self):
        """测试删除不存在的角色"""
        store = make_store()
        assert store.delete("nonexistent") is False

    def test_update_character(self):
        """测试更新角色"""
        store = make_store()
        store.create(character_id="c1", name="角色1", avatar="😊")
        updated = store.update("c1", name="新名字", avatar="🚀")
        assert updated["name"] == "新名字"
        assert updated["avatar"] == "🚀"

    def test_has_default_characters(self):
        """测试包含默认角色"""
        store = make_store()
        store.add_defaults()
        assert store.count() >= 2
        assert store.get("elon") is not None
