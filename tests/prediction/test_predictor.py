"""
行为预测测试
"""
import pytest
from src.prediction.predictor import BehaviorPredictor
from src.prediction.models import ScenarioType
from src.personality.profile import PersonalityProfile


class TestBehaviorPredictor:
    """BehaviorPredictor 测试"""

    @pytest.fixture
    def predictor(self):
        return BehaviorPredictor()

    @pytest.fixture
    def elon_profile(self):
        """Elon-like 高成就、高风险、高好奇心"""
        return PersonalityProfile(
            achievement_drive=0.9,
            curiosity=0.85,
            risk_preference=0.85,
            security_need=0.2,
            dominance=0.8,
            empathy=0.4,
            independence=0.9,
            responsibility=0.7,
            creativity=0.8,
            social_need=0.6,
        )

    @pytest.fixture
    def cautious_profile(self):
        """保守型人格：低风险、高安全、高责任"""
        return PersonalityProfile(
            achievement_drive=0.5,
            curiosity=0.3,
            risk_preference=0.2,
            security_need=0.9,
            dominance=0.3,
            empathy=0.7,
            independence=0.3,
            responsibility=0.9,
            creativity=0.3,
            social_need=0.4,
        )

    def test_predict_risk_decision(self, predictor, elon_profile):
        """测试风险决策场景"""
        result = predictor.predict(elon_profile, ScenarioType.RISK_DECISION)
        assert result.scenario == ScenarioType.RISK_DECISION
        assert 0.0 <= result.tendency <= 1.0
        assert result.confidence > 0
        assert len(result.description) > 0
        assert len(result.reasoning) > 0

    def test_predict_social_interaction(self, predictor, elon_profile):
        """测试社交互动场景"""
        result = predictor.predict(elon_profile, ScenarioType.SOCIAL_INTERACTION)
        assert result.scenario == ScenarioType.SOCIAL_INTERACTION
        assert 0.0 <= result.tendency <= 1.0

    def test_predict_conflict_resolution(self, predictor, elon_profile):
        """测试冲突处理场景"""
        result = predictor.predict(elon_profile, ScenarioType.CONFLICT_RESOLUTION)
        assert result.scenario == ScenarioType.CONFLICT_RESOLUTION

    def test_predict_creative_problem(self, predictor, elon_profile):
        """测试创意问题场景"""
        result = predictor.predict(elon_profile, ScenarioType.CREATIVE_PROBLEM)
        assert result.scenario == ScenarioType.CREATIVE_PROBLEM

    def test_predict_leadership(self, predictor, elon_profile):
        """测试领导力场景"""
        result = predictor.predict(elon_profile, ScenarioType.LEADERSHIP)
        assert result.scenario == ScenarioType.LEADERSHIP

    def test_predict_stress_response(self, predictor, elon_profile):
        """测试压力应对场景"""
        result = predictor.predict(elon_profile, ScenarioType.STRESS_RESPONSE)
        assert result.scenario == ScenarioType.STRESS_RESPONSE

    def test_high_risk_profile_takes_risks(self, predictor, elon_profile):
        """高风险偏好 → 倾向冒险"""
        result = predictor.predict(elon_profile, ScenarioType.RISK_DECISION)
        assert result.tendency > 0.6  # 应该倾向冒险

    def test_cautious_profile_avoids_risks(self, predictor, cautious_profile):
        """保守型 → 倾向规避风险"""
        result = predictor.predict(cautious_profile, ScenarioType.RISK_DECISION)
        assert result.tendency < 0.4  # 应该倾向保守

    def test_high_dominance_takes_lead(self, predictor, elon_profile):
        """高支配性 → 倾向领导"""
        result = predictor.predict(elon_profile, ScenarioType.LEADERSHIP)
        assert result.tendency > 0.6

    def test_low_dominance_defers(self, predictor, cautious_profile):
        """低支配性 → 倾向跟随（不高于0.55）"""
        result = predictor.predict(cautious_profile, ScenarioType.LEADERSHIP)
        assert result.tendency <= 0.55

    def test_predict_all_scenarios(self, predictor, elon_profile):
        """测试所有场景类型"""
        for scenario in ScenarioType:
            result = predictor.predict(elon_profile, scenario)
            assert result is not None
            assert 0.0 <= result.tendency <= 1.0
            assert result.confidence > 0

    def test_default_profile_returns_neutral(self, predictor):
        """默认人格应返回中性预测"""
        default = PersonalityProfile()  # 全部 0.5
        result = predictor.predict(default, ScenarioType.RISK_DECISION)
        assert 0.3 <= result.tendency <= 0.7  # 接近中性


class TestBehaviorPredictionAll:
    """批量预测测试"""

    @pytest.fixture
    def predictor(self):
        return BehaviorPredictor()

    def test_predict_all_returns_all_scenarios(self, predictor):
        """测试 predict_all 返回所有场景"""
        profile = PersonalityProfile(achievement_drive=0.8, curiosity=0.7)
        results = predictor.predict_all(profile)
        assert len(results) == len(ScenarioType)
        scenarios_returned = {r.scenario for r in results}
        assert scenarios_returned == set(ScenarioType)

    def test_predict_all_sorted_by_tendency(self, predictor):
        """测试 predict_all 按倾向度排序"""
        profile = PersonalityProfile(
            risk_preference=0.9, dominance=0.9,
            creativity=0.9, empathy=0.9,
        )
        results = predictor.predict_all(profile)
        tendencies = [r.tendency for r in results]
        assert tendencies == sorted(tendencies, reverse=True)
