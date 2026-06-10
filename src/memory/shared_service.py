"""
全局共享记忆服务

确保聊天引擎和API路由使用同一个 MemoryService 实例，实现记忆持久化
"""

from .service import MemoryService

# 全局单例
_global_service: MemoryService = None


def get_shared_memory_service() -> MemoryService:
    """获取全局共享的 MemoryService 实例"""
    global _global_service
    if _global_service is None:
        _global_service = MemoryService(persist=True)
    return _global_service


def reset_shared_memory_service() -> None:
    """重置全局单例（仅用于测试）"""
    global _global_service
    _global_service = None