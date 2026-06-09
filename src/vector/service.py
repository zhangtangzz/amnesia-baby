"""
向量检索服务

负责协调向量检索操作
"""

from typing import List, Dict, Any, Optional
from .embedding import EmbeddingService
from .store import VectorStore
from .search import SemanticSearch
from .ranker import SearchRanker
from .models import SearchResult


class VectorSearchService:
    """
    向量检索服务
    
    协调向量检索操作：向量化 -> 存储 -> 搜索 -> 排序
    """
    
    def __init__(self):
        """初始化服务"""
        self.embedding_service = EmbeddingService()
        self.store = VectorStore()
        self.search_engine = SemanticSearch(self.embedding_service, self.store)
        self.ranker = SearchRanker()
    
    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        添加文档
        
        Args:
            doc_id: 文档ID
            text: 文本内容
            metadata: 元数据
        """
        self.search_engine.add_document(doc_id, text, metadata)
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        批量添加文档
        
        Args:
            documents: 文档列表
        """
        self.search_engine.add_documents(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
            threshold: 相似度阈值
            
        Returns:
            List[SearchResult]: 搜索结果
        """
        if not query:
            return []
        
        # 搜索
        raw_results = self.search_engine.search(query, top_k)
        
        # 排序和过滤
        ranked_results = self.ranker.rank(raw_results, threshold=threshold, top_k=top_k)
        
        # 转换为 SearchResult
        results = []
        for r in ranked_results:
            result = SearchResult(
                doc_id=r["id"],
                score=r["score"],
                metadata=r.get("metadata", {}),
            )
            results.append(result)
        
        return results
    
    def delete_document(self, doc_id: str) -> None:
        """
        删除文档
        
        Args:
            doc_id: 文档ID
        """
        self.store.delete(doc_id)
    
    def count(self) -> int:
        """
        获取文档数量
        
        Returns:
            int: 文档数量
        """
        return self.store.count()
