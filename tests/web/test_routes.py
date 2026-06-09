"""
Web 路由测试
"""
import pytest
from src.api.app import app
from fastapi.testclient import TestClient


class TestWebRoutes:
    """Web 页面路由测试"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_index_page(self, client):
        """测试首页可访问"""
        response = client.get("/")
        assert response.status_code == 200
        assert "失忆宝宝" in response.text or "text/html" in response.headers.get("content-type", "")

    def test_chat_page(self, client):
        """测试聊天页面"""
        response = client.get("/chat")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_knowledge_page(self, client):
        """测试知识库页面"""
        response = client.get("/knowledge")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_profile_page(self, client):
        """测试角色画像页面"""
        response = client.get("/profile")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_index_has_navigation(self, client):
        """测试首页包含导航"""
        response = client.get("/")
        assert "chat" in response.text
        assert "knowledge" in response.text
        assert "profile" in response.text

    def test_chat_has_input(self, client):
        """测试聊天页包含输入区域"""
        response = client.get("/chat")
        assert "message-input" in response.text
        assert "send-btn" in response.text

    def test_knowledge_has_form(self, client):
        """测试知识库页包含表单"""
        response = client.get("/knowledge")
        assert "knowledge-form" in response.text
        assert "k-text" in response.text

    def test_profile_has_display(self, client):
        """测试画像页包含展示区域"""
        response = client.get("/profile")
        assert "personality-traits" in response.text
        assert "big-five-chart" in response.text

    def test_static_css_accessible(self, client):
        """测试静态 CSS 可访问"""
        response = client.get("/static/css/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_static_js_accessible(self, client):
        """测试静态 JS 可访问"""
        response = client.get("/static/js/app.js")
        assert response.status_code == 200

    def test_api_still_works(self, client):
        """测试 API 路由仍然可用"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
