"""
LLM 集成测试

测试完整 LLM 流水线：路由器 → 提供商 → 重试 → Token统计
"""
import pytest
from unittest.mock import patch
from src.api.app import app
from fastapi.testclient import TestClient


class TestLLMPipeline:
    """LLM 集成测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def _mock_settings(self):
        """创建 mock 设置对象（所有 key 为空）"""
        return type("S", (), {
            "llm_provider": "openai",
            "llm_model": "gpt-3.5-turbo",
            "llm_max_retries": 3,
            "llm_fallback_provider": "",
            "openai_api_key": "",
            "deepseek_api_key": "",
            "qwen_api_key": "",
            "xiaomi_api_key": "",
            "xiaomi_api_base": "https://token-plan-cn.xiaomimimo.com/anthropic",
            "xiaomi_model": "mimo-v2.5-pro",
        })()

    def test_chat_mock_mode(self, client):
        """测试聊天 mock 模式（无 API Key 时返回 mock）"""
        with patch("src.api.routes.chat.get_settings") as mock_settings:
            mock_settings.return_value = self._mock_settings()

            response = client.post("/api/chat/send", json={
                "character_id": "elon",
                "message": "你好",
            })
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "reply" in data["data"]
            assert data["data"]["provider"] == "mock"

    def test_chat_with_provider_param(self, client):
        """测试指定 provider 参数（mock 模式）"""
        with patch("src.api.routes.chat.get_settings") as mock_settings:
            mock_settings.return_value = self._mock_settings()

            response = client.post("/api/chat/send", json={
                "character_id": "elon",
                "message": "你好",
                "provider": "deepseek",
            })
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["provider"] == "mock"

    def test_token_stats_endpoint(self, client):
        """测试 token 统计接口"""
        response = client.get("/api/chat/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_full_pipeline_with_mock_llm(self, client):
        """测试完整流水线（mock 模式）"""
        # 1. 健康检查
        health = client.get("/health")
        assert health.status_code == 200

        # 2. 发送聊天消息
        with patch("src.api.routes.chat.get_settings") as mock_settings:
            mock_settings.return_value = self._mock_settings()

            chat_response = client.post("/api/chat/send", json={
                "character_id": "elon",
                "message": "你为什么喜欢创业？",
            })
            assert chat_response.status_code == 200
            chat_data = chat_response.json()
            assert chat_data["success"] is True
            assert "reply" in chat_data["data"]

        # 3. 获取统计
        stats = client.get("/api/chat/stats")
        assert stats.status_code == 200
