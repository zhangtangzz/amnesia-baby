import pytest
from src.vector.store import VectorStore
from src.vector.embedding import EmbeddingService


class TestVectorStore:
    """VectorStore 测试"""

    @pytest.fixture
    def store(self):
        """创建 store 实例"""
        return VectorStore()

    @pytest.fixture
    def embedding_service(self):
        """创建 embedding service 实例"""
        return EmbeddingService()

    def test_store_initialization(self, store):
        """测试 store 初始化"""
        assert store is not None
        assert hasattr(store, 'add')
        assert hasattr(store, 'search')

    def test_add_vector(self, store, embedding_service):
        """测试添加向量"""
        text = "清华大学毕业"
        vector = embedding_service.embed(text)
        store.add("doc1", vector, {"text": text})
        assert store.count() == 1

    def test_search_vector(self, store, embedding_service):
        """测试搜索向量"""
        text = "清华大学毕业"
        vector = embedding_service.embed(text)
        store.add("doc1", vector, {"text": text})
        
        query_vector = embedding_service.embed("清华")
        results = store.search(query_vector, top_k=1)
        assert len(results) > 0
        assert results[0]["id"] == "doc1"

    def test_search_empty_store(self, store, embedding_service):
        """测试空存储搜索"""
        query_vector = embedding_service.embed("清华")
        results = store.search(query_vector, top_k=1)
        assert len(results) == 0

    def test_delete_vector(self, store, embedding_service):
        """测试删除向量"""
        text = "清华大学毕业"
        vector = embedding_service.embed(text)
        store.add("doc1", vector, {"text": text})
        
        store.delete("doc1")
        assert store.count() == 0
