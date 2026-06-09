"""
应用配置管理
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # LLM 提供商配置
    llm_provider: str = "openai"
    llm_model: str = "gpt-3.5-turbo"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 500
    llm_max_retries: int = 3
    llm_fallback_provider: str = ""

    # OpenAI 配置
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"

    # DeepSeek 配置
    deepseek_api_key: str = ""
    deepseek_api_base: str = "https://api.deepseek.com/v1"

    # Qwen 配置
    qwen_api_key: str = ""
    qwen_api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 小米 MIMO 配置
    xiaomi_api_key: str = ""
    xiaomi_api_base: str = "https://token-plan-cn.xiaomimimo.com/anthropic"
    xiaomi_model: str = "mimo-v2.5-pro"

    # 应用配置
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置（缓存）"""
    return Settings()