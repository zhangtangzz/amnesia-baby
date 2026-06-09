"""
向量嵌入服务

负责将文本转换为向量
"""

from typing import List
import hashlib


class EmbeddingService:
    """
    向量嵌入服务
    
    将文本转换为向量表示
    """
    
    def __init__(self, dimension: int = 128):
        """
        初始化服务
        
        Args:
            dimension: 向量维度
        """
        self.dimension = dimension
    
    def embed(self, text: str) -> List[float]:
        """
        将文本转换为向量
        
        Args:
            text: 文本内容
            
        Returns:
            List[float]: 向量表示
        """
        if not text:
            return [0.0] * self.dimension
        
        # 使用哈希生成确定性向量（简化版本）
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        
        # 将哈希转换为浮点数向量
        vector = []
        for i in range(self.dimension):
            byte_index = i % len(hash_bytes)
            value = hash_bytes[byte_index] / 255.0  # 归一化到 0-1
            vector.append(value)
        
        return vector
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量向量化
        
        Args:
            texts: 文本列表
            
        Returns:
            List[List[float]]: 向量列表
        """
        return [self.embed(text) for text in texts]
