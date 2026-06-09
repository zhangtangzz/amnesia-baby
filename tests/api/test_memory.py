import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestMemoryAPI:
    """记忆API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_add_memory(self, client):
        """测试添加记忆"""
        request_data = {
            "character_id": "elon",
            "content": "用户喜欢SpaceX",
            "memory_type": "conversation",
            "importance": 0.8
        }
        response = client.post("/api/memory/add", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_context(self, client):
        """测试获取上下文"""
        response = client.get("/api/memory/context/elon?current_message=你好")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_consolidate_memories(self, client):
        """测试巩固记忆"""
        response = client.post("/api/memory/consolidate/elon")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
