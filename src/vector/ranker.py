"""
检索排序器

负责对搜索结果进行排序
"""

from typing import List, Dict, Any, Optional


class SearchRanker:
    """
    检索排序器
    
    对搜索结果进行排序和过滤
    """
    
    def __init__(self):
        """初始化排序器"""
        pass
    
    def rank(
        self,
        results: List[Dict[str, Any]],
        threshold: Optional[float] = None,
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        对结果进行排序
        
        Args:
            results: 搜索结果
            threshold: 相似度阈值
            top_k: 返回前k个结果
            
        Returns:
            List[Dict[str, Any]]: 排序后的结果
        """
        if not results:
            return []
        
        # 按分数降序排序
        ranked = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
        
        # 应用阈值过滤
        if threshold is not None:
            ranked = [r for r in ranked if r.get("score", 0) >= threshold]
        
        # 应用top_k限制
        if top_k is not None:
            ranked = ranked[:top_k]
        
        return ranked
