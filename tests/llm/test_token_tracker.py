"""
Token 统计器测试
"""
import pytest
from src.llm.token_tracker import TokenTracker
from src.llm.models import TokenUsage


class TestTokenTracker:
    """TokenTracker 测试"""

    def test_initialization(self):
        """测试初始化"""
        tracker = TokenTracker()
        assert tracker.total_prompt_tokens == 0
        assert tracker.total_completion_tokens == 0
        assert tracker.total_tokens == 0
        assert tracker.call_count == 0

    def test_record_usage(self):
        """测试记录 token 使用"""
        tracker = TokenTracker()
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        tracker.record(usage, provider="openai", model="gpt-3.5-turbo")

        assert tracker.total_prompt_tokens == 100
        assert tracker.total_completion_tokens == 50
        assert tracker.total_tokens == 150
        assert tracker.call_count == 1

    def test_record_multiple(self):
        """测试多次记录"""
        tracker = TokenTracker()
        tracker.record(TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150))
        tracker.record(TokenUsage(prompt_tokens=200, completion_tokens=80, total_tokens=280))

        assert tracker.total_tokens == 430
        assert tracker.call_count == 2

    def test_get_history(self):
        """测试获取历史记录"""
        tracker = TokenTracker()
        tracker.record(TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150), provider="openai")
        tracker.record(TokenUsage(prompt_tokens=200, completion_tokens=80, total_tokens=280), provider="deepseek")

        history = tracker.get_history()
        assert len(history) == 2
        assert history[0]["provider"] == "openai"
        assert history[1]["provider"] == "deepseek"

    def test_reset(self):
        """测试重置"""
        tracker = TokenTracker()
        tracker.record(TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150))
        tracker.reset()

        assert tracker.total_tokens == 0
        assert tracker.call_count == 0
        assert len(tracker.get_history()) == 0

    def test_summary(self):
        """测试摘要"""
        tracker = TokenTracker()
        tracker.record(TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150))
        tracker.record(TokenUsage(prompt_tokens=200, completion_tokens=80, total_tokens=280))

        summary = tracker.summary()
        assert summary["total_tokens"] == 430
        assert summary["call_count"] == 2
        assert summary["avg_tokens_per_call"] == 215.0
