"""
LLM 数据模型
"""

from pydantic import BaseModel, model_validator
from typing import Optional


class TokenUsage(BaseModel):
    """Token 使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @model_validator(mode="after")
    def auto_calculate_total(self):
        """自动计算 total_tokens"""
        if self.total_tokens == 0 and (self.prompt_tokens > 0 or self.completion_tokens > 0):
            self.total_tokens = self.prompt_tokens + self.completion_tokens
        return self


class LLMResponse(BaseModel):
    """LLM 响应"""
    content: str
    provider: str
    model: str
    usage: TokenUsage = TokenUsage()
    finish_reason: Optional[str] = None
