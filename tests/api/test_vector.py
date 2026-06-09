import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestVectorAPI:
    """向量检索API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_add_document(self, client):
        """测试添加文档"""
        request_data = {
            "text": "张三毕业于清华大学",
            "metadata": {"source": "采访"}
        }
        response = client.post("/api/vector/add", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_search_documents(self, client):
        """测试搜索文档"""
        request_data = {
            "query": "清华",
            "top_k": 5
        }
        response = client.post("/api/vector/search", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_vector_count(self, client):
        """测试获取向量数量"""
        response = client.get("/api/vector/count")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
