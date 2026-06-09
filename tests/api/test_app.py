import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestAPIApp:
    """API应用测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_app_initialization(self, client):
        """测试应用初始化"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "失忆宝宝 API"}

    def test_health_check(self, client):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_docs_endpoint(self, client):
        """测试文档端点"""
        response = client.get("/docs")
        assert response.status_code == 200
