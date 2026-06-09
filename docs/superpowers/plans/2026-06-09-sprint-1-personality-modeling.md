# Sprint-1 人格建模 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现失忆宝宝最小可运行版本（MVP），支持用户输入人物文本资料，系统解析素材，提取人格证据，构建人格画像，输出人格分析结果。

**Architecture:** 采用四层架构（Material Layer → Character Layer → Interaction Layer → Memory Layer），Sprint-1 聚焦于 Material Layer 和 Character Layer 的核心功能。使用 Pydantic 进行数据验证，FastAPI 提供 API 接口，LangGraph 编排 Agent 工作流。

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, LangGraph, pytest, httpx

---

## 文件结构

```
src/
├── __init__.py
├── main.py                          # FastAPI 应用入口
├── config.py                        # 配置管理
├── personality/
│   ├── __init__.py
│   ├── profile.py                   # PersonalityProfile 数据模型
│   ├── big_five.py                  # BigFiveProfile 数据模型
│   ├── enneagram.py                 # EnneagramProfile 数据模型
│   ├── evidence.py                  # PersonalityEvidence 数据模型
│   └── agent.py                     # Personality Agent
├── material/
│   ├── __init__.py
│   └── text_parser.py               # Text Material Parser
└── common/
    ├── __init__.py
    └── exceptions.py                # 自定义异常

tests/
├── __init__.py
├── conftest.py                      # pytest 配置
├── personality/
│   ├── __init__.py
│   ├── test_profile.py              # PersonalityProfile 测试
│   ├── test_big_five.py             # BigFiveProfile 测试
│   ├── test_enneagram.py            # EnneagramProfile 测试
│   ├── test_evidence.py             # PersonalityEvidence 测试
│   └── test_agent.py                # Personality Agent 测试
└── material/
    ├── __init__.py
    └── test_text_parser.py          # Text Material Parser 测试

requirements.txt                     # 依赖包
.env.example                         # 环境变量示例
.gitignore                           # Git 忽略文件
```

---

## Task 1: 项目初始化

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `src/__init__.py`
- Create: `src/config.py`
- Create: `src/common/__init__.py`
- Create: `src/common/exceptions.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
langgraph==0.0.20
httpx==0.26.0
python-dotenv==1.0.0
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
```

- [ ] **Step 2: 创建 .env.example**

```env
# OpenAI API 配置
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# 应用配置
APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
```

- [ ] **Step 3: 创建 .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Testing
.coverage
htmlcov/
.pytest_cache/

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 4: 创建 src/__init__.py**

```python
"""
失忆宝宝（Memory Baby）- 通过人物素材重建数字人格
"""

__version__ = "0.1.0"
```

- [ ] **Step 5: 创建 src/config.py**

```python
"""
应用配置管理
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # OpenAI 配置
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    
    # 应用配置
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置（缓存）"""
    return Settings()
```

- [ ] **Step 6: 创建 src/common/__init__.py**

```python
"""
通用工具模块
"""

from .exceptions import (
    PersonalityError,
    ValidationError,
    PersonalityProfileError,
    EvidenceError,
)

__all__ = [
    "PersonalityError",
    "ValidationError",
    "PersonalityProfileError",
    "EvidenceError",
]
```

- [ ] **Step 7: 创建 src/common/exceptions.py**

```python
"""
自定义异常
"""


class PersonalityError(Exception):
    """人格系统基础异常"""
    pass


class ValidationError(PersonalityError):
    """数据验证异常"""
    pass


class PersonalityProfileError(PersonalityError):
    """人格画像异常"""
    pass


class EvidenceError(PersonalityError):
    """人格证据异常"""
    pass
```

- [ ] **Step 8: 创建 tests/__init__.py**

```python
"""
测试包
"""
```

- [ ] **Step 9: 创建 tests/conftest.py**

```python
"""
pytest 配置和 fixtures
"""

import pytest
from src.config import Settings, get_settings


@pytest.fixture
def settings():
    """测试配置"""
    return Settings(
        openai_api_key="test-key",
        openai_api_base="http://localhost:8000",
        app_env="testing",
        app_debug=True,
    )


@pytest.fixture(autouse=True)
def override_settings(settings):
    """覆盖配置"""
    get_settings.cache_clear()
    get_settings.cache_clear()
    return settings
```

- [ ] **Step 10: 运行测试验证项目结构**

Run: `pytest tests/ -v`
Expected: 收集到 0 个测试，无错误

- [ ] **Step 11: 提交代码**

```bash
git add requirements.txt .env.example .gitignore src/ tests/
git commit -m "feat: initialize project structure with config and exceptions"
```

---

## Task 2: PersonalityProfile 数据模型

**Files:**
- Create: `src/personality/__init__.py`
- Create: `src/personality/profile.py`
- Create: `tests/personality/__init__.py`
- Create: `tests/personality/test_profile.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/personality/test_profile.py

import pytest
from pydantic import ValidationError
from src.personality.profile import PersonalityProfile


class TestPersonalityProfile:
    """PersonalityProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建画像"""
        profile = PersonalityProfile(
            achievement_drive=0.8,
            curiosity=0.7,
            risk_preference=0.6,
            security_need=0.4,
            dominance=0.5,
            empathy=0.9,
            independence=0.7,
            responsibility=0.8,
            creativity=0.6,
            social_need=0.5,
        )
        assert profile.achievement_drive == 0.8
        assert profile.curiosity == 0.7
        assert profile.risk_preference == 0.6
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建画像"""
        profile = PersonalityProfile()
        assert profile.achievement_drive == 0.5
        assert profile.curiosity == 0.5
        assert profile.risk_preference == 0.5
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            PersonalityProfile(achievement_drive=1.5)
        
        with pytest.raises(ValidationError):
            PersonalityProfile(achievement_drive=-0.1)
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = PersonalityProfile(achievement_drive=0.8)
        data = profile.model_dump()
        assert data["achievement_drive"] == 0.8
        assert "curiosity" in data
    
    def test_profile_deserialization(self):
        """测试反序列化"""
        data = {
            "achievement_drive": 0.8,
            "curiosity": 0.7,
            "risk_preference": 0.6,
            "security_need": 0.4,
            "dominance": 0.5,
            "empathy": 0.9,
            "independence": 0.7,
            "responsibility": 0.8,
            "creativity": 0.6,
            "social_need": 0.5,
        }
        profile = PersonalityProfile(**data)
        assert profile.achievement_drive == 0.8
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = PersonalityProfile(achievement_drive=0.8)
        json_str = profile.model_dump_json()
        assert '"achievement_drive":0.8' in json_str
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/personality/test_profile.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.personality.profile'"

- [ ] **Step 3: 编写最小实现**

```python
# src/personality/__init__.py

"""
人格系统模块
"""

from .profile import PersonalityProfile

__all__ = ["PersonalityProfile"]
```

```python
# src/personality/profile.py

"""
人格画像数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional


class PersonalityProfile(BaseModel):
    """
    人格画像
    
    包含 10 个人格维度，每个维度取值范围 0.0 ~ 1.0
    """
    
    achievement_drive: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="成就驱动"
    )
    
    curiosity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="好奇心"
    )
    
    risk_preference: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="风险偏好"
    )
    
    security_need: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="安全需求"
    )
    
    dominance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="支配性"
    )
    
    empathy: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="共情能力"
    )
    
    independence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="独立性"
    )
    
    responsibility: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="责任感"
    )
    
    creativity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="创造力"
    )
    
    social_need: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="社交需求"
    )
    
    class Config:
        """Pydantic 配置"""
        json_schema_extra = {
            "example": {
                "achievement_drive": 0.8,
                "curiosity": 0.7,
                "risk_preference": 0.6,
                "security_need": 0.4,
                "dominance": 0.5,
                "empathy": 0.9,
                "independence": 0.7,
                "responsibility": 0.8,
                "creativity": 0.6,
                "social_need": 0.5,
            }
        }
```

- [ ] **Step 4: 运行测试验证通过**

Run: `pytest tests/personality/test_profile.py -v`
Expected: 6 passed

- [ ] **Step 5: 提交代码**

```bash
git add src/personality/ tests/personality/
git commit -m "feat: implement PersonalityProfile data model with validation"
```

---

## Task 3: BigFiveProfile 数据模型

**Files:**
- Create: `src/personality/big_five.py`
- Create: `tests/personality/test_big_five.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/personality/test_big_five.py

import pytest
from pydantic import ValidationError
from src.personality.big_five import BigFiveProfile


class TestBigFiveProfile:
    """BigFiveProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建大五人格"""
        profile = BigFiveProfile(
            openness=0.75,
            conscientiousness=0.80,
            extraversion=0.72,
            agreeableness=0.65,
            neuroticism=0.30,
        )
        assert profile.openness == 0.75
        assert profile.conscientiousness == 0.80
        assert profile.extraversion == 0.72
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建大五人格"""
        profile = BigFiveProfile()
        assert profile.openness == 0.5
        assert profile.conscientiousness == 0.5
        assert profile.extraversion == 0.5
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            BigFiveProfile(openness=1.5)
        
        with pytest.raises(ValidationError):
            BigFiveProfile(openness=-0.1)
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = BigFiveProfile(openness=0.75)
        data = profile.model_dump()
        assert data["openness"] == 0.75
        assert "conscientiousness" in data
    
    def test_profile_deserialization(self):
        """测试反序列化"""
        data = {
            "openness": 0.75,
            "conscientiousness": 0.80,
            "extraversion": 0.72,
            "agreeableness": 0.65,
            "neuroticism": 0.30,
        }
        profile = BigFiveProfile(**data)
        assert profile.openness == 0.75
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = BigFiveProfile(openness=0.75)
        json_str = profile.model_dump_json()
        assert '"openness":0.75' in json_str
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/personality/test_big_five.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.personality.big_five'"

- [ ] **Step 3: 编写最小实现**

```python
# src/personality/big_five.py

"""
大五人格数据模型
"""

from pydantic import BaseModel, Field


class BigFiveProfile(BaseModel):
    """
    大五人格（Big Five / OCEAN）
    
    包含 5 个人格维度，每个维度取值范围 0.0 ~ 1.0
    """
    
    openness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="开放性"
    )
    
    conscientiousness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="尽责性"
    )
    
    extraversion: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="外向性"
    )
    
    agreeableness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="宜人性"
    )
    
    neuroticism: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="神经质"
    )
    
    class Config:
        """Pydantic 配置"""
        json_schema_extra = {
            "example": {
                "openness": 0.75,
                "conscientiousness": 0.80,
                "extraversion": 0.72,
                "agreeableness": 0.65,
                "neuroticism": 0.30,
            }
        }
```

- [ ] **Step 4: 更新 src/personality/__init__.py**

```python
# src/personality/__init__.py

"""
人格系统模块
"""

from .profile import PersonalityProfile
from .big_five import BigFiveProfile

__all__ = [
    "PersonalityProfile",
    "BigFiveProfile",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/personality/test_big_five.py -v`
Expected: 6 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/personality/big_five.py src/personality/__init__.py tests/personality/test_big_five.py
git commit -m "feat: implement BigFiveProfile data model"
```

---

## Task 4: EnneagramProfile 数据模型

**Files:**
- Create: `src/personality/enneagram.py`
- Create: `tests/personality/test_enneagram.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/personality/test_enneagram.py

import pytest
from pydantic import ValidationError
from src.personality.enneagram import EnneagramProfile


class TestEnneagramProfile:
    """EnneagramProfile 测试"""
    
    def test_create_profile_with_valid_data(self):
        """测试使用有效数据创建九型人格"""
        profile = EnneagramProfile(
            type1=0.10,
            type2=0.08,
            type3=0.30,
            type4=0.05,
            type5=0.12,
            type6=0.07,
            type7=0.18,
            type8=0.41,
            type9=0.09,
        )
        assert profile.type8 == 0.41
        assert profile.type3 == 0.30
        assert profile.type7 == 0.18
    
    def test_create_profile_with_default_values(self):
        """测试使用默认值创建九型人格"""
        profile = EnneagramProfile()
        assert profile.type1 == 0.111
        assert profile.type2 == 0.111
        assert profile.type3 == 0.111
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            EnneagramProfile(type1=1.5)
        
        with pytest.raises(ValidationError):
            EnneagramProfile(type1=-0.1)
    
    def test_get_top3(self):
        """测试获取前三人格类型"""
        profile = EnneagramProfile(
            type1=0.10,
            type2=0.08,
            type3=0.30,
            type4=0.05,
            type5=0.12,
            type6=0.07,
            type7=0.18,
            type8=0.41,
            type9=0.09,
        )
        top3 = profile.get_top3()
        assert len(top3) == 3
        assert top3[0][0] == "type8"
        assert top3[1][0] == "type3"
        assert top3[2][0] == "type7"
    
    def test_profile_serialization(self):
        """测试序列化"""
        profile = EnneagramProfile(type8=0.41)
        data = profile.model_dump()
        assert data["type8"] == 0.41
        assert "type1" in data
    
    def test_profile_to_json(self):
        """测试导出为 JSON"""
        profile = EnneagramProfile(type8=0.41)
        json_str = profile.model_dump_json()
        assert '"type8":0.41' in json_str
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/personality/test_enneagram.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.personality.enneagram'"

- [ ] **Step 3: 编写最小实现**

```python
# src/personality/enneagram.py

"""
九型人格数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Tuple


class EnneagramProfile(BaseModel):
    """
    九型人格（Enneagram）
    
    包含 9 种人格类型，每个类型取值范围 0.0 ~ 1.0
    """
    
    type1: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="完美主义者"
    )
    
    type2: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="助人者"
    )
    
    type3: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="成就者"
    )
    
    type4: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="个人主义者"
    )
    
    type5: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="观察者"
    )
    
    type6: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="忠诚者"
    )
    
    type7: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="热情者"
    )
    
    type8: float = Field(
        default=0.111,
        ge=0.0,
        le=1.0,
        description="挑战者"
    )
    
    type9: float = Field(
        default=0.112,
        ge=0.0,
        le=1.0,
        description="和平者"
    )
    
    def get_top3(self) -> List[Tuple[str, float]]:
        """
        获取前三人格类型
        
        Returns:
            List[Tuple[str, float]]: [(类型名, 分数), ...]
        """
        scores = {
            "type1": self.type1,
            "type2": self.type2,
            "type3": self.type3,
            "type4": self.type4,
            "type5": self.type5,
            "type6": self.type6,
            "type7": self.type7,
            "type8": self.type8,
            "type9": self.type9,
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:3]
    
    class Config:
        """Pydantic 配置"""
        json_schema_extra = {
            "example": {
                "type1": 0.10,
                "type2": 0.08,
                "type3": 0.30,
                "type4": 0.05,
                "type5": 0.12,
                "type6": 0.07,
                "type7": 0.18,
                "type8": 0.41,
                "type9": 0.09,
            }
        }
```

- [ ] **Step 4: 更新 src/personality/__init__.py**

```python
# src/personality/__init__.py

"""
人格系统模块
"""

from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile

__all__ = [
    "PersonalityProfile",
    "BigFiveProfile",
    "EnneagramProfile",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/personality/test_enneagram.py -v`
Expected: 6 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/personality/enneagram.py src/personality/__init__.py tests/personality/test_enneagram.py
git commit -m "feat: implement EnneagramProfile data model with top3 method"
```

---

## Task 5: PersonalityEvidence 数据模型

**Files:**
- Create: `src/personality/evidence.py`
- Create: `tests/personality/test_evidence.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/personality/test_evidence.py

import pytest
from pydantic import ValidationError
from src.personality.evidence import PersonalityEvidence


class TestPersonalityEvidence:
    """PersonalityEvidence 测试"""
    
    def test_create_evidence_with_valid_data(self):
        """测试使用有效数据创建证据"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        assert evidence.trait == "risk_preference"
        assert evidence.score == 0.91
        assert evidence.evidence == "创业最大的风险是不创业"
        assert evidence.source == "采访视频"
        assert evidence.confidence == 0.88
    
    def test_create_evidence_with_metadata(self):
        """测试使用元数据创建证据"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
            metadata={"timestamp": "12:33", "speaker": "角色本人"},
        )
        assert evidence.metadata["timestamp"] == "12:33"
        assert evidence.metadata["speaker"] == "角色本人"
    
    def test_invalid_trait_validation(self):
        """测试无效的人格维度"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="invalid_trait",
                score=0.91,
                evidence="test",
                source="test",
                confidence=0.88,
            )
    
    def test_score_range_validation(self):
        """测试分数范围验证"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=1.5,
                evidence="test",
                source="test",
                confidence=0.88,
            )
        
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=-0.1,
                evidence="test",
                source="test",
                confidence=0.88,
            )
    
    def test_confidence_range_validation(self):
        """测试置信度范围验证"""
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="test",
                source="test",
                confidence=1.5,
            )
        
        with pytest.raises(ValidationError):
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="test",
                source="test",
                confidence=-0.1,
            )
    
    def test_evidence_serialization(self):
        """测试序列化"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        data = evidence.model_dump()
        assert data["trait"] == "risk_preference"
        assert data["score"] == 0.91
    
    def test_evidence_deserialization(self):
        """测试反序列化"""
        data = {
            "trait": "risk_preference",
            "score": 0.91,
            "evidence": "创业最大的风险是不创业",
            "source": "采访视频",
            "confidence": 0.88,
        }
        evidence = PersonalityEvidence(**data)
        assert evidence.trait == "risk_preference"
    
    def test_evidence_to_json(self):
        """测试导出为 JSON"""
        evidence = PersonalityEvidence(
            trait="risk_preference",
            score=0.91,
            evidence="创业最大的风险是不创业",
            source="采访视频",
            confidence=0.88,
        )
        json_str = evidence.model_dump_json()
        assert '"trait":"risk_preference"' in json_str
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/personality/test_evidence.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.personality.evidence'"

- [ ] **Step 3: 编写最小实现**

```python
# src/personality/evidence.py

"""
人格证据数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


class PersonalityTrait(str, Enum):
    """人格维度枚举"""
    ACHIEVEMENT_DRIVE = "achievement_drive"
    CURIOSITY = "curiosity"
    RISK_PREFERENCE = "risk_preference"
    SECURITY_NEED = "security_need"
    DOMINANCE = "dominance"
    EMPATHY = "empathy"
    INDEPENDENCE = "independence"
    RESPONSIBILITY = "responsibility"
    CREATIVITY = "creativity"
    SOCIAL_NEED = "social_need"


class PersonalityEvidence(BaseModel):
    """
    人格证据
    
    素材解析层与人格建模层之间的数据桥梁
    """
    
    trait: PersonalityTrait = Field(
        ...,
        description="人格维度"
    )
    
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="证据强度"
    )
    
    evidence: str = Field(
        ...,
        min_length=1,
        description="原始证据"
    )
    
    source: str = Field(
        ...,
        min_length=1,
        description="证据来源"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="置信度"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="扩展信息"
    )
    
    class Config:
        """Pydantic 配置"""
        json_schema_extra = {
            "example": {
                "trait": "risk_preference",
                "score": 0.91,
                "evidence": "创业最大的风险是不创业",
                "source": "采访视频",
                "confidence": 0.88,
                "metadata": {
                    "timestamp": "12:33",
                    "speaker": "角色本人",
                },
            }
        }
```

- [ ] **Step 4: 更新 src/personality/__init__.py**

```python
# src/personality/__init__.py

"""
人格系统模块
"""

from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile
from .evidence import PersonalityEvidence, PersonalityTrait

__all__ = [
    "PersonalityProfile",
    "BigFiveProfile",
    "EnneagramProfile",
    "PersonalityEvidence",
    "PersonalityTrait",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/personality/test_evidence.py -v`
Expected: 8 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/personality/evidence.py src/personality/__init__.py tests/personality/test_evidence.py
git commit -m "feat: implement PersonalityEvidence data model with trait validation"
```

---

## Task 6: Personality Agent 实现

**Files:**
- Create: `src/personality/agent.py`
- Create: `tests/personality/test_agent.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/personality/test_agent.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.personality.agent import PersonalityAgent
from src.personality.evidence import PersonalityEvidence
from src.personality.profile import PersonalityProfile
from src.personality.big_five import BigFiveProfile
from src.personality.enneagram import EnneagramProfile


class TestPersonalityAgent:
    """PersonalityAgent 测试"""
    
    @pytest.fixture
    def agent(self):
        """创建 agent 实例"""
        return PersonalityAgent()
    
    @pytest.fixture
    def sample_evidence(self):
        """示例证据"""
        return [
            PersonalityEvidence(
                trait="risk_preference",
                score=0.91,
                evidence="创业最大的风险是不创业",
                source="采访视频",
                confidence=0.88,
            ),
            PersonalityEvidence(
                trait="achievement_drive",
                score=0.85,
                evidence="我总是追求卓越",
                source="人物自传",
                confidence=0.90,
            ),
            PersonalityEvidence(
                trait="curiosity",
                score=0.78,
                evidence="我喜欢探索未知领域",
                source="博客文章",
                confidence=0.75,
            ),
        ]
    
    def test_agent_initialization(self, agent):
        """测试 agent 初始化"""
        assert agent is not None
        assert hasattr(agent, 'analyze')
    
    @pytest.mark.asyncio
    async def test_analyze_returns_profile(self, agent, sample_evidence):
        """测试分析返回人格画像"""
        result = await agent.analyze(sample_evidence)
        assert isinstance(result, dict)
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result
    
    @pytest.mark.asyncio
    async def test_analyze_personality_scores(self, agent, sample_evidence):
        """测试人格分数"""
        result = await agent.analyze(sample_evidence)
        personality = result["personality"]
        assert 0.0 <= personality["risk_preference"] <= 1.0
        assert 0.0 <= personality["achievement_drive"] <= 1.0
        assert 0.0 <= personality["curiosity"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_big_five_scores(self, agent, sample_evidence):
        """测试大五人格分数"""
        result = await agent.analyze(sample_evidence)
        big_five = result["big_five"]
        assert 0.0 <= big_five["openness"] <= 1.0
        assert 0.0 <= big_five["conscientiousness"] <= 1.0
        assert 0.0 <= big_five["extraversion"] <= 1.0
        assert 0.0 <= big_five["agreeableness"] <= 1.0
        assert 0.0 <= big_five["neuroticism"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_enneagram_top3(self, agent, sample_evidence):
        """测试九型人格前三"""
        result = await agent.analyze(sample_evidence)
        enneagram_top3 = result["enneagram_top3"]
        assert len(enneagram_top3) == 3
        for type_name, score in enneagram_top3.items():
            assert 0.0 <= score <= 1.0
    
    @pytest.mark.asyncio
    async def test_analyze_empty_evidence(self, agent):
        """测试空证据"""
        result = await agent.analyze([])
        assert isinstance(result, dict)
        assert "personality" in result
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/personality/test_agent.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.personality.agent'"

- [ ] **Step 3: 编写最小实现**

```python
# src/personality/agent.py

"""
Personality Agent

负责根据人格证据构建人格画像
"""

from typing import List, Dict, Any
from .evidence import PersonalityEvidence, PersonalityTrait
from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile


class PersonalityAgent:
    """
    人格 Agent
    
    根据人格证据分析并生成人格画像
    """
    
    def __init__(self):
        """初始化 agent"""
        pass
    
    async def analyze(self, evidence_list: List[PersonalityEvidence]) -> Dict[str, Any]:
        """
        分析人格证据，生成人格画像
        
        Args:
            evidence_list: 人格证据列表
            
        Returns:
            Dict: 包含 personality, big_five, enneagram_top3 的结果
        """
        # 计算人格画像
        personality = self._calculate_personality(evidence_list)
        
        # 计算大五人格
        big_five = self._calculate_big_five(personality)
        
        # 计算九型人格
        enneagram = self._calculate_enneagram(personality)
        enneagram_top3 = dict(enneagram.get_top3())
        
        return {
            "personality": personality.model_dump(),
            "big_five": big_five.model_dump(),
            "enneagram_top3": enneagram_top3,
        }
    
    def _calculate_personality(self, evidence_list: List[PersonalityEvidence]) -> PersonalityProfile:
        """
        计算人格画像
        
        Args:
            evidence_list: 人格证据列表
            
        Returns:
            PersonalityProfile: 人格画像
        """
        # 初始化默认值
        traits = {trait.value: 0.5 for trait in PersonalityTrait}
        
        # 根据证据更新分数
        for evidence in evidence_list:
            trait = evidence.trait.value
            # 加权平均：分数 * 置信度
            if trait in traits:
                traits[trait] = evidence.score * evidence.confidence
        
        return PersonalityProfile(**traits)
    
    def _calculate_big_five(self, personality: PersonalityProfile) -> BigFiveProfile:
        """
        计算大五人格
        
        基于人格画像映射到大五人格维度
        
        Args:
            personality: 人格画像
            
        Returns:
            BigFiveProfile: 大五人格
        """
        # 映射关系（简化版本）
        openness = (personality.curiosity + personality.creativity) / 2
        conscientiousness = (personality.responsibility + personality.achievement_drive) / 2
        extraversion = (personality.social_need + personality.dominance) / 2
        agreeableness = (personality.empathy + (1 - personality.dominance)) / 2
        neuroticism = (personality.security_need + (1 - personality.independence)) / 2
        
        return BigFiveProfile(
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
        )
    
    def _calculate_enneagram(self, personality: PersonalityProfile) -> EnneagramProfile:
        """
        计算九型人格
        
        基于人格画像映射到九型人格
        
        Args:
            personality: 人格画像
            
        Returns:
            EnneagramProfile: 九型人格
        """
        # 映射关系（简化版本）
        type1 = (personality.responsibility + personality.achievement_drive) / 2
        type2 = (personality.empathy + personality.social_need) / 2
        type3 = (personality.achievement_drive + personality.dominance) / 2
        type4 = (personality.creativity + personality.independence) / 2
        type5 = (personality.curiosity + personality.independence) / 2
        type6 = (personality.security_need + personality.responsibility) / 2
        type7 = (personality.curiosity + personality.social_need) / 2
        type8 = (personality.dominance + personality.risk_preference) / 2
        type9 = ((1 - personality.dominance) + (1 - personality.security_need)) / 2
        
        return EnneagramProfile(
            type1=type1,
            type2=type2,
            type3=type3,
            type4=type4,
            type5=type5,
            type6=type6,
            type7=type7,
            type8=type8,
            type9=type9,
        )
```

- [ ] **Step 4: 更新 src/personality/__init__.py**

```python
# src/personality/__init__.py

"""
人格系统模块
"""

from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile
from .evidence import PersonalityEvidence, PersonalityTrait
from .agent import PersonalityAgent

__all__ = [
    "PersonalityProfile",
    "BigFiveProfile",
    "EnneagramProfile",
    "PersonalityEvidence",
    "PersonalityTrait",
    "PersonalityAgent",
]
```

- [ ] **Step 5: 运行测试验证通过**

Run: `pytest tests/personality/test_agent.py -v`
Expected: 7 passed

- [ ] **Step 6: 提交代码**

```bash
git add src/personality/agent.py src/personality/__init__.py tests/personality/test_agent.py
git commit -m "feat: implement PersonalityAgent with Big Five and Enneagram mapping"
```

---

## Task 7: Text Material Parser 实现

**Files:**
- Create: `src/material/__init__.py`
- Create: `src/material/text_parser.py`
- Create: `tests/material/__init__.py`
- Create: `tests/material/test_text_parser.py`

- [ ] **Step 1: 编写失败的测试**

```python
# tests/material/test_text_parser.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.material.text_parser import TextMaterialParser
from src.personality.evidence import PersonalityEvidence


class TestTextMaterialParser:
    """TextMaterialParser 测试"""
    
    @pytest.fixture
    def parser(self):
        """创建 parser 实例"""
        return TextMaterialParser()
    
    def test_parser_initialization(self, parser):
        """测试 parser 初始化"""
        assert parser is not None
        assert hasattr(parser, 'parse')
    
    @pytest.mark.asyncio
    async def test_parse_returns_evidence_list(self, parser):
        """测试解析返回证据列表"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(e, PersonalityEvidence) for e in result)
    
    @pytest.mark.asyncio
    async def test_parse_with_source(self, parser):
        """测试解析包含来源"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert evidence.source == "采访视频"
    
    @pytest.mark.asyncio
    async def test_parse_empty_text(self, parser):
        """测试解析空文本"""
        result = await parser.parse("", source="test")
        assert isinstance(result, list)
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_parse_validates_trait(self, parser):
        """测试解析验证人格维度"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert evidence.trait.value in [
                "achievement_drive",
                "curiosity",
                "risk_preference",
                "security_need",
                "dominance",
                "empathy",
                "independence",
                "responsibility",
                "creativity",
                "social_need",
            ]
    
    @pytest.mark.asyncio
    async def test_parse_validates_score(self, parser):
        """测试解析验证分数"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert 0.0 <= evidence.score <= 1.0
    
    @pytest.mark.asyncio
    async def test_parse_validates_confidence(self, parser):
        """测试解析验证置信度"""
        text = "创业最大的风险是不创业"
        result = await parser.parse(text, source="采访视频")
        for evidence in result:
            assert 0.0 <= evidence.confidence <= 1.0
```

- [ ] **Step 2: 运行测试验证失败**

Run: `pytest tests/material/test_text_parser.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.material.text_parser'"

- [ ] **Step 3: 编写最小实现**

```python
# src/material/__init__.py

"""
素材解析模块
"""

from .text_parser import TextMaterialParser

__all__ = ["TextMaterialParser"]
```

```python
# src/material/text_parser.py

"""
文本素材解析器

负责解析文本素材，提取人格证据
"""

from typing import List
from ..personality.evidence import PersonalityEvidence, PersonalityTrait


class TextMaterialParser:
    """
    文本素材解析器
    
    解析文本内容，提取人格证据
    """
    
    def __init__(self):
        """初始化解析器"""
        # 关键词映射到人格维度（简化版本）
        self.trait_keywords = {
            PersonalityTrait.RISK_PREFERENCE: [
                "风险", "冒险", "挑战", "大胆", "勇敢", "创新", "突破",
            ],
            PersonalityTrait.ACHIEVEMENT_DRIVE: [
                "成功", "目标", "追求", "卓越", "成就", "优秀", "领先",
            ],
            PersonalityTrait.CURIOSITY: [
                "探索", "好奇", "学习", "研究", "发现", "未知", "新奇",
            ],
            PersonalityTrait.EMPATHY: [
                "理解", "共情", "关心", "帮助", "支持", "体贴", "善良",
            ],
            PersonalityTrait.DOMINANCE: [
                "领导", "主导", "控制", "指挥", "权威", "强大", "自信",
            ],
            PersonalityTrait.INDEPENDENCE: [
                "独立", "自主", "自由", "自我", "个人", "独自", "单独",
            ],
            PersonalityTrait.RESPONSIBILITY: [
                "责任", "负责", "担当", "可靠", "信任", "承诺", "认真",
            ],
            PersonalityTrait.CREATIVITY: [
                "创造", "创新", "想象", "独特", "新颖", "艺术", "设计",
            ],
            PersonalityTrait.SOCIAL_NEED: [
                "社交", "朋友", "团队", "合作", "交流", "人脉", "关系",
            ],
            PersonalityTrait.SECURITY_NEED: [
                "安全", "稳定", "保障", "保护", "谨慎", "保守", "可靠",
            ],
        }
    
    async def parse(self, text: str, source: str) -> List[PersonalityEvidence]:
        """
        解析文本，提取人格证据
        
        Args:
            text: 文本内容
            source: 证据来源
            
        Returns:
            List[PersonalityEvidence]: 人格证据列表
        """
        if not text or not text.strip():
            return []
        
        evidence_list = []
        
        # 遍历关键词映射
        for trait, keywords in self.trait_keywords.items():
            # 检查文本是否包含关键词
            matched_keywords = [kw for kw in keywords if kw in text]
            
            if matched_keywords:
                # 计算分数（简化版本：基于匹配关键词数量）
                score = min(len(matched_keywords) / 3.0, 1.0)
                
                # 计算置信度（简化版本）
                confidence = 0.7 + (len(matched_keywords) * 0.05)
                confidence = min(confidence, 1.0)
                
                # 创建证据
                evidence = PersonalityEvidence(
                    trait=trait,
                    score=score,
                    evidence=text,
                    source=source,
                    confidence=confidence,
                    metadata={"matched_keywords": matched_keywords},
                )
                evidence_list.append(evidence)
        
        return evidence_list
```

- [ ] **Step 4: 运行测试验证通过**

Run: `pytest tests/material/test_text_parser.py -v`
Expected: 7 passed

- [ ] **Step 5: 提交代码**

```bash
git add src/material/ tests/material/
git commit -m "feat: implement TextMaterialParser with keyword-based trait extraction"
```

---

## Task 8: 集成测试

**Files:**
- Create: `tests/integration/test_personality_pipeline.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/integration/test_personality_pipeline.py

import pytest
from src.material.text_parser import TextMaterialParser
from src.personality.agent import PersonalityAgent


class TestPersonalityPipeline:
    """人格建模流水线集成测试"""
    
    @pytest.fixture
    def parser(self):
        """创建解析器"""
        return TextMaterialParser()
    
    @pytest.fixture
    def agent(self):
        """创建 agent"""
        return PersonalityAgent()
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, parser, agent):
        """测试完整流水线"""
        # 输入文本
        text = "创业最大的风险是不创业"
        source = "采访视频"
        
        # 解析文本
        evidence_list = await parser.parse(text, source)
        assert len(evidence_list) > 0
        
        # 分析人格
        result = await agent.analyze(evidence_list)
        
        # 验证结果结构
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result
        
        # 验证人格分数
        personality = result["personality"]
        assert 0.0 <= personality["risk_preference"] <= 1.0
        
        # 验证大五人格
        big_five = result["big_five"]
        assert 0.0 <= big_five["openness"] <= 1.0
        assert 0.0 <= big_five["conscientiousness"] <= 1.0
        assert 0.0 <= big_five["extraversion"] <= 1.0
        assert 0.0 <= big_five["agreeableness"] <= 1.0
        assert 0.0 <= big_five["neuroticism"] <= 1.0
        
        # 验证九型人格
        enneagram_top3 = result["enneagram_top3"]
        assert len(enneagram_top3) == 3
        for type_name, score in enneagram_top3.items():
            assert 0.0 <= score <= 1.0
    
    @pytest.mark.asyncio
    async def test_pipeline_with_multiple_texts(self, parser, agent):
        """测试多文本流水线"""
        texts = [
            ("创业最大的风险是不创业", "采访视频"),
            ("我总是追求卓越", "人物自传"),
            ("我喜欢探索未知领域", "博客文章"),
        ]
        
        all_evidence = []
        for text, source in texts:
            evidence = await parser.parse(text, source)
            all_evidence.extend(evidence)
        
        result = await agent.analyze(all_evidence)
        
        assert "personality" in result
        assert "big_five" in result
        assert "enneagram_top3" in result
```

- [ ] **Step 2: 创建集成测试目录**

```bash
mkdir -p tests/integration
touch tests/integration/__init__.py
```

- [ ] **Step 3: 运行集成测试**

Run: `pytest tests/integration/ -v`
Expected: 2 passed

- [ ] **Step 4: 提交代码**

```bash
git add tests/integration/
git commit -m "test: add integration tests for personality pipeline"
```

---

## Task 9: 运行所有测试并生成覆盖率报告

- [ ] **Step 1: 运行所有测试**

Run: `pytest tests/ -v`
Expected: All tests passed

- [ ] **Step 2: 生成覆盖率报告**

Run: `pytest tests/ --cov=src --cov-report=html`
Expected: Coverage report generated in `htmlcov/`

- [ ] **Step 3: 检查覆盖率**

Run: `pytest tests/ --cov=src --cov-report=term-missing`
Expected: Coverage >= 80%

- [ ] **Step 4: 提交最终代码**

```bash
git add .
git commit -m "feat: complete Sprint-1 personality modeling MVP"
```

---

## 执行选项

**计划已完成并保存到 `docs/superpowers/plans/2026-06-09-sprint-1-personality-modeling.md`**

两种执行方式：

**1. Subagent-Driven（推荐）** - 每个任务分发给独立子代理执行，任务间进行审查，快速迭代

**2. Inline Execution** - 在当前会话中执行任务，批量执行并设置检查点

**选择哪种方式？**