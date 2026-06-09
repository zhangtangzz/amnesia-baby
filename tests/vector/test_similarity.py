import pytest
from src.vector.similarity import SimilarityCalculator


class TestSimilarityCalculator:
    """SimilarityCalculator 测试"""

    @pytest.fixture
    def calculator(self):
        """创建 calculator 实例"""
        return SimilarityCalculator()

    def test_cosine_similarity(self, calculator):
        """测试余弦相似度"""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        similarity = calculator.cosine_similarity(vec1, vec2)
        assert similarity == 1.0

    def test_cosine_similarity_orthogonal(self, calculator):
        """测试正交向量余弦相似度"""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        similarity = calculator.cosine_similarity(vec1, vec2)
        assert similarity == 0.0

    def test_cosine_similarity_opposite(self, calculator):
        """测试相反向量余弦相似度"""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [-1.0, 0.0, 0.0]
        similarity = calculator.cosine_similarity(vec1, vec2)
        assert similarity == -1.0

    def test_euclidean_distance(self, calculator):
        """测试欧氏距离"""
        vec1 = [0.0, 0.0]
        vec2 = [3.0, 4.0]
        distance = calculator.euclidean_distance(vec1, vec2)
        assert distance == 5.0

    def test_manhattan_distance(self, calculator):
        """测试曼哈顿距离"""
        vec1 = [0.0, 0.0]
        vec2 = [3.0, 4.0]
        distance = calculator.manhattan_distance(vec1, vec2)
        assert distance == 7.0
