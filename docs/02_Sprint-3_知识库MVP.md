# Sprint-3 知识库 MVP

## Sprint编号

Sprint-3

---

## Sprint名称

知识库 MVP

---

## Sprint目标

实现角色知识库最小可运行版本（MVP）。

完成：

用户上传素材

↓

系统解析素材

↓

提取知识

↓

结构化存储

↓

知识查询

---

## Sprint周期

预计：

7天

---

## Sprint范围

包含：

知识库数据结构

知识提取

知识存储

知识查询

知识更新

---

不包含：

知识图谱

向量检索

知识推理

知识冲突检测

---

# 一、业务流程

用户上传素材

↓

Material Agent (素材解析)

↓

Knowledge Extractor (知识抽取)

↓

实体识别

人物识别

事件识别

关系识别

观点识别

↓

结构化存储

↓

Knowledge Base

---

# 二、Sprint任务

## TASK-016 知识库数据结构

目标：

实现知识库数据模型

状态：

TODO

优先级：

P0

---

## TASK-017 知识提取器实现

目标：

实现KnowledgeExtractor

状态：

TODO

优先级：

P0

---

## TASK-018 知识存储器实现

目标：

实现KnowledgeStore

状态：

TODO

优先级：

P0

---

## TASK-019 知识查询器实现

目标：

实现KnowledgeQuery

状态：

TODO

优先级：

P0

---

## TASK-020 知识更新器实现

目标：

实现KnowledgeUpdater

状态：

TODO

优先级：

P0

---

## TASK-021 知识服务实现

目标：

实现KnowledgeService

状态：

TODO

优先级：

P0

---

# 三、任务执行顺序

第一阶段

TASK-016

↓

TASK-017

---

第二阶段

TASK-018

↓

TASK-019

↓

TASK-020

---

第三阶段

TASK-021

↓

联调测试

---

# 四、目录结构

src/

knowledge/

├── __init__.py

├── models.py

├── extractor.py

├── store.py

├── query.py

├── updater.py

└── service.py

---

tests/

knowledge/

├── __init__.py

├── test_models.py

├── test_extractor.py

├── test_store.py

├── test_query.py

├── test_updater.py

└── test_service.py

---

# 五、核心交付物

## 交付物1

KnowledgeProfile (基础信息)

---

## 交付物2

Relationship (人物关系)

---

## 交付物3

Event (重要事件)

---

## 交付物4

Belief (观点体系)

---

## 交付物5

Fact (事实库)

---

## 交付物6

Timeline (人生时间轴)

---

## 交付物7

Evidence (证据库)

---

## 交付物8

KnowledgeExtractor (知识提取器)

---

## 交付物9

KnowledgeStore (知识存储器)

---

## 交付物10

KnowledgeQuery (知识查询器)

---

## 交付物11

KnowledgeUpdater (知识更新器)

---

## 交付物12

KnowledgeService (知识服务)

---

# 六、验收标准

输入：

```json
{
  "text": "张三毕业于清华大学，创立了某科技公司",
  "source": "采访视频"
}
```

---

系统输出：

```json
{
  "profile": {
    "name": "张三",
    "education": "清华大学",
    "occupation": "创业者"
  },
  "facts": [
    {
      "fact": "毕业于清华大学",
      "category": "education",
      "confidence": 0.92
    },
    {
      "fact": "创立某科技公司",
      "category": "career",
      "confidence": 0.94
    }
  ]
}
```

---

# 七、测试要求

必须完成：

单元测试

集成测试

知识提取测试

知识存储测试

知识查询测试

---

覆盖率：

>=80%

---

# 八、完成定义（DoD）

所有Task完成

所有测试通过

覆盖率达到80%

知识库功能正常

文档同步更新

Code Review通过

---

# 九、Sprint成功标准

能够上传素材

↓

系统提取知识

↓

知识结构化存储

↓

支持知识查询

即视为Sprint-3完成