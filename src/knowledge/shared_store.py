"""
全局共享知识存储

确保 API 处理的知识和对话加载的知识使用同一个存储实例
"""

from .store import KnowledgeStore

# 全局单例
_global_store: KnowledgeStore = None


def get_shared_store() -> KnowledgeStore:
    """获取全局共享的 KnowledgeStore 实例"""
    global _global_store
    if _global_store is None:
        _global_store = KnowledgeStore()
    return _global_store
