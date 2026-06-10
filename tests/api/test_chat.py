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


class TestChatStreamAPI:
    """聊天流式输出 API 测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_stream_endpoint_exists(self, client):
        """测试流式端点存在"""
        response = client.get(
            "/api/chat/stream",
            params={"character_id": "elon", "message": "你好"},
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_stream_returns_sse_events(self, client):
        """测试流式端点返回 SSE 事件格式"""
        response = client.get(
            "/api/chat/stream",
            params={"character_id": "elon", "message": "你好"},
        )
        assert response.status_code == 200
        content = response.text
        # 应包含 SSE 格式的 data: 行
        assert "data:" in content
        # 应包含结束标记
        assert "[DONE]" in content

    def test_stream_no_api_key_returns_mock(self, client):
        """测试无 API Key 时流式返回 mock 响应"""
        response = client.get(
            "/api/chat/stream",
            params={"character_id": "elon", "message": "测试"},
        )
        assert response.status_code == 200
        content = response.text
        # mock 模式也应该返回 SSE 格式
        assert "data:" in content
        assert "[DONE]" in content
