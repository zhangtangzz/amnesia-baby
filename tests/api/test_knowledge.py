import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestKnowledgeAPI:
    """知识库API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_process_knowledge(self, client):
        """测试处理知识"""
        request_data = {
            "text": "张三毕业于清华大学，创立了某科技公司",
            "source": "采访视频",
            "character_id": "test_char"
        }
        response = client.post("/api/knowledge/process", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_query_knowledge(self, client):
        """测试查询知识"""
        response = client.get("/api/knowledge/query/test_char?keyword=清华")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_knowledge_base(self, client):
        """测试获取知识库"""
        response = client.get("/api/knowledge/base/test_char")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
