"""
LLM 路由器

负责根据配置选择和切换 LLM 提供商
"""

from typing import List, Dict, Optional, Any
from .base import LLMProvider
from .models import LLMResponse


# 提供商注册表
_PROVIDER_REGISTRY: Dict[str, type] = {}


def _register_defaults():
    """注册默认提供商"""
    from .openai_provider import OpenAIProvider
    from .deepseek_provider import DeepSeekProvider
    from .qwen_provider import QwenProvider

    _PROVIDER_REGISTRY["openai"] = OpenAIProvider
    _PROVIDER_REGISTRY["deepseek"] = DeepSeekProvider
    _PROVIDER_REGISTRY["qwen"] = QwenProvider


class LLMRouter:
    """
    LLM 路由器

    根据配置创建和管理 LLM 提供商实例
    """

    def __init__(
        self,
        default_provider: str = "openai",
        api_key: str = "",
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs,
    ):
        """
        初始化路由器

        Args:
            default_provider: 默认提供商名称
            api_key: API Key
            base_url: 自定义 Base URL
            model: 自定义模型
        """
        if not _PROVIDER_REGISTRY:
            _register_defaults()

        self._default_provider = default_provider
        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        self._kwargs = kwargs
        self._current_provider: Optional[LLMProvider] = None

    def get_provider(self, provider_name: Optional[str] = None) -> LLMProvider:
        """
        获取提供商实例

        Args:
            provider_name: 提供商名称，None 则使用当前

        Returns:
            LLMProvider 实例
        """
        name = provider_name or self._default_provider

        if name not in _PROVIDER_REGISTRY:
            raise ValueError(f"Unknown provider: {name}. Available: {list(_PROVIDER_REGISTRY.keys())}")

        provider_cls = _PROVIDER_REGISTRY[name]

        init_kwargs: Dict[str, Any] = {"api_key": self._api_key}
        if self._base_url:
            init_kwargs["base_url"] = self._base_url
        if self._model:
            init_kwargs["model"] = self._model

        return provider_cls(**init_kwargs)

    def get_provider_name(self) -> str:
        """获取当前提供商名称"""
        return self._default_provider

    def switch_provider(self, provider_name: str):
        """
        切换提供商

        Args:
            provider_name: 提供商名称

        Raises:
            ValueError: 未知提供商
        """
        if provider_name not in _PROVIDER_REGISTRY:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(_PROVIDER_REGISTRY.keys())}")
        self._default_provider = provider_name
        self._current_provider = None

    async def generate(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """
        生成回复

        Args:
            messages: 消息列表
            provider: 指定提供商（覆盖默认）
            model: 指定模型
            temperature: 温度
            max_tokens: 最大 token 数

        Returns:
            LLMResponse
        """
        p = self.get_provider(provider)
        return await p.generate(messages, model=model, temperature=temperature, max_tokens=max_tokens)

    @staticmethod
    def list_providers() -> List[str]:
        """列出所有可用提供商"""
        if not _PROVIDER_REGISTRY:
            _register_defaults()
        return list(_PROVIDER_REGISTRY.keys())
