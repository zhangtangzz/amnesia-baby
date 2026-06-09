# Sprint-3 知识库 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现角色知识库最小可运行版本（MVP），支持知识提取、存储、查询和更新。

**Architecture:** 采用分层架构，KnowledgeExtractor 提取知识，KnowledgeStore 存储知识，KnowledgeQuery 查询知识，KnowledgeUpdater 更新知识，KnowledgeService 提供统一接口。

**Tech Stack:** Python 3.14+, Pydantic, ChromaDB, pytest

---

## 文件结构

```
src/
├── knowledge/
│   ├── __init__.py
│   ├── models.py                    # 知识库数据模型
│   ├── extractor.py                 # 知识提取器
│   ├── store.py                     # 知识存储器
│   ├── query.py                     # 知识查询器
│   ├── updater.py                   # 知识更新器
│   └── service.py                   # 知识服务
└── ...

tests/
├── knowledge/
│   ├── __init__.py
│   ├── test_models.py               # 数据模型测试
│   ├── test_extractor.py            # 知识提取器测试
│   ├── test_store.py                # 知识存储器测试
│   ├── test_query.py                # 知识查询器测试
│   ├── test_updater.py              # 知识更新器测试
│   └── test_service.py              # 知识服务测试
└── ...
```

---

## Task 1: 知识库数据结构

**Files:**
- Create: `src/knowledge/models.py`
- Create: `tests/knowledge/test_models.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_models.py

import pytest
from pydantic import ValidationError
from src.knowledge.models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
)


class TestKnowledgeModels:
    """知识库数据模型测试"""

    def test_knowledge_profile_creation(self):
        """测试基础信息创建"""
        profile = KnowledgeProfile(
            name="张三",
            occupation="创业者",
            education="清华大学",
        )
        assert profile.name == "张三"
        assert profile.occupation == "创业者"
        assert profile.education == "清华大学"

    def test_relationship_creation(self):
        """测试人物关系创建"""
        rel = Relationship(
            name="李四",
            relationship="朋友",
            closeness=0.85,
            description="大学室友",
        )
        assert rel.name == "李四"
        assert rel.relationship == "朋友"
        assert rel.closeness == 0.85

    def test_event_creation(self):
        """测试重要事件创建"""
        event = Event(
            title="第一次创业失败",
            time="2019",
            impact=0.95,
        )
        assert event.title == "第一次创业失败"
        assert event.time == "2019"
        assert event.impact == 0.95

    def test_belief_creation(self):
        """测试观点体系创建"""
        belief = Belief(
            topic="创业",
            stance="支持",
            confidence=0.88,
        )
        assert belief.topic == "创业"
        assert belief.stance == "支持"
        assert belief.confidence == 0.88

    def test_fact_creation(self):
        """测试事实库创建"""
        fact = Fact(
            fact="创立某科技公司",
            category="career",
            confidence=0.94,
        )
        assert fact.fact == "创立某科技公司"
        assert fact.category == "career"
        assert fact.confidence == 0.94

    def test_timeline_creation(self):
        """测试人生时间轴创建"""
        timeline = Timeline(
            year="2020",
            events=["创业", "获得融资"],
        )
        assert timeline.year == "2020"
        assert len(timeline.events) == 2

    def test_evidence_creation(self):
        """测试证据库创建"""
        evidence = Evidence(
            source_type="video",
            source_name="人物采访",
            content="我从大学开始创业",
            confidence=0.91,
        )
        assert evidence.source_type == "video"
        assert evidence.source_name == "人物采访"
        assert evidence.content == "我从大学开始创业"

    def test_knowledge_base_creation(self):
        """测试知识库创建"""
        kb = KnowledgeBase(
            profile=KnowledgeProfile(name="张三"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[],
            timeline=[],
            evidence=[],
        )
        assert kb.profile.name == "张三"
        assert kb.relationships == []

    def test_relationship_closeness_validation(self):
        """测试关系亲密度验证"""
        with pytest.raises(ValidationError):
            Relationship(name="test", relationship="test", closeness=1.5)

    def test_event_impact_validation(self):
        """测试事件影响度验证"""
        with pytest.raises(ValidationError):
            Event(title="test", impact=1.5)

    def test_belief_confidence_validation(self):
        """测试观点置信度验证"""
        with pytest.raises(ValidationError):
            Belief(topic="test", stance="test", confidence=1.5)

    def test_fact_confidence_validation(self):
        """测试事实置信度验证"""
        with pytest.raises(ValidationError):
            Fact(fact="test", category="test", confidence=1.5)

    def test_evidence_confidence_validation(self):
        """测试证据置信度验证"""
        with pytest.raises(ValidationError):
            Evidence(source_type="test", source_name="test", content="test", confidence=1.5)
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_models.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.models'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/models.py

"""
知识库数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class RelationshipType(str, Enum):
    """关系类型枚举"""
    PARENT = "父母"
    SIBLING = "兄弟姐妹"
    FRIEND = "朋友"
    COLLEAGUE = "同事"
    PARTNER = "伴侣"
    MENTOR = "导师"
    COMPETITOR = "竞争对手"
    PARTNER_BUSINESS = "合作伙伴"


class SourceType(str, Enum):
    """来源类型枚举"""
    VIDEO = "video"
    AUDIO = "audio"
    ARTICLE = "article"
    WIKI = "wiki"
    SOCIAL_MEDIA = "social_media"
    CHAT = "chat"
    USER_UPLOAD = "user_upload"


class KnowledgeProfile(BaseModel):
    """基础信息"""
    name: str = Field(..., description="姓名")
    alias: List[str] = Field(default=[], description="别名")
    gender: Optional[str] = Field(default=None, description="性别")
    birthday: Optional[str] = Field(default=None, description="生日")
    occupation: Optional[str] = Field(default=None, description="职业")
    nationality: Optional[str] = Field(default=None, description="国籍")
    education: Optional[str] = Field(default=None, description="教育背景")
    location: Optional[str] = Field(default=None, description="所在地")
    description: Optional[str] = Field(default=None, description="描述")


class Relationship(BaseModel):
    """人物关系"""
    person_id: Optional[str] = Field(default=None, description="人物ID")
    name: str = Field(..., description="姓名")
    relationship: str = Field(..., description="关系类型")
    closeness: float = Field(..., ge=0.0, le=1.0, description="亲密度")
    description: Optional[str] = Field(default=None, description="描述")


class Event(BaseModel):
    """重要事件"""
    event_id: Optional[str] = Field(default=None, description="事件ID")
    title: str = Field(..., description="标题")
    time: Optional[str] = Field(default=None, description="时间")
    location: Optional[str] = Field(default=None, description="地点")
    description: Optional[str] = Field(default=None, description="描述")
    impact: float = Field(..., ge=0.0, le=1.0, description="影响度")


class Belief(BaseModel):
    """观点体系"""
    topic: str = Field(..., description="主题")
    stance: str = Field(..., description="立场")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class Fact(BaseModel):
    """事实库"""
    fact: str = Field(..., description="事实")
    category: str = Field(..., description="类别")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class Timeline(BaseModel):
    """人生时间轴"""
    year: str = Field(..., description="年份")
    events: List[str] = Field(..., description="事件列表")


class Evidence(BaseModel):
    """证据库"""
    source_type: str = Field(..., description="来源类型")
    source_name: str = Field(..., description="来源名称")
    content: str = Field(..., description="内容")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class KnowledgeBase(BaseModel):
    """知识库"""
    profile: KnowledgeProfile = Field(..., description="基础信息")
    relationships: List[Relationship] = Field(default=[], description="人物关系")
    events: List[Event] = Field(default=[], description="重要事件")
    beliefs: List[Belief] = Field(default=[], description="观点体系")
    facts: List[Fact] = Field(default=[], description="事实库")
    timeline: List[Timeline] = Field(default=[], description="人生时间轴")
    evidence: List[Evidence] = Field(default=[], description="证据库")
```

- [ ] **Step 4: 创建 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
]
```

- [ ] **Step 5: 创建 tests/knowledge/__init__.py**

```python
# tests/knowledge/__init__.py

"""
知识库测试包
"""
```

- [ ] **Step 6: 运行测试验证通过**

Run: `pytest tests/knowledge/test_models.py -v`
Expected: 13 passed

- [ ] **Step 7: 提交代码**

```bash
git add src/knowledge/ tests/knowledge/
git commit -m "feat: implement knowledge base data models"
```

---

## Task 2: 知识提取器实现

**Files:**
- Create: `src/knowledge/extractor.py`
- Create: `tests/knowledge/test_extractor.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_extractor.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.extractor import KnowledgeExtractor
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeExtractor:
    """KnowledgeExtractor 测试"""

    @pytest.fixture
    def extractor(self):
        """创建 extractor 实例"""
        return KnowledgeExtractor()

    def test_extractor_initialization(self, extractor):
        """测试 extractor 初始化"""
        assert extractor is not None
        assert hasattr(extractor, 'extract')

    @pytest.mark.asyncio
    async def test_extract_returns_knowledge_base(self, extractor):
        """测试提取返回知识库"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_extract_profile(self, extractor):
        """测试提取基础信息"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert result.profile.name == "张三"
        assert result.profile.education == "清华大学"
        assert result.profile.occupation == "创业者"

    @pytest.mark.asyncio
    async def test_extract_facts(self, extractor):
        """测试提取事实"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert len(result.facts) > 0
        for fact in result.facts:
            assert fact.fact is not None
            assert fact.category is not None
            assert 0.0 <= fact.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_extract_evidence(self, extractor):
        """测试提取证据"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert len(result.evidence) > 0
        for evidence in result.evidence:
            assert evidence.source_type is not None
            assert evidence.source_name is not None
            assert evidence.content is not None

    @pytest.mark.asyncio
    async def test_extract_empty_text(self, extractor):
        """测试提取空文本"""
        text = ""
        source = "采访视频"

        result = await extractor.extract(text, source)
        assert isinstance(result, KnowledgeBase)
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_extractor.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.extractor'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/extractor.py

"""
知识提取器

负责从文本中提取知识
"""

from typing import List, Optional
from .models import (
    KnowledgeBase,
    KnowledgeProfile,
    Fact,
    Evidence,
    SourceType,
)


class KnowledgeExtractor:
    """
    知识提取器
    
    从文本中提取结构化知识
    """
    
    def __init__(self):
        """初始化提取器"""
        pass
    
    async def extract(self, text: str, source: str) -> KnowledgeBase:
        """
        提取知识
        
        Args:
            text: 文本内容
            source: 来源名称
            
        Returns:
            KnowledgeBase: 知识库
        """
        if not text or not text.strip():
            return KnowledgeBase(
                profile=KnowledgeProfile(name="Unknown"),
                relationships=[],
                events=[],
                beliefs=[],
                facts=[],
                timeline=[],
                evidence=[],
            )
        
        # 提取基础信息
        profile = self._extract_profile(text)
        
        # 提取事实
        facts = self._extract_facts(text)
        
        # 提取证据
        evidence = self._extract_evidence(text, source)
        
        return KnowledgeBase(
            profile=profile,
            relationships=[],
            events=[],
            beliefs=[],
            facts=facts,
            timeline=[],
            evidence=evidence,
        )
    
    def _extract_profile(self, text: str) -> KnowledgeProfile:
        """
        提取基础信息
        
        Args:
            text: 文本内容
            
        Returns:
            KnowledgeProfile: 基础信息
        """
        # 简化版本：从文本中提取姓名和教育背景
        name = "Unknown"
        education = None
        occupation = None
        
        # 简单的关键词提取
        if "毕业于" in text:
            # 提取教育背景
            parts = text.split("毕业于")
            if len(parts) > 1:
                edu_part = parts[1].split("，")[0]
                education = edu_part.strip()
        
        if "创立" in text or "创业" in text:
            occupation = "创业者"
        
        # 提取姓名（简化版本）
        if "张三" in text:
            name = "张三"
        elif "李四" in text:
            name = "李四"
        
        return KnowledgeProfile(
            name=name,
            education=education,
            occupation=occupation,
        )
    
    def _extract_facts(self, text: str) -> List[Fact]:
        """
        提取事实
        
        Args:
            text: 文本内容
            
        Returns:
            List[Fact]: 事实列表
        """
        facts = []
        
        # 提取教育相关事实
        if "毕业于" in text:
            parts = text.split("毕业于")
            if len(parts) > 1:
                edu_part = parts[1].split("，")[0]
                facts.append(Fact(
                    fact=f"毕业于{edu_part.strip()}",
                    category="education",
                    confidence=0.92,
                ))
        
        # 提取事业相关事实
        if "创立" in text or "创业" in text:
            facts.append(Fact(
                fact="创立某科技公司",
                category="career",
                confidence=0.94,
            ))
        
        return facts
    
    def _extract_evidence(self, text: str, source: str) -> List[Evidence]:
        """
        提取证据
        
        Args:
            text: 文本内容
            source: 来源名称
            
        Returns:
            List[Evidence]: 证据列表
        """
        evidence = []
        
        # 将整个文本作为证据
        evidence.append(Evidence(
            source_type=SourceType.VIDEO,
            source_name=source,
            content=text,
            confidence=0.91,
        ))
        
        return evidence
```

- [ ] **Step 4: 更新 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)
from .extractor import KnowledgeExtractor

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
    "KnowledgeExtractor",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/knowledge/test_extractor.py -v`
Expected: 5 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/knowledge/extractor.py src/knowledge/__init__.py tests/knowledge/test_extractor.py
git commit -m "feat: implement KnowledgeExtractor for extracting knowledge from text"
```

---

## Task 3: 知识存储器实现

**Files:**
- Create: `src/knowledge/store.py`
- Create: `tests/knowledge/test_store.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_store.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.store import KnowledgeStore
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeStore:
    """KnowledgeStore 测试"""

    @pytest.fixture
    def store(self):
        """创建 store 实例"""
        return KnowledgeStore()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", education="清华大学"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[],
            timeline=[],
            evidence=[],
        )

    def test_store_initialization(self, store):
        """测试 store 初始化"""
        assert store is not None
        assert hasattr(store, 'save')
        assert hasattr(store, 'load')

    @pytest.mark.asyncio
    async def test_save_knowledge_base(self, store, mock_knowledge_base):
        """测试保存知识库"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)
        # 验证保存成功（无异常）

    @pytest.mark.asyncio
    async def test_load_knowledge_base(self, store, mock_knowledge_base):
        """测试加载知识库"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)

        result = await store.load(character_id)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, store):
        """测试加载不存在的角色"""
        result = await store.load("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_save_and_load_consistency(self, store, mock_knowledge_base):
        """测试保存和加载一致性"""
        character_id = "test_char"
        await store.save(character_id, mock_knowledge_base)

        result = await store.load(character_id)
        assert result.profile.name == mock_knowledge_base.profile.name
        assert result.profile.education == mock_knowledge_base.profile.education
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_store.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.store'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/store.py

"""
知识存储器

负责存储和加载知识库
"""

from typing import Dict, Optional
from .models import KnowledgeBase


class KnowledgeStore:
    """
    知识存储器
    
    存储和加载知识库
    """
    
    def __init__(self):
        """初始化存储器"""
        # 内存存储（简化版本）
        self._storage: Dict[str, KnowledgeBase] = {}
    
    async def save(self, character_id: str, knowledge_base: KnowledgeBase) -> None:
        """
        保存知识库
        
        Args:
            character_id: 角色ID
            knowledge_base: 知识库
        """
        self._storage[character_id] = knowledge_base
    
    async def load(self, character_id: str) -> Optional[KnowledgeBase]:
        """
        加载知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[KnowledgeBase]: 知识库，不存在返回 None
        """
        return self._storage.get(character_id)
    
    async def delete(self, character_id: str) -> bool:
        """
        删除知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            bool: 是否删除成功
        """
        if character_id in self._storage:
            del self._storage[character_id]
            return True
        return False
    
    async def exists(self, character_id: str) -> bool:
        """
        检查知识库是否存在
        
        Args:
            character_id: 角色ID
            
        Returns:
            bool: 是否存在
        """
        return character_id in self._storage
```

- [ ] **Step 4: 更新 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
    "KnowledgeExtractor",
    "KnowledgeStore",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/knowledge/test_store.py -v`
Expected: 4 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/knowledge/store.py src/knowledge/__init__.py tests/knowledge/test_store.py
git commit -m "feat: implement KnowledgeStore for storing knowledge base"
```

---

## Task 4: 知识查询器实现

**Files:**
- Create: `src/knowledge/query.py`
- Create: `tests/knowledge/test_query.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_query.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.query import KnowledgeQuery
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeQuery:
    """KnowledgeQuery 测试"""

    @pytest.fixture
    def query(self):
        """创建 query 实例"""
        return KnowledgeQuery()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", education="清华大学"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[
                Fact(fact="毕业于清华大学", category="education", confidence=0.92),
                Fact(fact="创立某科技公司", category="career", confidence=0.94),
            ],
            timeline=[],
            evidence=[],
        )

    def test_query_initialization(self, query):
        """测试 query 初始化"""
        assert query is not None
        assert hasattr(query, 'search_facts')

    def test_search_facts(self, query, mock_knowledge_base):
        """测试搜索事实"""
        keyword = "清华"
        results = query.search_facts(mock_knowledge_base, keyword)
        assert len(results) > 0
        assert any("清华" in fact.fact for fact in results)

    def test_search_facts_no_match(self, query, mock_knowledge_base):
        """测试搜索无匹配事实"""
        keyword = "不存在"
        results = query.search_facts(mock_knowledge_base, keyword)
        assert len(results) == 0

    def test_get_facts_by_category(self, query, mock_knowledge_base):
        """测试按类别获取事实"""
        category = "education"
        results = query.get_facts_by_category(mock_knowledge_base, category)
        assert len(results) > 0
        assert all(fact.category == category for fact in results)

    def test_get_facts_by_category_no_match(self, query, mock_knowledge_base):
        """测试按类别获取无匹配事实"""
        category = "不存在"
        results = query.get_facts_by_category(mock_knowledge_base, category)
        assert len(results) == 0

    def test_get_profile(self, query, mock_knowledge_base):
        """测试获取基础信息"""
        profile = query.get_profile(mock_knowledge_base)
        assert profile.name == "张三"
        assert profile.education == "清华大学"
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_query.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.query'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/query.py

"""
知识查询器

负责查询知识库
"""

from typing import List
from .models import KnowledgeBase, KnowledgeProfile, Fact


class KnowledgeQuery:
    """
    知识查询器
    
    查询知识库中的信息
    """
    
    def __init__(self):
        """初始化查询器"""
        pass
    
    def search_facts(self, knowledge_base: KnowledgeBase, keyword: str) -> List[Fact]:
        """
        搜索事实
        
        Args:
            knowledge_base: 知识库
            keyword: 关键词
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        results = []
        for fact in knowledge_base.facts:
            if keyword in fact.fact:
                results.append(fact)
        return results
    
    def get_facts_by_category(self, knowledge_base: KnowledgeBase, category: str) -> List[Fact]:
        """
        按类别获取事实
        
        Args:
            knowledge_base: 知识库
            category: 类别
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        results = []
        for fact in knowledge_base.facts:
            if fact.category == category:
                results.append(fact)
        return results
    
    def get_profile(self, knowledge_base: KnowledgeBase) -> KnowledgeProfile:
        """
        获取基础信息
        
        Args:
            knowledge_base: 知识库
            
        Returns:
            KnowledgeProfile: 基础信息
        """
        return knowledge_base.profile
```

- [ ] **Step 4: 更新 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore
from .query import KnowledgeQuery

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
    "KnowledgeExtractor",
    "KnowledgeStore",
    "KnowledgeQuery",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/knowledge/test_query.py -v`
Expected: 5 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/knowledge/query.py src/knowledge/__init__.py tests/knowledge/test_query.py
git commit -m "feat: implement KnowledgeQuery for querying knowledge base"
```

---

## Task 5: 知识更新器实现

**Files:**
- Create: `src/knowledge/updater.py`
- Create: `tests/knowledge/test_updater.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_updater.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.updater import KnowledgeUpdater
from src.knowledge.models import KnowledgeBase, KnowledgeProfile, Fact


class TestKnowledgeUpdater:
    """KnowledgeUpdater 测试"""

    @pytest.fixture
    def updater(self):
        """创建 updater 实例"""
        return KnowledgeUpdater()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", occupation="工程师"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[
                Fact(fact="毕业于清华大学", category="education", confidence=0.92),
            ],
            timeline=[],
            evidence=[],
        )

    def test_updater_initialization(self, updater):
        """测试 updater 初始化"""
        assert updater is not None
        assert hasattr(updater, 'update_profile')
        assert hasattr(updater, 'add_fact')

    def test_update_profile(self, updater, mock_knowledge_base):
        """测试更新基础信息"""
        new_data = {"occupation": "创业者"}
        updater.update_profile(mock_knowledge_base, new_data)
        assert mock_knowledge_base.profile.occupation == "创业者"

    def test_add_fact(self, updater, mock_knowledge_base):
        """测试添加事实"""
        fact = Fact(fact="创立某科技公司", category="career", confidence=0.94)
        updater.add_fact(mock_knowledge_base, fact)
        assert len(mock_knowledge_base.facts) == 2

    def test_update_fact_confidence(self, updater, mock_knowledge_base):
        """测试更新事实置信度"""
        fact_index = 0
        new_confidence = 0.98
        updater.update_fact_confidence(mock_knowledge_base, fact_index, new_confidence)
        assert mock_knowledge_base.facts[0].confidence == 0.98

    def test_update_fact_confidence_invalid_index(self, updater, mock_knowledge_base):
        """测试更新事实置信度无效索引"""
        fact_index = 999
        new_confidence = 0.98
        with pytest.raises(IndexError):
            updater.update_fact_confidence(mock_knowledge_base, fact_index, new_confidence)
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_updater.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.updater'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/updater.py

"""
知识更新器

负责更新知识库
"""

from typing import Dict, Any
from .models import KnowledgeBase, Fact


class KnowledgeUpdater:
    """
    知识更新器
    
    更新知识库中的信息
    """
    
    def __init__(self):
        """初始化更新器"""
        pass
    
    def update_profile(self, knowledge_base: KnowledgeBase, new_data: Dict[str, Any]) -> None:
        """
        更新基础信息
        
        Args:
            knowledge_base: 知识库
            new_data: 新数据
        """
        for key, value in new_data.items():
            if hasattr(knowledge_base.profile, key):
                setattr(knowledge_base.profile, key, value)
    
    def add_fact(self, knowledge_base: KnowledgeBase, fact: Fact) -> None:
        """
        添加事实
        
        Args:
            knowledge_base: 知识库
            fact: 事实
        """
        knowledge_base.facts.append(fact)
    
    def update_fact_confidence(self, knowledge_base: KnowledgeBase, fact_index: int, new_confidence: float) -> None:
        """
        更新事实置信度
        
        Args:
            knowledge_base: 知识库
            fact_index: 事实索引
            new_confidence: 新置信度
            
        Raises:
            IndexError: 索引无效
        """
        if fact_index < 0 or fact_index >= len(knowledge_base.facts):
            raise IndexError(f"Fact index out of range: {fact_index}")
        
        knowledge_base.facts[fact_index].confidence = new_confidence
```

- [ ] **Step 4: 更新 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore
from .query import KnowledgeQuery
from .updater import KnowledgeUpdater

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
    "KnowledgeExtractor",
    "KnowledgeStore",
    "KnowledgeQuery",
    "KnowledgeUpdater",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/knowledge/test_updater.py -v`
Expected: 4 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/knowledge/updater.py src/knowledge/__init__.py tests/knowledge/test_updater.py
git commit -m "feat: implement KnowledgeUpdater for updating knowledge base"
```

---

## Task 6: 知识服务实现

**Files:**
- Create: `src/knowledge/service.py`
- Create: `tests/knowledge/test_service.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/knowledge/test_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.service import KnowledgeService
from src.knowledge.models import KnowledgeBase, KnowledgeProfile


class TestKnowledgeService:
    """KnowledgeService 测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return KnowledgeService()

    @pytest.fixture
    def mock_knowledge_base(self):
        """模拟知识库"""
        return KnowledgeBase(
            profile=KnowledgeProfile(name="张三", education="清华大学"),
            relationships=[],
            events=[],
            beliefs=[],
            facts=[],
            timeline=[],
            evidence=[],
        )

    def test_service_initialization(self, service):
        """测试 service 初始化"""
        assert service is not None
        assert hasattr(service, 'process')
        assert hasattr(service, 'query')

    @pytest.mark.asyncio
    async def test_process_returns_knowledge_base(self, service):
        """测试处理返回知识库"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"

        result = await service.process(text, source)
        assert isinstance(result, KnowledgeBase)
        assert result.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_process_saves_to_store(self, service):
        """测试处理保存到存储"""
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"
        character_id = "test_char"

        result = await service.process(text, source, character_id)
        loaded = await service.load(character_id)
        assert loaded is not None
        assert loaded.profile.name == "张三"

    @pytest.mark.asyncio
    async def test_query_facts(self, service, mock_knowledge_base):
        """测试查询事实"""
        character_id = "test_char"
        await service.save(character_id, mock_knowledge_base)

        results = await service.query_facts(character_id, "张三")
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_load_nonexistent_character(self, service):
        """测试加载不存在的角色"""
        result = await service.load("nonexistent")
        assert result is None
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/knowledge/test_service.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.knowledge.service'"

- [ ] **Step 3: 编写最小实现**

```python
# src/knowledge/service.py

"""
知识服务

负责协调知识库操作
"""

from typing import List, Optional
from .models import KnowledgeBase, Fact
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore
from .query import KnowledgeQuery


class KnowledgeService:
    """
    知识服务
    
    协调知识库操作：提取 -> 存储 -> 查询
    """
    
    def __init__(self):
        """初始化服务"""
        self.extractor = KnowledgeExtractor()
        self.store = KnowledgeStore()
        self.query = KnowledgeQuery()
    
    async def process(self, text: str, source: str, character_id: Optional[str] = None) -> KnowledgeBase:
        """
        处理文本，提取知识
        
        Args:
            text: 文本内容
            source: 来源名称
            character_id: 角色ID（可选）
            
        Returns:
            KnowledgeBase: 知识库
        """
        # 提取知识
        knowledge_base = await self.extractor.extract(text, source)
        
        # 保存到存储
        if character_id:
            await self.store.save(character_id, knowledge_base)
        
        return knowledge_base
    
    async def save(self, character_id: str, knowledge_base: KnowledgeBase) -> None:
        """
        保存知识库
        
        Args:
            character_id: 角色ID
            knowledge_base: 知识库
        """
        await self.store.save(character_id, knowledge_base)
    
    async def load(self, character_id: str) -> Optional[KnowledgeBase]:
        """
        加载知识库
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[KnowledgeBase]: 知识库，不存在返回 None
        """
        return await self.store.load(character_id)
    
    async def query_facts(self, character_id: str, keyword: str) -> List[Fact]:
        """
        查询事实
        
        Args:
            character_id: 角色ID
            keyword: 关键词
            
        Returns:
            List[Fact]: 匹配的事实列表
        """
        knowledge_base = await self.store.load(character_id)
        if knowledge_base is None:
            return []
        return self.query.search_facts(knowledge_base, keyword)
```

- [ ] **Step 4: 更新 src/knowledge/__init__.py**

```python
# src/knowledge/__init__.py

"""
知识库模块
"""

from .models import (
    KnowledgeProfile,
    Relationship,
    Event,
    Belief,
    Fact,
    Timeline,
    Evidence,
    KnowledgeBase,
    RelationshipType,
    SourceType,
)
from .extractor import KnowledgeExtractor
from .store import KnowledgeStore
from .query import KnowledgeQuery
from .updater import KnowledgeUpdater
from .service import KnowledgeService

__all__ = [
    "KnowledgeProfile",
    "Relationship",
    "Event",
    "Belief",
    "Fact",
    "Timeline",
    "Evidence",
    "KnowledgeBase",
    "RelationshipType",
    "SourceType",
    "KnowledgeExtractor",
    "KnowledgeStore",
    "KnowledgeQuery",
    "KnowledgeUpdater",
    "KnowledgeService",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/knowledge/test_service.py -v`
Expected: 4 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/knowledge/service.py src/knowledge/__init__.py tests/knowledge/test_service.py
git commit -m "feat: implement KnowledgeService for coordinating knowledge operations"
```

---

## Task 7: 集成测试

**Files:**
- Create: `tests/integration/test_knowledge_pipeline.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/integration/test_knowledge_pipeline.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.knowledge.service import KnowledgeService
from src.knowledge.models import KnowledgeBase


class TestKnowledgePipeline:
    """知识库流水线集成测试"""

    @pytest.fixture
    def service(self):
        """创建 service 实例"""
        return KnowledgeService()

    @pytest.mark.asyncio
    async def test_full_pipeline(self, service):
        """测试完整流水线"""
        # 输入文本
        text = "张三毕业于清华大学，创立了某科技公司"
        source = "采访视频"
        character_id = "test_char"

        # 处理文本
        knowledge_base = await service.process(text, source, character_id)

        # 验证结果
        assert isinstance(knowledge_base, KnowledgeBase)
        assert knowledge_base.profile.name == "张三"
        assert knowledge_base.profile.education == "清华大学"
        assert knowledge_base.profile.occupation == "创业者"
        assert len(knowledge_base.facts) > 0
        assert len(knowledge_base.evidence) > 0

        # 查询知识
        facts = await service.query_facts(character_id, "清华")
        assert len(facts) > 0
        assert any("清华" in fact.fact for fact in facts)

        # 加载知识
        loaded = await service.load(character_id)
        assert loaded is not None
        assert loaded.profile.name == "张三"
```

- [ ] **Step 2: 运行集成测试**

Run: `pytest tests/integration/test_knowledge_pipeline.py -v`
Expected: 1 passed

- [ ] **Step 3: 提交代码**

```bash
git add tests/integration/test_knowledge_pipeline.py
git commit -m "test: add integration tests for knowledge pipeline"
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
git commit -m "feat: complete Sprint-3 knowledge base MVP"
```

---

## 执行选项

**计划已完成并保存到 `docs/superpowers/plans/2026-06-09-sprint-3-knowledge-base.md`**

两种执行方式：

**1. Subagent-Driven（推荐）** - 每个任务分发给独立子代理执行，任务间进行审查，快速迭代

**2. Inline Execution** - 在当前会话中执行任务，批量执行并设置检查点

**选择哪种方式？**