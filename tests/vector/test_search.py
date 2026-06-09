import pytest
from src.vector.search import SemanticSearch
from src.vector.embedding import EmbeddingService
from src.vector.store import VectorStore


class TestSemanticSearch:
    """SemanticSearch 测试"""

    @pytest.fixture
    def search(self):
        """创建 search 实例"""
        embedding_service = EmbeddingService()
        store = VectorStore()
        return SemanticSearch(embedding_service, store)

    def test_search_initialization(self, search):
        """测试 search 初始化"""
        assert search is not None
        assert hasattr(search, 'search')

    def test_search_returns_results(self, search):
        """测试搜索返回结果"""
        # 添加测试数据
        search.add_document("doc1", "清华大学毕业", {"source": "采访"})
        search.add_document("doc2", "创业成功", {"source": "新闻"})
        
        # 搜索
        results = search.search("清华大学毕业", top_k=1)
        assert len(results) > 0
        assert results[0]["id"] == "doc1"

    def test_search_empty_query(self, search):
        """测试空查询"""
        results = search.search("", top_k=1)
        assert len(results) == 0

    def test_search_no_results(self, search):
        """测试无结果搜索"""
        results = search.search("不存在的内容", top_k=1)
        assert len(results) == 0

    def test_search_multiple_results(self, search):
        """测试多结果搜索"""
        # 添加测试数据
        search.add_document("doc1", "清华大学毕业", {"source": "采访"})
        search.add_document("doc2", "清华大学计算机系", {"source": "简历"})
        search.add_document("doc3", "创业成功", {"source": "新闻"})
        
        # 搜索
        results = search.search("清华", top_k=2)
        assert len(results) == 2
