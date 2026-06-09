"""
相似度计算

负责计算向量之间的相似度
"""

from typing import List
import numpy as np


class SimilarityCalculator:
    """
    相似度计算器
    
    计算向量之间的相似度
    """
    
    def __init__(self):
        """初始化计算器"""
        pass
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算余弦相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            float: 相似度 (-1 到 1)
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算欧氏距离
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            float: 距离
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        return np.linalg.norm(vec1 - vec2)
    
    def manhattan_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算曼哈顿距离
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            float: 距离
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        return np.sum(np.abs(vec1 - vec2))
