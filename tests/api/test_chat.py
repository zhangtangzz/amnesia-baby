import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestChatAPI:
    """聊天API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_chat(self, client):
        """测试聊天"""
        request_data = {
            "character_id": "elon",
            "message": "你好"
        }
        response = client.post("/api/chat/send", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_chat_history(self, client):
        """测试获取聊天历史"""
        response = client.get("/api/chat/history/test_char")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
