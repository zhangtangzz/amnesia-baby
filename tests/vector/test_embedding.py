import pytest
from src.vector.embedding import EmbeddingService


class TestEmbeddingService:
    """EmbeddingService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return EmbeddingService()

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'embed')

    def test_embed_returns_vector(self, service):
        """测试向量化返回向量"""
        text = "清华大学毕业"
        result = service.embed(text)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_embed_consistency(self, service):
        """测试向量化一致性"""
        text = "清华大学毕业"
        result1 = service.embed(text)
        result2 = service.embed(text)
        assert result1 == result2

    def test_embed_different_texts(self, service):
        """测试不同文本向量化"""
        text1 = "清华大学毕业"
        text2 = "创业成功"
        result1 = service.embed(text1)
        result2 = service.embed(text2)
        assert result1 != result2

    def test_embed_empty_text(self, service):
        """测试空文本向量化"""
        text = ""
        result = service.embed(text)
        assert isinstance(result, list)
