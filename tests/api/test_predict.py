"""
行为预测 API 测试
"""
import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestPredictAPI:
    """行为预测 API 测试"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_predict_endpoint_exists(self, client):
        """测试预测端点存在"""
        response = client.post("/api/predict", json={
            "personality": {
                "achievement_drive": 0.9,
                "curiosity": 0.8,
                "risk_preference": 0.85,
            },
            "scenario": "risk_decision",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_predict_returns_tendency(self, client):
        """测试返回倾向度"""
        response = client.post("/api/predict", json={
            "personality": {"risk_preference": 0.9},
            "scenario": "risk_decision",
        })
        data = response.json()
        assert "tendency" in data["data"]
        assert 0.0 <= data["data"]["tendency"] <= 1.0

    def test_predict_all_scenarios(self, client):
        """测试预测所有场景"""
        response = client.post("/api/predict/all", json={
            "personality": {
                "achievement_drive": 0.8,
                "curiosity": 0.7,
            },
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["predictions"]) == 6

    def test_predict_with_character_id(self, client):
        """测试通过角色ID预测"""
        response = client.post("/api/predict", json={
            "character_id": "elon",
            "scenario": "leadership",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_predict_invalid_scenario(self, client):
        """测试无效场景"""
        response = client.post("/api/predict", json={
            "personality": {"achievement_drive": 0.8},
            "scenario": "invalid_scenario",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
