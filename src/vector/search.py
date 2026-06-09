"""
语义搜索器

负责语义搜索
"""

from typing import List, Dict, Any, Optional
from .embedding import EmbeddingService
from .store import VectorStore


class SemanticSearch:
    """
    语义搜索器
    
    提供语义搜索功能
    """
    
    def __init__(self, embedding_service: EmbeddingService, store: VectorStore):
        """
        初始化搜索器
        
        Args:
            embedding_service: 向量嵌入服务
            store: 向量存储器
        """
        self.embedding_service = embedding_service
        self.store = store
    
    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        添加文档
        
        Args:
            doc_id: 文档ID
            text: 文本内容
            metadata: 元数据
        """
        vector = self.embedding_service.embed(text)
        self.store.add(doc_id, vector, metadata)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
            
        Returns:
            List[Dict[str, Any]]: 搜索结果
        """
        if not query:
            return []
        
        # 向量化查询
        query_vector = self.embedding_service.embed(query)
        
        # 搜索相似向量
        results = self.store.search(query_vector, top_k)
        
        return results
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        批量添加文档
        
        Args:
            documents: 文档列表，每个文档包含 id, text, metadata
        """
        for doc in documents:
            self.add_document(doc["id"], doc["text"], doc.get("metadata"))
