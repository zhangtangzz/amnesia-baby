"""
行为预测器

基于人格画像的 10 个维度，在不同场景下预测角色行为倾向
"""

from typing import List
from ..personality.profile import PersonalityProfile
from .models import ScenarioType, BehaviorPrediction


class BehaviorPredictor:
    """
    行为预测器

    使用加权公式将人格特质映射到场景行为倾向
    """

    # 每种场景使用的人格维度权重
    # 正权重：该特质越高，倾向值越高
    # 负权重：该特质越高，倾向值越低
    SCENARIO_WEIGHTS = {
        ScenarioType.RISK_DECISION: {
            "risk_preference": 0.4,
            "curiosity": 0.2,
            "achievement_drive": 0.2,
            "security_need": -0.3,
            "responsibility": -0.1,
        },
        ScenarioType.SOCIAL_INTERACTION: {
            "social_need": 0.35,
            "empathy": 0.25,
            "dominance": 0.15,
            "independence": -0.1,
        },
        ScenarioType.CONFLICT_RESOLUTION: {
            "empathy": 0.3,
            "dominance": 0.25,
            "independence": 0.15,
            "responsibility": 0.15,
            "risk_preference": 0.1,
        },
        ScenarioType.CREATIVE_PROBLEM: {
            "creativity": 0.35,
            "curiosity": 0.3,
            "independence": 0.15,
            "risk_preference": 0.1,
            "security_need": -0.1,
        },
        ScenarioType.LEADERSHIP: {
            "dominance": 0.35,
            "achievement_drive": 0.25,
            "responsibility": 0.15,
            "social_need": 0.1,
            "empathy": 0.1,
        },
        ScenarioType.STRESS_RESPONSE: {
            "security_need": 0.3,
            "responsibility": 0.2,
            "independence": 0.15,
            "risk_preference": -0.15,
            "dominance": 0.1,
        },
    }

    # 场景描述模板
    SCENARIO_DESCRIPTIONS = {
        ScenarioType.RISK_DECISION: {
            "high": "倾向于大胆冒险，愿意承担高风险以追求高回报",
            "mid": "在评估风险后谨慎行动，寻求平衡",
            "low": "倾向保守稳健，优先规避风险",
        },
        ScenarioType.SOCIAL_INTERACTION: {
            "high": "主动社交，乐于建立广泛的人际网络",
            "mid": "根据需要参与社交，保持适度互动",
            "low": "偏好独处，减少不必要的社交活动",
        },
        ScenarioType.CONFLICT_RESOLUTION: {
            "high": "直面冲突，积极沟通寻求解决方案",
            "mid": "根据情况选择对抗或妥协",
            "low": "倾向回避冲突，寻求和谐",
        },
        ScenarioType.CREATIVE_PROBLEM: {
            "high": "跳出常规思维，提出创新性解决方案",
            "mid": "在传统方法基础上适当创新",
            "low": "倾向使用经过验证的方法",
        },
        ScenarioType.LEADERSHIP: {
            "high": "主动承担领导角色，推动团队前进",
            "mid": "在需要时承担领导职责",
            "low": "倾向配合他人，做好支持角色",
        },
        ScenarioType.STRESS_RESPONSE: {
            "high": "在压力下保持冷静，坚持既定方向",
            "mid": "压力下会调整策略但不放弃目标",
            "low": "压力下倾向寻求安全方案或外部帮助",
        },
    }

    def predict(
        self,
        personality: PersonalityProfile,
        scenario: ScenarioType,
    ) -> BehaviorPrediction:
        """
        预测单一场景下的行为倾向

        Args:
            personality: 人格画像
            scenario: 场景类型

        Returns:
            BehaviorPrediction: 预测结果
        """
        weights = self.SCENARIO_WEIGHTS[scenario]

        # 加权计算倾向值
        # 正权重：特质越高 → 倾向越高
        # 负权重：特质越高 → 倾向越低（反转贡献）
        weighted_sum = 0.0
        total_weight = 0.0
        reasoning_parts = []

        traits = personality.model_dump()
        for trait_name, weight in weights.items():
            value = traits.get(trait_name, 0.5)
            # 负权重时反转：高特质值反而降低倾向
            if weight >= 0:
                contribution = value * weight
            else:
                contribution = (1 - value) * abs(weight)
            weighted_sum += contribution
            total_weight += abs(weight)
            reasoning_parts.append(f"{trait_name}={value:.1f}×{weight:+.2f}")

        # 归一化到 0~1
        if total_weight > 0:
            tendency = weighted_sum / total_weight
        else:
            tendency = 0.5

        # 确保在范围内
        tendency = max(0.0, min(1.0, tendency))

        # 计算置信度（人格特质越极端，置信度越高）
        extremeness = sum(abs(v - 0.5) for v in traits.values()) / len(traits)
        confidence = min(1.0, 0.5 + extremeness)

        # 生成描述
        descriptions = self.SCENARIO_DESCRIPTIONS[scenario]
        if tendency > 0.6:
            description = descriptions["high"]
        elif tendency < 0.4:
            description = descriptions["low"]
        else:
            description = descriptions["mid"]

        reasoning = "人格权重分析: " + ", ".join(reasoning_parts)

        return BehaviorPrediction(
            scenario=scenario,
            tendency=round(tendency, 3),
            confidence=round(confidence, 3),
            description=description,
            reasoning=reasoning,
        )

    def predict_all(
        self,
        personality: PersonalityProfile,
    ) -> List[BehaviorPrediction]:
        """
        预测所有场景的行为倾向

        Args:
            personality: 人格画像

        Returns:
            List[BehaviorPrediction]: 按倾向度降序排列的预测结果
        """
        results = []
        for scenario in ScenarioType:
            result = self.predict(personality, scenario)
            results.append(result)

        # 按倾向度降序排列
        results.sort(key=lambda r: r.tendency, reverse=True)
        return results
