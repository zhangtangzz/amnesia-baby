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
        response = client.post("/api/characters/create", json={
            "character_id": "test_new",
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
