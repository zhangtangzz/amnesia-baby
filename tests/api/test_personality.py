import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestPersonalityAPI:
    """人格API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_analyze_personality(self, client):
        """测试人格分析"""
        request_data = {
            "text": "张三追求成功，勇于冒险创新",
            "source": "采访视频"
        }
        response = client.post("/api/personality/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_analyze_personality_empty_text(self, client):
        """测试空文本人格分析"""
        request_data = {
            "text": "",
            "source": "采访视频"
        }
        response = client.post("/api/personality/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_personality_profile(self, client):
        """测试获取人格画像"""
        response = client.get("/api/personality/profile/test_char")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
