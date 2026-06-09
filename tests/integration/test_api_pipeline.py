import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestAPIPipeline:
    """API流水线集成测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_full_api_pipeline(self, client):
        """测试完整API流水线"""
        # 1. 健康检查
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        # 2. 人格分析
        personality_request = {
            "text": "张三追求成功，勇于冒险创新",
            "source": "采访视频"
        }
        response = client.post("/api/personality/analyze", json=personality_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 3. 聊天
        chat_request = {
            "character_id": "elon",
            "message": "你好"
        }
        response = client.post("/api/chat/send", json=chat_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 4. 知识库处理
        knowledge_request = {
            "text": "张三毕业于清华大学，创立了某科技公司",
            "source": "采访视频",
            "character_id": "test_char"
        }
        response = client.post("/api/knowledge/process", json=knowledge_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 5. 添加记忆
        memory_request = {
            "character_id": "elon",
            "content": "用户喜欢SpaceX",
            "memory_type": "conversation",
            "importance": 0.8
        }
        response = client.post("/api/memory/add", json=memory_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 6. 向量检索
        vector_request = {
            "text": "张三毕业于清华大学",
            "metadata": {"source": "采访"}
        }
        response = client.post("/api/vector/add", json=vector_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # 7. 搜索向量
        search_request = {
            "query": "清华",
            "top_k": 5
        }
        response = client.post("/api/vector/search", json=search_request)
        assert response.status_code == 200
        assert response.json()["success"] is True
