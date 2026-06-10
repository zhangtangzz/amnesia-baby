import pytest
import os
import json
from src.memory.service import MemoryService
from src.memory.models import MemoryItem


class TestMemoryService:
    """MemoryService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return MemoryService()

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'add_memory')
        assert hasattr(service, 'get_context')

    def test_add_memory(self, service):
        """测试添加记忆"""
        service.add_memory(
            character_id="elon",
            content="我喜欢SpaceX",
            memory_type="conversation",
            importance=0.8,
        )

        # 验证记忆被添加
        context = service.get_context("elon", "SpaceX")
        assert len(context) > 0

    def test_get_context(self, service):
        """测试获取上下文"""
        # 添加记忆
        service.add_memory(
            character_id="elon",
            content="用户喜欢SpaceX",
            memory_type="conversation",
            importance=0.8,
        )
        service.add_memory(
            character_id="elon",
            content="用户喜欢火星计划",
            memory_type="conversation",
            importance=0.9,
        )

        # 获取上下文
        context = service.get_context("elon", "SpaceX", max_context=5)

        # 验证结果
        assert isinstance(context, list)
        assert len(context) > 0

    def test_get_context_empty(self, service):
        """测试获取空上下文"""
        context = service.get_context("elon", "test", max_context=5)
        assert isinstance(context, list)
        assert len(context) > 0

    def test_consolidate_memories(self, service):
        """测试巩固记忆"""
        # 添加短期记忆
        for i in range(15):
            service.add_memory(
                character_id="elon",
                content=f"消息{i}",
                memory_type="conversation",
                importance=0.5 + i * 0.03,
            )

        # 巩固记忆
        service.consolidate_memories("elon")

        # 验证长期记忆
        assert service.long_term_memory.count() > 0


class TestMemoryPersistence:
    """记忆持久化测试"""

    @pytest.fixture(autouse=True)
    def cleanup_data_file(self):
        """测试前后清理数据文件"""
        from src.storage.database import DATA_DIR
        filepath = DATA_DIR / "memory.json"
        if filepath.exists():
            filepath.unlink()
        yield
        if filepath.exists():
            filepath.unlink()

    def test_service_persist_flag(self):
        """测试 persist 参数"""
        service = MemoryService(persist=True)
        assert service._persist is True

        service_no_persist = MemoryService(persist=False)
        assert service_no_persist._persist is False

    def test_save_and_load_short_term(self):
        """测试短期记忆保存和加载"""
        # 创建服务并添加记忆
        service1 = MemoryService(persist=True)
        service1.add_memory(
            character_id="elon",
            content="用户: 你好",
            memory_type="conversation",
            importance=0.5,
        )
        service1.add_memory(
            character_id="elon",
            content="助手: 你好！我是 Elon",
            memory_type="conversation",
            importance=0.5,
        )

        # 验证文件已写入
        from src.storage.database import DATA_DIR
        filepath = DATA_DIR / "memory.json"
        assert filepath.exists()

        # 创建新服务实例，验证记忆被加载
        service2 = MemoryService(persist=True)
        context = service2.get_context("elon", "你是谁", max_context=5)
        # 上下文应包含之前的对话记忆
        context_text = " ".join(context)
        assert "你好" in context_text

    def test_save_and_load_long_term(self):
        """测试长期记忆保存和加载"""
        service1 = MemoryService(persist=True)
        # 添加多个记忆并巩固
        for i in range(12):
            service1.add_memory(
                character_id="elon",
                content=f"重要记忆{i}",
                memory_type="conversation",
                importance=0.6 + i * 0.03,
            )
        service1.consolidate_memories("elon")
        assert service1.long_term_memory.count() > 0

        # 新实例加载
        service2 = MemoryService(persist=True)
        assert service2.long_term_memory.count() > 0

    def test_multi_character_persistence(self):
        """测试多角色记忆独立持久化"""
        service1 = MemoryService(persist=True)
        service1.add_memory(
            character_id="elon",
            content="用户: SpaceX 好棒",
            memory_type="conversation",
            importance=0.8,
        )
        service1.add_memory(
            character_id="zhangsan",
            content="用户: 今天天气不错",
            memory_type="conversation",
            importance=0.5,
        )

        # 新实例加载
        service2 = MemoryService(persist=True)
        elon_ctx = " ".join(service2.get_context("elon", "test", max_context=5))
        zhangsan_ctx = " ".join(service2.get_context("zhangsan", "test", max_context=5))

        assert "SpaceX" in elon_ctx
        assert "天气" in zhangsan_ctx
        # 角色记忆不应混在一起
        assert "SpaceX" not in zhangsan_ctx

    def test_persist_false_no_file_written(self):
        """测试 persist=False 不写文件"""
        service = MemoryService(persist=False)
        service.add_memory(
            character_id="elon",
            content="测试",
            memory_type="conversation",
        )

        from src.storage.database import DATA_DIR
        filepath = DATA_DIR / "memory.json"
        assert not filepath.exists()

    def test_load_corrupted_file(self):
        """测试加载损坏的文件不会崩溃"""
        from src.storage.database import DATA_DIR, _ensure_data_dir
        _ensure_data_dir()
        filepath = DATA_DIR / "memory.json"
        filepath.write_text("not valid json {{{", encoding="utf-8")

        # 不应抛异常
        service = MemoryService(persist=True)
        assert service.get_short_term_count() == 0
        assert service.get_long_term_count() == 0

    def test_persistence_with_memory_type_and_metadata(self):
        """测试记忆类型和元数据正确持久化"""
        service1 = MemoryService(persist=True)
        service1.add_memory(
            character_id="elon",
            content="重要信息",
            memory_type="fact",
            importance=0.9,
            metadata={"source": "interview"},
        )

        service2 = MemoryService(persist=True)
        all_memories = service2.short_term_memory.get_all()
        assert len(all_memories) == 1
        assert all_memories[0].memory_type == "fact"
        assert all_memories[0].importance == 0.9
        assert all_memories[0].metadata == {"source": "interview"}
