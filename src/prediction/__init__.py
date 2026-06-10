"""
行为预测模块

基于人格画像预测角色在不同场景下的行为倾向
"""

from .models import ScenarioType, BehaviorPrediction
from .predictor import BehaviorPredictor

__all__ = [
    "ScenarioType",
    "BehaviorPrediction",
    "BehaviorPredictor",
]
