import pytest
from src.vector.service import VectorSearchService
from src.vector.models import SearchResult


class TestVectorSearchService:
    """VectorSearchService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return VectorSearchService()

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'add_document')
        assert hasattr(service, 'search')

    def test_add_document(self, service):
        """测试添加文档"""
        service.add_document("doc1", "清华大学毕业", {"source": "采访"})
        assert service.count() == 1

    def test_search_returns_results(self, service):
        """测试搜索返回结果"""
        # 添加测试数据
        service.add_document("doc1", "清华大学毕业", {"source": "采访"})
        service.add_document("doc2", "创业成功", {"source": "新闻"})
        
        # 搜索
        results = service.search("清华大学毕业", top_k=1)
        assert len(results) > 0
        assert results[0].doc_id == "doc1"

    def test_search_empty_query(self, service):
        """测试空查询"""
        results = service.search("", top_k=1)
        assert len(results) == 0

    def test_delete_document(self, service):
        """测试删除文档"""
        service.add_document("doc1", "清华大学毕业", {"source": "采访"})
        service.delete_document("doc1")
        assert service.count() == 0

    def test_search_with_threshold(self, service):
        """测试带阈值搜索"""
        # 添加测试数据
        service.add_document("doc1", "清华大学毕业", {"source": "采访"})
        service.add_document("doc2", "创业成功", {"source": "新闻"})
        
        # 搜索
        results = service.search("清华大学毕业", threshold=0.5)
        assert all(r.score >= 0.5 for r in results)
