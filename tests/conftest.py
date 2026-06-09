"""
pytest 配置和 fixtures
"""

import pytest
from src.config import Settings, get_settings


@pytest.fixture
def settings():
    """测试配置"""
    return Settings(
        openai_api_key="test-key",
        openai_api_base="http://localhost:8000",
        app_env="testing",
        app_debug=True,
    )


@pytest.fixture(autouse=True)
def override_settings(settings):
    """覆盖配置"""
    get_settings.cache_clear()
    return settings