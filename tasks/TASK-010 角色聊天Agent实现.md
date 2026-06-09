# TASK-010 Chat Agent V1

## 任务编号

TASK-010

---

## 任务名称

角色聊天Agent实现

---

## 所属模块

对话系统

---

## 优先级

P0

---

## 目标

根据人格画像与知识库进行角色扮演聊天。

实现：

```text
用户提问
↓
加载人格
↓
加载知识
↓
生成角色回复
```

---

## 参考文档

03_角色知识库规范.md

08_Agent设计规范.md

09_总体架构设计.md

---

## 输入

```json
{
  "character_id": "elon",
  "message": "你为什么喜欢创业？"
}
```

---

## 输出

```json
{
  "reply": "..."
}
```

---

## 实现内容

创建：

```text
src/chat/
├── chat_agent.py
├── prompt_builder.py
├── character_loader.py
└── chat_service.py
```

---

### Step1

加载人格画像

来源：

```python
PersonalityProfile
```

---

### Step2

加载知识库

来源：

```python
CharacterKnowledge
```

---

### Step3

构建角色Prompt

Prompt组成：

```text
人格
+
知识
+
价值观
+
用户问题
```

---

### Step4

调用LLM生成回复

---

### Step5

返回角色回复

---

## MVP限制

暂不实现：

* 长期记忆
* 行为预测
* 一致性验证
* 人格成长
* 语音克隆

仅实现：

```text
人格 + 知识 + 聊天
```

---

## 验收标准

角色能够聊天

角色回复符合知识库

角色回复符合人格设定

---

## 测试要求

普通聊天

角色知识问答

人格一致性测试

异常输入测试

---

## 完成定义（DoD）

接口可调用

测试覆盖率 ≥ 80%

角色回复符合设定
