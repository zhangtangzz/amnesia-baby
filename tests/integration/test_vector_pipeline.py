import pytest
from src.vector.service import VectorSearchService


class TestVectorPipeline:
    """向量检索流水线集成测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return VectorSearchService()

    def test_full_pipeline(self, service):
        """测试完整流水线"""
        # 添加文档
        documents = [
            {"id": "doc1", "text": "张三毕业于清华大学", "metadata": {"source": "采访"}},
            {"id": "doc2", "text": "张三创立了科技公司", "metadata": {"source": "新闻"}},
            {"id": "doc3", "text": "李四是一名教师", "metadata": {"source": "简历"}},
        ]
        service.add_documents(documents)
        
        # 搜索
        results = service.search("张三毕业于清华大学", top_k=2)
        
        # 验证结果
        assert len(results) > 0
        assert results[0].doc_id == "doc1"
        assert results[0].score > 0
        
        # 删除文档
        service.delete_document("doc1")
        assert service.count() == 2
