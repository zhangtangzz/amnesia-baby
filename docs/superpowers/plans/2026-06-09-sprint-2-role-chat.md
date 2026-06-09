# Sprint-2 角色聊天 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现角色聊天最小可运行版本（MVP），支持用户发送消息，系统加载人格画像和知识库，构建角色Prompt，调用LLM生成回复。

**Architecture:** 采用分层架构，Chat Agent 作为核心协调器，CharacterLoader 加载人格画像，KnowledgeLoader 加载知识库，PromptBuilder 构建Prompt，LLMService 调用LLM，ChatService 提供统一接口。

**Tech Stack:** Python 3.14+, FastAPI, Pydantic, LangGraph, OpenAI API, pytest

---

## 文件结构

```
src/
├── chat/
│   ├── __init__.py
│   ├── chat_agent.py                # Chat Agent 核心
│   ├── character_loader.py          # 角色加载器
│   ├── knowledge_loader.py          # 知识加载器
│   ├── prompt_builder.py            # Prompt 构建器
│   ├── llm_service.py               # LLM 服务
│   └── chat_service.py              # 聊天服务
└── ...

tests/
├── chat/
│   ├── __init__.py
│   ├── test_chat_agent.py           # Chat Agent 测试
│   ├── test_character_loader.py     # 角色加载器测试
│   ├── test_knowledge_loader.py     # 知识加载器测试
│   ├── test_prompt_builder.py       # Prompt 构建器测试
│   ├── test_llm_service.py          # LLM 服务测试
│   └── test_chat_service.py         # 聊天服务测试
└── ...
```

---

## Task 1: CharacterLoader 实现

**Files:**
- Create: `src/chat/character_loader.py`
- Create: `tests/chat/test_character_loader.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_character_loader.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.character_loader import CharacterLoader
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestCharacterLoader:
    """CharacterLoader 测试"""
    
    @pytest.fixture
    def loader(self):
        """创建 loader 实例"""
        return CharacterLoader()
    
    @pytest.fixture
    def mock_character_data(self):
        """模拟角色数据"""
        return {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": {
                "achievement_drive": 0.9,
                "curiosity": 0.8,
                "risk_preference": 0.85,
            },
            "big_five": {
                "openness": 0.8,
                "conscientiousness": 0.7,
                "extraversion": 0.75,
            },
            "enneagram": {
                "type8": 0.4,
                "type3": 0.3,
                "type7": 0.2,
            },
        }
    
    def test_loader_initialization(self, loader):
        """测试 loader 初始化"""
        assert loader is not None
        assert hasattr(loader, 'load')
    
    @pytest.mark.asyncio
    async def test_load_returns_character(self, loader, mock_character_data):
        """测试加载返回角色数据"""
        # 模拟数据源
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        assert isinstance(result, dict)
        assert "character_id" in result
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram" in result
    
    @pytest.mark.asyncio
    async def test_load_personality_profile(self, loader, mock_character_data):
        """测试加载人格画像"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        personality = result["personality"]
        assert isinstance(personality, PersonalityProfile)
        assert personality.achievement_drive == 0.9
    
    @pytest.mark.asyncio
    async def test_load_big_five_profile(self, loader, mock_character_data):
        """测试加载大五人格"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        big_five = result["big_five"]
        assert isinstance(big_five, BigFiveProfile)
        assert big_five.openness == 0.8
    
    @pytest.mark.asyncio
    async def test_load_enneagram_profile(self, loader, mock_character_data):
        """测试加载九型人格"""
        loader._load_from_source = AsyncMock(return_value=mock_character_data)
        
        result = await loader.load("elon")
        enneagram = result["enneagram"]
        assert isinstance(enneagram, EnneagramProfile)
        assert enneagram.type8 == 0.4
    
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
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_character_loader.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.character_loader'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/character_loader.py

"""
角色加载器

负责加载角色的人格画像
"""

from typing import Dict, Any, Optional
from ..personality.profile import PersonalityProfile
from ..personality.big_five import BigFiveProfile
from ..personality.enneagram import EnneagramProfile


class CharacterLoader:
    """
    角色加载器
    
    从数据源加载角色信息，包括人格画像
    """
    
    def __init__(self):
        """初始化加载器"""
        pass
    
    async def load(self, character_id: str) -> Dict[str, Any]:
        """
        加载角色信息
        
        Args:
            character_id: 角色ID
            
        Returns:
            Dict: 包含角色信息的字典
            
        Raises:
            ValueError: 角色不存在或数据无效
        """
        # 从数据源加载
        data = await self._load_from_source(character_id)
        
        if data is None:
            raise ValueError(f"Character not found: {character_id}")
        
        # 验证数据结构
        if "personality" not in data:
            raise ValueError(f"Invalid character data: missing personality")
        
        # 解析人格画像
        personality = PersonalityProfile(**data["personality"])
        big_five = BigFiveProfile(**data.get("big_five", {}))
        enneagram = EnneagramProfile(**data.get("enneagram", {}))
        
        return {
            "character_id": data.get("character_id", character_id),
            "name": data.get("name", ""),
            "personality": personality,
            "big_five": big_five,
            "enneagram": enneagram,
        }
    
    async def _load_from_source(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        从数据源加载角色数据
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[Dict]: 角色数据，不存在返回 None
        """
        # TODO: 实现实际的数据源加载逻辑
        # 这里返回模拟数据用于测试
        mock_data = {
            "elon": {
                "character_id": "elon",
                "name": "Elon Musk",
                "personality": {
                    "achievement_drive": 0.9,
                    "curiosity": 0.8,
                    "risk_preference": 0.85,
                },
                "big_five": {
                    "openness": 0.8,
                    "conscientiousness": 0.7,
                    "extraversion": 0.75,
                },
                "enneagram": {
                    "type8": 0.4,
                    "type3": 0.3,
                    "type7": 0.2,
                },
            }
        }
        return mock_data.get(character_id)
```

- [ ] **Step 4: 创建 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader

__all__ = ["CharacterLoader"]
```

- [ ] **Step 5: 创建 tests/chat/__init__.py**

```python
# tests/chat/__init__.py

"""
聊天测试包
"""
```

- [ ] **Step 6: 运行测试验证通过**

Run: `pytest tests/chat/test_character_loader.py -v`
Expected: 7 passed

- [ ] **Step 7: 提交代码**

```bash
git add src/chat/ tests/chat/
git commit -m "feat: implement CharacterLoader for loading character profiles"
```

---

## Task 2: KnowledgeLoader 实现

**Files:**
- Create: `src/chat/knowledge_loader.py`
- Create: `tests/chat/test_knowledge_loader.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_knowledge_loader.py

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
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_knowledge_loader.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.knowledge_loader'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/knowledge_loader.py

"""
知识加载器

负责加载角色的知识库
"""

from typing import Dict, Any, List, Optional


class KnowledgeLoader:
    """
    知识加载器
    
    从数据源加载角色的知识库
    """
    
    def __init__(self):
        """初始化加载器"""
        pass
    
    async def load(self, character_id: str) -> Dict[str, Any]:
        """
        加载角色知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            Dict: 包含知识库的字典
            
        Raises:
            ValueError: 角色不存在或数据无效
        """
        # 从数据源加载
        data = await self._load_from_source(character_id)
        
        if data is None:
            raise ValueError(f"Character not found: {character_id}")
        
        # 验证数据结构
        if "knowledge" not in data:
            raise ValueError(f"Invalid knowledge data: missing knowledge")
        
        return {
            "character_id": data.get("character_id", character_id),
            "knowledge": data.get("knowledge", []),
        }
    
    async def _load_from_source(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        从数据源加载知识数据
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[Dict]: 知识数据，不存在返回 None
        """
        # TODO: 实现实际的数据源加载逻辑
        # 这里返回模拟数据用于测试
        mock_data = {
            "elon": {
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
        }
        return mock_data.get(character_id)
```

- [ ] **Step 4: 更新 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader

__all__ = [
    "CharacterLoader",
    "KnowledgeLoader",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/chat/test_knowledge_loader.py -v`
Expected: 5 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/chat/knowledge_loader.py src/chat/__init__.py tests/chat/test_knowledge_loader.py
git commit -m "feat: implement KnowledgeLoader for loading character knowledge"
```

---

## Task 3: PromptBuilder 实现

**Files:**
- Create: `src/chat/prompt_builder.py`
- Create: `tests/chat/test_prompt_builder.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_prompt_builder.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.prompt_builder import PromptBuilder
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestPromptBuilder:
    """PromptBuilder 测试"""
    
    @pytest.fixture
    def builder(self):
        """创建 builder 实例"""
        return PromptBuilder()
    
    @pytest.fixture
    def mock_character(self):
        """模拟角色数据"""
        return {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": PersonalityProfile(
                achievement_drive=0.9,
                curiosity=0.8,
                risk_preference=0.85,
            ),
            "big_five": BigFiveProfile(openness=0.8),
            "enneagram": EnneagramProfile(type8=0.4),
        }
    
    @pytest.fixture
    def mock_knowledge(self):
        """模拟知识数据"""
        return {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
            ],
        }
    
    def test_builder_initialization(self, builder):
        """测试 builder 初始化"""
        assert builder is not None
        assert hasattr(builder, 'build')
    
    def test_build_returns_prompt(self, builder, mock_character, mock_knowledge):
        """测试构建返回 prompt"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_build_includes_personality(self, builder, mock_character, mock_knowledge):
        """测试构建包含人格信息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert "Elon Musk" in result
        assert "成就驱动" in result or "achievement_drive" in result
    
    def test_build_includes_knowledge(self, builder, mock_character, mock_knowledge):
        """测试构建包含知识信息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert "创业" in result
        assert "创业让我能够实现那些看似不可能的想法" in result
    
    def test_build_includes_message(self, builder, mock_character, mock_knowledge):
        """测试构建包含用户消息"""
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, mock_knowledge, message)
        assert message in result
    
    def test_build_empty_knowledge(self, builder, mock_character):
        """测试构建空知识"""
        empty_knowledge = {"character_id": "elon", "knowledge": []}
        message = "你为什么喜欢创业？"
        result = builder.build(mock_character, empty_knowledge, message)
        assert isinstance(result, str)
        assert len(result) > 0
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_prompt_builder.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.prompt_builder'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/prompt_builder.py

"""
Prompt 构建器

负责构建角色聊天的 Prompt
"""

from typing import Dict, Any


class PromptBuilder:
    """
    Prompt 构建器
    
    根据角色信息、知识库和用户消息构建 Prompt
    """
    
    def __init__(self):
        """初始化构建器"""
        pass
    
    def build(
        self,
        character: Dict[str, Any],
        knowledge: Dict[str, Any],
        message: str,
    ) -> str:
        """
        构建 Prompt
        
        Args:
            character: 角色信息
            knowledge: 知识库
            message: 用户消息
            
        Returns:
            str: 构建的 Prompt
        """
        # 获取角色信息
        name = character.get("name", "Unknown")
        personality = character.get("personality")
        
        # 构建人格描述
        personality_desc = self._build_personality_description(personality)
        
        # 构建知识描述
        knowledge_desc = self._build_knowledge_description(knowledge)
        
        # 构建完整 Prompt
        prompt = f"""你正在扮演角色: {name}

## 角色人格

{personality_desc}

## 角色知识

{knowledge_desc}

## 用户消息

{message}

## 回复要求

请以角色的身份回复用户的消息。回复应该：
1. 符合角色的人格特征
2. 基于角色的知识
3. 自然、流畅、有说服力

请开始回复："""
        
        return prompt
    
    def _build_personality_description(self, personality) -> str:
        """
        构建人格描述
        
        Args:
            personality: 人格画像
            
        Returns:
            str: 人格描述
        """
        if personality is None:
            return "暂无人格信息"
        
        traits = []
        if hasattr(personality, 'achievement_drive'):
            traits.append(f"- 成就驱动: {personality.achievement_drive:.2f}")
        if hasattr(personality, 'curiosity'):
            traits.append(f"- 好奇心: {personality.curiosity:.2f}")
        if hasattr(personality, 'risk_preference'):
            traits.append(f"- 风险偏好: {personality.risk_preference:.2f}")
        if hasattr(personality, 'empathy'):
            traits.append(f"- 共情能力: {personality.empathy:.2f}")
        if hasattr(personality, 'dominance'):
            traits.append(f"- 支配性: {personality.dominance:.2f}")
        
        return "\n".join(traits) if traits else "暂无人格信息"
    
    def _build_knowledge_description(self, knowledge: Dict[str, Any]) -> str:
        """
        构建知识描述
        
        Args:
            knowledge: 知识库
            
        Returns:
            str: 知识描述
        """
        knowledge_list = knowledge.get("knowledge", [])
        
        if not knowledge_list:
            return "暂无知识信息"
        
        descriptions = []
        for item in knowledge_list:
            topic = item.get("topic", "")
            content = item.get("content", "")
            if topic and content:
                descriptions.append(f"- {topic}: {content}")
        
        return "\n".join(descriptions) if descriptions else "暂无知识信息"
```

- [ ] **Step 4: 更新 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder

__all__ = [
    "CharacterLoader",
    "KnowledgeLoader",
    "PromptBuilder",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/chat/test_prompt_builder.py -v`
Expected: 6 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/chat/prompt_builder.py src/chat/__init__.py tests/chat/test_prompt_builder.py
git commit -m "feat: implement PromptBuilder for building character chat prompts"
```

---

## Task 4: LLMService 实现

**Files:**
- Create: `src/chat/llm_service.py`
- Create: `tests/chat/test_llm_service.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_llm_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chat.llm_service import LLMService


class TestLLMService:
    """LLMService 测试"""
    
    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return LLMService()
    
    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'generate')
    
    @pytest.mark.asyncio
    async def test_generate_returns_response(self, service):
        """测试生成返回响应"""
        prompt = "你为什么喜欢创业？"
        
        # 模拟 LLM 响应
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "创业让我能够实现那些看似不可能的想法"
        
        with patch.object(service, '_call_llm', return_value=mock_response):
            result = await service.generate(prompt)
            assert isinstance(result, str)
            assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_generate_with_context(self, service):
        """测试生成带上下文"""
        prompt = "你为什么喜欢创业？"
        context = "Elon Musk"
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "创业让我能够实现那些看似不可能的想法"
        
        with patch.object(service, '_call_llm', return_value=mock_response):
            result = await service.generate(prompt, context=context)
            assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_generate_empty_prompt(self, service):
        """测试生成空 prompt"""
        with pytest.raises(ValueError):
            await service.generate("")
    
    @pytest.mark.asyncio
    async def test_generate_handles_error(self, service):
        """测试生成处理错误"""
        prompt = "你为什么喜欢创业？"
        
        with patch.object(service, '_call_llm', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                await service.generate(prompt)
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_llm_service.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.llm_service'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/llm_service.py

"""
LLM 服务

负责调用 LLM 生成回复
"""

from typing import Optional
import openai
from ..config import get_settings


class LLMService:
    """
    LLM 服务
    
    调用 OpenAI 兼容的 LLM 生成回复
    """
    
    def __init__(self):
        """初始化服务"""
        self.settings = get_settings()
        self.client = openai.AsyncOpenAI(
            api_key=self.settings.openai_api_key,
            base_url=self.settings.openai_api_base,
        )
    
    async def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """
        生成回复
        
        Args:
            prompt: Prompt 内容
            context: 上下文信息
            
        Returns:
            str: 生成的回复
            
        Raises:
            ValueError: Prompt 为空
            Exception: LLM 调用失败
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # 构建消息
        messages = []
        
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": prompt})
        
        # 调用 LLM
        response = await self._call_llm(messages)
        
        return response.choices[0].message.content
    
    async def _call_llm(self, messages):
        """
        调用 LLM
        
        Args:
            messages: 消息列表
            
        Returns:
            LLM 响应
        """
        return await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
```

- [ ] **Step 4: 更新 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from .llm_service import LLMService

__all__ = [
    "CharacterLoader",
    "KnowledgeLoader",
    "PromptBuilder",
    "LLMService",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/chat/test_llm_service.py -v`
Expected: 4 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/chat/llm_service.py src/chat/__init__.py tests/chat/test_llm_service.py
git commit -m "feat: implement LLMService for calling OpenAI-compatible LLM"
```

---

## Task 5: ChatService 实现

**Files:**
- Create: `src/chat/chat_service.py`
- Create: `tests/chat/test_chat_service.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_chat_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.chat_service import ChatService
from src.chat.character_loader import CharacterLoader
from src.chat.knowledge_loader import KnowledgeLoader
from src.chat.prompt_builder import PromptBuilder
from src.chat.llm_service import LLMService


class TestChatService:
    """ChatService 测试"""
    
    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return ChatService()
    
    @pytest.fixture
    def mock_character(self):
        """模拟角色数据"""
        return {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": MagicMock(),
            "big_five": MagicMock(),
            "enneagram": MagicMock(),
        }
    
    @pytest.fixture
    def mock_knowledge(self):
        """模拟知识数据"""
        return {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
            ],
        }
    
    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'chat')
    
    @pytest.mark.asyncio
    async def test_chat_returns_reply(self, service, mock_character, mock_knowledge):
        """测试聊天返回回复"""
        # 模拟依赖
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")
        
        result = await service.chat("elon", "你为什么喜欢创业？")
        assert isinstance(result, dict)
        assert "reply" in result
        assert result["reply"] == "test reply"
    
    @pytest.mark.asyncio
    async def test_chat_with_character_id(self, service, mock_character, mock_knowledge):
        """测试聊天带角色ID"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")
        
        result = await service.chat("elon", "你为什么喜欢创业？")
        service.character_loader.load.assert_called_once_with("elon")
    
    @pytest.mark.asyncio
    async def test_chat_with_message(self, service, mock_character, mock_knowledge):
        """测试聊天带消息"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(return_value="test reply")
        
        message = "你为什么喜欢创业？"
        result = await service.chat("elon", message)
        service.prompt_builder.build.assert_called_once_with(
            mock_character, mock_knowledge, message
        )
    
    @pytest.mark.asyncio
    async def test_chat_handles_character_not_found(self, service):
        """测试聊天处理角色不存在"""
        service.character_loader.load = AsyncMock(side_effect=ValueError("Character not found"))
        
        with pytest.raises(ValueError):
            await service.chat("nonexistent", "test")
    
    @pytest.mark.asyncio
    async def test_chat_handles_llm_error(self, service, mock_character, mock_knowledge):
        """测试聊天处理 LLM 错误"""
        service.character_loader.load = AsyncMock(return_value=mock_character)
        service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        service.prompt_builder.build = MagicMock(return_value="test prompt")
        service.llm_service.generate = AsyncMock(side_effect=Exception("LLM Error"))
        
        with pytest.raises(Exception):
            await service.chat("elon", "test")
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_chat_service.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.chat_service'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/chat_service.py

"""
聊天服务

负责协调角色聊天流程
"""

from typing import Dict, Any
from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from .llm_service import LLMService


class ChatService:
    """
    聊天服务
    
    协调角色聊天流程：加载角色 -> 加载知识 -> 构建Prompt -> 调用LLM
    """
    
    def __init__(self):
        """初始化服务"""
        self.character_loader = CharacterLoader()
        self.knowledge_loader = KnowledgeLoader()
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService()
    
    async def chat(self, character_id: str, message: str) -> Dict[str, Any]:
        """
        角色聊天
        
        Args:
            character_id: 角色ID
            message: 用户消息
            
        Returns:
            Dict: 包含回复的字典
            
        Raises:
            ValueError: 角色不存在
            Exception: LLM 调用失败
        """
        # 加载角色信息
        character = await self.character_loader.load(character_id)
        
        # 加载知识库
        knowledge = await self.knowledge_loader.load(character_id)
        
        # 构建 Prompt
        prompt = self.prompt_builder.build(character, knowledge, message)
        
        # 调用 LLM 生成回复
        reply = await self.llm_service.generate(prompt)
        
        return {
            "reply": reply,
        }
```

- [ ] **Step 4: 更新 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from .llm_service import LLMService
from .chat_service import ChatService

__all__ = [
    "CharacterLoader",
    "KnowledgeLoader",
    "PromptBuilder",
    "LLMService",
    "ChatService",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/chat/test_chat_service.py -v`
Expected: 5 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/chat/chat_service.py src/chat/__init__.py tests/chat/test_chat_service.py
git commit -m "feat: implement ChatService for coordinating character chat"
```

---

## Task 6: ChatAgent 实现

**Files:**
- Create: `src/chat/chat_agent.py`
- Create: `tests/chat/test_chat_agent.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/chat/test_chat_agent.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.chat_agent import ChatAgent
from src.chat.chat_service import ChatService


class TestChatAgent:
    """ChatAgent 测试"""
    
    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        return ChatAgent()
    
    @pytest.fixture
    def mock_reply(self):
        """模拟回复"""
        return {"reply": "创业让我能够实现那些看似不可能的想法"}
    
    def test_agent_initialization(self, agent):
        """测试 agent 初始化"""
        assert agent is not None
        assert hasattr(agent, 'chat')
    
    @pytest.mark.asyncio
    async def test_chat_returns_reply(self, agent, mock_reply):
        """测试聊天返回回复"""
        agent.chat_service.chat = AsyncMock(return_value=mock_reply)
        
        result = await agent.chat("elon", "你为什么喜欢创业？")
        assert isinstance(result, dict)
        assert "reply" in result
        assert result["reply"] == mock_reply["reply"]
    
    @pytest.mark.asyncio
    async def test_chat_with_character_id(self, agent, mock_reply):
        """测试聊天带角色ID"""
        agent.chat_service.chat = AsyncMock(return_value=mock_reply)
        
        result = await agent.chat("elon", "你为什么喜欢创业？")
        agent.chat_service.chat.assert_called_once_with("elon", "你为什么喜欢创业？")
    
    @pytest.mark.asyncio
    async def test_chat_handles_error(self, agent):
        """测试聊天处理错误"""
        agent.chat_service.chat = AsyncMock(side_effect=Exception("Chat Error"))
        
        with pytest.raises(Exception):
            await agent.chat("elon", "test")
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/chat/test_chat_agent.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.chat.chat_agent'"

- [ ] **Step 3: 编写最小实现**

```python
# src/chat/chat_agent.py

"""
Chat Agent

负责角色聊天的核心逻辑
"""

from typing import Dict, Any
from .chat_service import ChatService


class ChatAgent:
    """
    Chat Agent
    
    角色聊天的核心入口
    """
    
    def __init__(self):
        """初始化 agent"""
        self.chat_service = ChatService()
    
    async def chat(self, character_id: str, message: str) -> Dict[str, Any]:
        """
        角色聊天
        
        Args:
            character_id: 角色ID
            message: 用户消息
            
        Returns:
            Dict: 包含回复的字典
            
        Raises:
            ValueError: 角色不存在
            Exception: LLM 调用失败
        """
        return await self.chat_service.chat(character_id, message)
```

- [ ] **Step 4: 更新 src/chat/__init__.py**

```python
# src/chat/__init__.py

"""
聊天模块
"""

from .character_loader import CharacterLoader
from .knowledge_loader import KnowledgeLoader
from .prompt_builder import PromptBuilder
from .llm_service import LLMService
from .chat_service import ChatService
from .chat_agent import ChatAgent

__all__ = [
    "CharacterLoader",
    "KnowledgeLoader",
    "PromptBuilder",
    "LLMService",
    "ChatService",
    "ChatAgent",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/chat/test_chat_agent.py -v`
Expected: 4 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/chat/chat_agent.py src/chat/__init__.py tests/chat/test_chat_agent.py
git commit -m "feat: implement ChatAgent as core entry point for character chat"
```

---

## Task 7: 集成测试

**Files:**
- Create: `tests/integration/test_chat_pipeline.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/integration/test_chat_pipeline.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.chat.chat_agent import ChatAgent
from src.chat.character_loader import CharacterLoader
from src.chat.knowledge_loader import KnowledgeLoader
from src.chat.prompt_builder import PromptBuilder
from src.chat.llm_service import LLMService


class TestChatPipeline:
    """聊天流水线集成测试"""
    
    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        return ChatAgent()
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, agent):
        """测试完整流水线"""
        # 模拟数据
        mock_character = {
            "character_id": "elon",
            "name": "Elon Musk",
            "personality": MagicMock(),
            "big_five": MagicMock(),
            "enneagram": MagicMock(),
        }
        mock_knowledge = {
            "character_id": "elon",
            "knowledge": [
                {
                    "topic": "创业",
                    "content": "创业让我能够实现那些看似不可能的想法",
                    "source": "采访视频",
                },
            ],
        }
        mock_reply = "创业让我能够实现那些看似不可能的想法"
        
        # 模拟依赖
        agent.chat_service.character_loader.load = AsyncMock(return_value=mock_character)
        agent.chat_service.knowledge_loader.load = AsyncMock(return_value=mock_knowledge)
        agent.chat_service.prompt_builder.build = MagicMock(return_value="test prompt")
        agent.chat_service.llm_service.generate = AsyncMock(return_value=mock_reply)
        
        # 执行测试
        result = await agent.chat("elon", "你为什么喜欢创业？")
        
        # 验证结果
        assert "reply" in result
        assert result["reply"] == mock_reply
        
        # 验证调用
        agent.chat_service.character_loader.load.assert_called_once_with("elon")
        agent.chat_service.knowledge_loader.load.assert_called_once_with("elon")
        agent.chat_service.prompt_builder.build.assert_called_once()
        agent.chat_service.llm_service.generate.assert_called_once()
```

- [ ] **Step 2: 运行集成测试**

Run: `pytest tests/integration/test_chat_pipeline.py -v`
Expected: 1 passed

- [ ] **Step 3: 提交代码**

```bash
git add tests/integration/test_chat_pipeline.py
git commit -m "test: add integration tests for chat pipeline"
```

---

## Task 8: 运行所有测试并生成覆盖率报告

- [ ] **Step 1: 运行所有测试**

Run: `pytest tests/ -v`
Expected: All tests passed

- [ ] **Step 2: 生成覆盖率报告**

Run: `pytest tests/ --cov=src --cov-report=term-missing`
Expected: Coverage >= 80%

- [ ] **Step 3: 提交最终代码**

```bash
git add .
git commit -m "feat: complete Sprint-2 role chat MVP"
```

---

## 执行选项

**计划已完成并保存到 `docs/superpowers/plans/2026-06-09-sprint-2-role-chat.md`**

两种执行方式：

**1. Subagent-Driven（推荐）** - 每个任务分发给独立子代理执行，任务间进行审查，快速迭代

**2. Inline Execution** - 在当前会话中执行任务，批量执行并设置检查点

**选择哪种方式？**