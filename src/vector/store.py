"""
向量存储器

负责存储和检索向量
"""

from typing import List, Dict, Any, Optional
import numpy as np
from .embedding import EmbeddingService


class VectorStore:
    """
    向量存储器
    
    存储和检索向量
    """
    
    def __init__(self):
        """初始化存储器"""
        self._vectors: Dict[str, List[float]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
    
    def add(self, doc_id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        添加向量
        
        Args:
            doc_id: 文档ID
            vector: 向量
            metadata: 元数据
        """
        self._vectors[doc_id] = vector
        if metadata:
            self._metadata[doc_id] = metadata
    
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相似向量
        
        Args:
            query_vector: 查询向量
            top_k: 返回前k个结果
            
        Returns:
            List[Dict[str, Any]]: 搜索结果
        """
        if not self._vectors:
            return []
        
        results = []
        for doc_id, vector in self._vectors.items():
            # 计算余弦相似度
            similarity = self._cosine_similarity(query_vector, vector)
            results.append({
                "id": doc_id,
                "score": similarity,
                "metadata": self._metadata.get(doc_id, {}),
            })
        
        # 按相似度排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def delete(self, doc_id: str) -> None:
        """
        删除向量
        
        Args:
            doc_id: 文档ID
        """
        if doc_id in self._vectors:
            del self._vectors[doc_id]
        if doc_id in self._metadata:
            del self._metadata[doc_id]
    
    def count(self) -> int:
        """
        获取向量数量
        
        Returns:
            int: 向量数量
        """
        return len(self._vectors)
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算余弦相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            float: 相似度
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
