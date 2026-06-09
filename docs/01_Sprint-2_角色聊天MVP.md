# Sprint-2 角色聊天 MVP

## Sprint编号

Sprint-2

---

## Sprint名称

角色聊天 MVP

---

## Sprint目标

实现角色聊天最小可运行版本（MVP）。

完成：

用户输入消息

↓

系统加载人格画像

↓

系统加载知识库

↓

构建角色Prompt

↓

调用LLM生成回复

↓

输出角色回复

---

## Sprint周期

预计：

7天

---

## Sprint范围

包含：

角色聊天

人格加载

知识加载

Prompt构建

LLM调用

---

不包含：

长期记忆

行为预测

一致性验证

人格成长

语音克隆

多轮对话记忆

---

# 一、业务流程

用户发送消息

↓

Chat Agent

↓

Character Loader (加载人格)

↓

Knowledge Loader (加载知识)

↓

Prompt Builder (构建Prompt)

↓

LLM Service (调用LLM)

↓

返回角色回复

---

# 二、Sprint任务

## TASK-010 角色聊天Agent实现

目标：

实现角色聊天Agent

状态：

TODO

优先级：

P0

---

## TASK-011 角色加载器实现

目标：

实现CharacterLoader

状态：

TODO

优先级：

P0

---

## TASK-012 知识加载器实现

目标：

实现KnowledgeLoader

状态：

TODO

优先级：

P0

---

## TASK-013 Prompt构建器实现

目标：

实现PromptBuilder

状态：

TODO

优先级：

P0

---

## TASK-014 LLM服务实现

目标：

实现LLMService

状态：

TODO

优先级：

P0

---

## TASK-015 聊天服务实现

目标：

实现ChatService

状态：

TODO

优先级：

P0

---

# 三、任务执行顺序

第一阶段

TASK-011

↓

TASK-012

↓

TASK-013

---

第二阶段

TASK-014

↓

TASK-015

---

第三阶段

TASK-010

↓

联调测试

---

# 四、目录结构

src/

chat/

├── __init__.py

├── chat_agent.py

├── character_loader.py

├── knowledge_loader.py

├── prompt_builder.py

├── llm_service.py

└── chat_service.py

---

tests/

chat/

├── __init__.py

├── test_chat_agent.py

├── test_character_loader.py

├── test_knowledge_loader.py

├── test_prompt_builder.py

├── test_llm_service.py

└── test_chat_service.py

---

# 五、核心交付物

## 交付物1

CharacterLoader

---

## 交付物2

KnowledgeLoader

---

## 交付物3

PromptBuilder

---

## 交付物4

LLMService

---

## 交付物5

ChatService

---

## 交付物6

ChatAgent

---

# 六、验收标准

输入：

```json
{
  "character_id": "elon",
  "message": "你为什么喜欢创业？"
}
```

---

系统输出：

```json
{
  "reply": "创业让我能够实现那些看似不可能的想法..."
}
```

---

# 七、测试要求

必须完成：

单元测试

集成测试

人格一致性测试

知识问答测试

异常输入测试

---

覆盖率：

>=80%

---

# 八、完成定义（DoD）

所有Task完成

所有测试通过

覆盖率达到80%

角色聊天成功

文档同步更新

Code Review通过

---

# 九、Sprint成功标准

能够发送消息给角色

↓

角色根据人格和知识回复

↓

回复符合角色设定

即视为Sprint-2完成