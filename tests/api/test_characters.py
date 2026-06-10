"""
角色管理 API 测试
"""
import pytest
from src.api.app import app
from fastapi.testclient import TestClient


class TestCharactersAPI:
    """角色管理 API 测试"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_list_characters(self, client):
        """测试列出角色"""
        response = client.get("/api/characters/list")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 2  # 默认角色

    def test_get_character(self, client):
        """测试获取角色"""
        response = client.get("/api/characters/elon")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Elon Musk"

    def test_get_nonexistent(self, client):
        """测试获取不存在的角色"""
        response = client.get("/api/characters/nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False

    def test_create_character(self, client):
        """测试创建角色"""
        import time
        uid = "test_" + str(int(time.time() * 1000))[-6:]
        response = client.post("/api/characters/create", json={
            "character_id": uid,
            "name": "新角色",
            "avatar": "🎭",
            "description": "测试新建角色",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "新角色"

    def test_create_duplicate(self, client):
        """测试创建重复角色"""
        client.post("/api/characters/create", json={
            "character_id": "dup_test",
            "name": "角色A",
        })
        response = client.post("/api/characters/create", json={
            "character_id": "dup_test",
            "name": "角色B",
        })
        data = response.json()
        assert data["success"] is False

    def test_delete_character(self, client):
        """测试删除角色"""
        # 先创建
        client.post("/api/characters/create", json={
            "character_id": "to_delete",
            "name": "待删除",
        })
        # 再删除
        response = client.delete("/api/characters/to_delete")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCharacterUpdate:
    """角色编辑 API 测试"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_update_character_name(self, client):
        """测试更新角色名称"""
        # 先创建
        client.post("/api/characters/create", json={
            "character_id": "edit_test",
            "name": "原始名称",
            "avatar": "😊",
            "description": "原始描述",
        })
        # 更新名称
        response = client.put("/api/characters/edit_test", json={
            "name": "新名称",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "新名称"
        # 未修改的字段保持不变
        assert data["data"]["avatar"] == "😊"

    def test_update_character_avatar(self, client):
        """测试更新角色头像"""
        client.post("/api/characters/create", json={
            "character_id": "avatar_test",
            "name": "头像测试",
        })
        response = client.put("/api/characters/avatar_test", json={
            "avatar": "🚀",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["avatar"] == "🚀"

    def test_update_character_description(self, client):
        """测试更新角色描述"""
        client.post("/api/characters/create", json={
            "character_id": "desc_test",
            "name": "描述测试",
        })
        response = client.put("/api/characters/desc_test", json={
            "description": "全新的描述内容",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["description"] == "全新的描述内容"

    def test_update_multiple_fields(self, client):
        """测试同时更新多个字段"""
        client.post("/api/characters/create", json={
            "character_id": "multi_edit",
            "name": "原始",
            "avatar": "😊",
        })
        response = client.put("/api/characters/multi_edit", json={
            "name": "更新后",
            "avatar": "🌟",
            "description": "新描述",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "更新后"
        assert data["data"]["avatar"] == "🌟"
        assert data["data"]["description"] == "新描述"

    def test_update_nonexistent_character(self, client):
        """测试更新不存在的角色"""
        response = client.put("/api/characters/nonexistent_999", json={
            "name": "不存在",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "不存在" in data["message"]

    def test_update_preserves_personality(self, client):
        """测试更新不影响人格数据"""
        client.post("/api/characters/create", json={
            "character_id": "personality_preserve",
            "name": "人格测试",
            "personality": {"achievement_drive": 0.9},
        })
        response = client.put("/api/characters/personality_preserve", json={
            "name": "新名字",
        })
        data = response.json()
        assert data["success"] is True
        assert data["data"]["personality"]["achievement_drive"] == 0.9

    def test_update_default_character(self, client):
        """测试更新默认角色"""
        response = client.put("/api/characters/elon", json={
            "description": "更新了 Elon 的描述",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["description"] == "更新了 Elon 的描述"
