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


class TestMemoryHistoryAPI:
    """对话历史 API 测试"""

    @pytest.fixture(autouse=True)
    def cleanup_memory(self):
        """每个测试前清空记忆"""
        from src.memory.shared_service import get_shared_memory_service
        svc = get_shared_memory_service()
        svc.short_term_memory.clear()
        svc.long_term_memory.clear()
        svc._save_to_file()
        yield
        svc.short_term_memory.clear()
        svc.long_term_memory.clear()
        svc._save_to_file()

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def _add_test_memories(self, client):
        """添加测试记忆"""
        for content, cid in [
            ("用户: 你好", "test_hist"),
            ("助手: 你好！我是测试", "test_hist"),
            ("用户: 今天天气怎样", "test_hist"),
            ("助手: 今天天气不错", "test_hist"),
            ("用户: 别的角色消息", "other_char"),
        ]:
            client.post("/api/memory/add", json={
                "character_id": cid,
                "content": content,
                "memory_type": "conversation",
                "importance": 0.5,
            })

    def test_list_characters_with_memory(self, client):
        """测试列出有记忆的角色"""
        self._add_test_memories(client)
        response = client.get("/api/memory/list")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        characters = data["data"]["characters"]
        cids = [c["character_id"] for c in characters]
        assert "test_hist" in cids
        assert "other_char" in cids

    def test_list_characters_count(self, client):
        """测试角色记忆条数"""
        self._add_test_memories(client)
        response = client.get("/api/memory/list")
        characters = response.json()["data"]["characters"]
        for c in characters:
            if c["character_id"] == "test_hist":
                assert c["count"] == 4
            elif c["character_id"] == "other_char":
                assert c["count"] == 1

    def test_get_history(self, client):
        """测试获取角色对话历史"""
        self._add_test_memories(client)
        response = client.get("/api/memory/history/test_hist")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["character_id"] == "test_hist"
        assert data["data"]["count"] == 4
        # 应包含对话内容
        contents = [h["content"] for h in data["data"]["history"]]
        assert any("你好" in c for c in contents)

    def test_get_history_empty(self, client):
        """测试获取不存在角色的历史"""
        response = client.get("/api/memory/history/nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["count"] == 0

    def test_clear_history(self, client):
        """测试清空角色历史"""
        self._add_test_memories(client)
        # 确认有记忆
        response = client.get("/api/memory/history/test_hist")
        assert response.json()["data"]["count"] == 4

        # 清空
        response = client.delete("/api/memory/test_hist")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["removed_count"] == 4

        # 验证已清空
        response = client.get("/api/memory/history/test_hist")
        assert response.json()["data"]["count"] == 0

        # 其他角色不受影响
        response = client.get("/api/memory/history/other_char")
        assert response.json()["data"]["count"] == 1

    def test_clear_history_nonexistent(self, client):
        """测试清空不存在角色的历史"""
        response = client.delete("/api/memory/nonexistent_999")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["removed_count"] == 0
