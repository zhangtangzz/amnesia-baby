import pytest
from src.vector.ranker import SearchRanker


class TestSearchRanker:
    """SearchRanker 测试"""

    @pytest.fixture
    def ranker(self):
        """创建 ranker 实例"""
        return SearchRanker()

    def test_ranker_initialization(self, ranker):
        """测试 ranker 初始化"""
        assert ranker is not None
        assert hasattr(ranker, 'rank')

    def test_rank_by_score(self, ranker):
        """测试按分数排序"""
        results = [
            {"id": "doc1", "score": 0.8},
            {"id": "doc2", "score": 0.9},
            {"id": "doc3", "score": 0.7},
        ]
        ranked = ranker.rank(results)
        assert ranked[0]["id"] == "doc2"
        assert ranked[1]["id"] == "doc1"
        assert ranked[2]["id"] == "doc3"

    def test_rank_with_threshold(self, ranker):
        """测试带阈值的排序"""
        results = [
            {"id": "doc1", "score": 0.8},
            {"id": "doc2", "score": 0.9},
            {"id": "doc3", "score": 0.3},
        ]
        ranked = ranker.rank(results, threshold=0.5)
        assert len(ranked) == 2
        assert all(r["score"] >= 0.5 for r in ranked)

    def test_rank_empty_results(self, ranker):
        """测试空结果排序"""
        results = []
        ranked = ranker.rank(results)
        assert len(ranked) == 0

    def test_rank_with_top_k(self, ranker):
        """测试限制返回数量"""
        results = [
            {"id": "doc1", "score": 0.8},
            {"id": "doc2", "score": 0.9},
            {"id": "doc3", "score": 0.7},
        ]
        ranked = ranker.rank(results, top_k=2)
        assert len(ranked) == 2
