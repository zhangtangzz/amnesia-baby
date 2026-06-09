"""
Token 使用统计器

统计每次 LLM 调用的 token 用量
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import TokenUsage


class TokenTracker:
    """
    Token 使用统计器

    记录和统计 LLM 调用的 token 用量
    """

    def __init__(self):
        """初始化"""
        self.total_prompt_tokens: int = 0
        self.total_completion_tokens: int = 0
        self.total_tokens: int = 0
        self.call_count: int = 0
        self._history: List[Dict[str, Any]] = []

    def record(
        self,
        usage: TokenUsage,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        记录一次 token 使用

        Args:
            usage: Token 使用量
            provider: 提供商名称
            model: 模型名称
        """
        self.total_prompt_tokens += usage.prompt_tokens
        self.total_completion_tokens += usage.completion_tokens
        self.total_tokens += usage.total_tokens
        self.call_count += 1

        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        })

    def get_history(self) -> List[Dict[str, Any]]:
        """获取历史记录"""
        return list(self._history)

    def summary(self) -> Dict[str, Any]:
        """
        获取统计摘要

        Returns:
            Dict: 包含统计信息
        """
        avg = self.total_tokens / self.call_count if self.call_count > 0 else 0.0
        return {
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens,
            "call_count": self.call_count,
            "avg_tokens_per_call": avg,
        }

    def reset(self):
        """重置统计"""
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.call_count = 0
        self._history.clear()
