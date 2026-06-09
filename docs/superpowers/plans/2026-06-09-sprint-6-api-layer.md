# Sprint-6 API接口层 MVP 实施计划

**Goal:** 实现RESTful API接口，让系统可以被外部调用。

**Tech Stack:** Python 3.14+, FastAPI, Pydantic, pytest

---

## 文件结构

src/api/ - API接口层
tests/api/ - API测试

---

## Task 1: API基础框架
- Create: src/api/app.py
- Create: src/api/routes/__init__.py
- Create: src/api/models/__init__.py
- Create: src/api/models/requests.py
- Create: src/api/models/responses.py
- Create: tests/api/test_app.py

## Task 2: 人格API
- Create: src/api/routes/personality.py
- Create: tests/api/test_personality.py

## Task 3: 聊天API
- Create: src/api/routes/chat.py
- Create: tests/api/test_chat.py

## Task 4: 知识库API
- Create: src/api/routes/knowledge.py
- Create: tests/api/test_knowledge.py

## Task 5: 记忆API
- Create: src/api/routes/memory.py
- Create: tests/api/test_memory.py

## Task 6: 向量检索API
- Create: src/api/routes/vector.py
- Create: tests/api/test_vector.py

## Task 7: 集成测试
- Create: tests/integration/test_api_pipeline.py

## Task 8: 运行所有测试并生成覆盖率报告
