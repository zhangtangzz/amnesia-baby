"""
KnowledgeLoader 测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.knowledge_loader import KnowledgeLoader


class TestKnowledgeLoader:
    """KnowledgeLoader 测试"""
    
    @pytest.fixture
    def loader(self):
        """创建 loader 实例"""
        return KnowledgeLoader()
    
    @pytest.fixture
    def mock_knowledge_data(self):
        """模拟知识数据"""
        return {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
                {
                    "topic": "技术",
                    "content": "技术是改变世界的力量",
                    "source": "演讲",
                },
            ],
        }
    
    def test_loader_initialization(self, loader):
        """测试 loader 初始化"""
        assert loader is not None
        assert hasattr(loader, 'load')
    
    @pytest.mark.asyncio
    async def test_load_returns_knowledge(self, loader, mock_knowledge_data):
        """测试加载返回知识数据"""
        loader._load_from_source = AsyncMock(return_value=mock_knowledge_data)
        
        result = await loader.load("elon")
        assert isinstance(result, dict)
        assert "character_id" in result
        assert "knowledge" in result
        assert isinstance(result["knowledge"], list)
    
    @pytest.mark.asyncio
    async def test_load_knowledge_list(self, loader, mock_knowledge_data):
        """测试加载知识列表"""
        loader._load_from_source = AsyncMock(return_value=mock_knowledge_data)
        
        result = await loader.load("elon")
        knowledge = result["knowledge"]
        assert len(knowledge) == 2
        assert knowledge[0]["topic"] == "创业"
        assert knowledge[1]["topic"] == "技术"
    
    @pytest.mark.asyncio
    async def test_load_empty_knowledge(self, loader):
        """测试加载空知识"""
        loader._load_from_source = AsyncMock(return_value={"character_id": "elon", "knowledge": []})
        
        result = await loader.load("elon")
        assert result["knowledge"] == []
    
    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, loader):
        """测试加载不存在的角色"""
        loader._load_from_source = AsyncMock(return_value=None)
        
        with pytest.raises(ValueError):
            await loader.load("nonexistent")
    
    @pytest.mark.asyncio
    async def test_load_invalid_data(self, loader):
        """测试加载无效数据"""
        loader._load_from_source = AsyncMock(return_value={"invalid": "data"})
        
        with pytest.raises(ValueError):
            await loader.load("elon")