# Agent设计规范（V1）

## 文档信息

| 项目   | 内容        |
| ---- | --------- |
| 文档名称 | Agent设计规范 |
| 文档版本 | V1.0      |
| 所属项目 | 失忆宝宝      |
| 更新时间 | 2026-06   |

---

# 一、设计目标

定义《失忆宝宝》系统中的Agent职责划分。

原则：

```text
一个Agent只负责一件事
```

避免：

```text
超级Agent
```

承担所有工作。

---

# 二、总体架构

```text
User Input
      ↓

Orchestrator Agent
（总调度）

      ↓

Material Agent
Personality Agent
Knowledge Agent
Memory Agent
Behavior Agent
Consistency Agent
Growth Agent
Voice Agent

      ↓

Response
```

---

# 三、Orchestrator Agent

## 职责

系统总调度中心。

负责：

* 接收用户请求
* 分配任务
* 调用Agent
* 汇总结果

---

## 输入

```json
{
  "user_input": ""
}
```

---

## 输出

```json
{
  "next_agents": []
}
```

---

## 示例

用户：

```text
分析马斯克人格
```

调度：

```text
Material Agent
↓
Personality Agent
↓
Knowledge Agent
```

---

# 四、Material Agent

## 职责

素材解析。

负责：

* 视频解析
* 音频解析
* 文本解析
* 网页解析

---

## 输入

```json
{
  "material": ""
}
```

---

## 输出

```json
{
  "personality_evidence": [],
  "knowledge_evidence": [],
  "value_evidence": []
}
```

---

# 五、Personality Agent

## 职责

人格建模。

---

## 输入

```json
{
  "personality_evidence": []
}
```

---

## 输出

```json
{
  "traits": {},
  "big_five": {},
  "enneagram": {}
}
```

---

## 负责

### 十维人格特征

```text
achievement_drive
curiosity
risk_preference
security_need
dominance
empathy
independence
responsibility
creativity
social_need
```

---

### 大五人格

```text
O
C
E
A
N
```

---

### 九型人格

```text
Type1 ~ Type9
```

---

# 六、Knowledge Agent

## 职责

知识库构建与检索。

---

## 输入

```json
{
  "knowledge_evidence": []
}
```

---

## 输出

```json
{
  "profile": {},
  "events": [],
  "relationships": [],
  "beliefs": []
}
```

---

## 功能

### 实体抽取

```text
人物
地点
组织
时间
```

---

### 事件抽取

```text
创业
获奖
工作经历
```

---

### 关系抽取

```text
朋友
家人
同事
导师
```

---

# 七、Memory Agent

## 职责

记忆管理。

---

## 管理

### 短期记忆

```text
当前对话
```

---

### 长期记忆

```text
用户历史
```

---

### 共享记忆

```text
角色与用户共同经历
```

---

### 情绪记忆

```text
情绪事件
```

---

## 输出

```json
{
  "related_memories": []
}
```

---

# 八、Behavior Agent

## 职责

行为预测。

---

## 输入

```json
{
  "personality": {},
  "values": {},
  "knowledge": {},
  "memory": {},
  "situation": {}
}
```

---

## 输出

```json
{
  "decision": {},
  "reasoning": {}
}
```

---

## 核心公式

```text
Behavior =
f(
Personality,
Values,
Knowledge,
Memory,
Situation
)
```

---

# 九、Consistency Agent

## 职责

一致性验证。

---

## 检查内容

### 人格一致性

```text
符合人格？
```

---

### 知识一致性

```text
符合知识库？
```

---

### 记忆一致性

```text
符合历史？
```

---

### 行为一致性

```text
符合过去决策？
```

---

## 输出

```json
{
  "score": 0.91,
  "conflicts": []
}
```

---

# 十、Growth Agent

## 职责

人格成长。

---

## 输入

```json
{
  "new_evidence": []
}
```

---

## 功能

### 检测变化

```text
变了吗？
```

---

### 分析变化

```text
为什么变？
```

---

### 更新时间轴

```text
人格成长记录
```

---

## 输出

```json
{
  "updated_personality": {},
  "growth_history": []
}
```

---

# 十一、Voice Agent

## 职责

语音能力。

---

## 功能

### 语音克隆

```text
声音复制
```

---

### 情绪语音

```text
开心
愤怒
悲伤
```

---

### 风格模仿

```text
语速
停顿
口头禅
```

---

## 输出

```json
{
  "audio": ""
}
```

---

# 十二、Agent通信协议

统一采用：

```json
{
  "task_id": "",
  "agent_name": "",
  "input": {},
  "output": {},
  "confidence": 0.0,
  "timestamp": ""
}
```

---

# 十三、Agent执行流程

## 场景1

分析人物

```text
Material Agent
      ↓

Personality Agent

      ↓

Knowledge Agent

      ↓

Growth Agent
```

---

## 场景2

角色聊天

```text
Memory Agent
      ↓

Knowledge Agent
      ↓

Behavior Agent
      ↓

Consistency Agent
      ↓

Voice Agent
```

---

## 场景3

人格更新

```text
Material Agent
      ↓

Growth Agent
      ↓

Personality Agent
      ↓

Knowledge Agent
```

---

# 十四、未来扩展Agent

## Emotion Agent

负责：

```text
情绪状态管理
```

---

## Relationship Agent

负责：

```text
关系成长
```

---

## Planning Agent

负责：

```text
长期目标规划
```

---

## Reflection Agent

负责：

```text
自我反思
```

---

# 十五、最终Agent架构

```text
                User
                  ↓

        Orchestrator Agent
                  ↓

 ┌─────────────────────────┐
 │                         │
 ▼                         ▼

Material Agent       Memory Agent
      │                    │
      ▼                    ▼

Personality Agent   Knowledge Agent
      │                    │
      └──────┬─────────────┘
             ▼

      Behavior Agent
             ▼

    Consistency Agent
             ▼

        Voice Agent
             ▼

         Response

             ▼

       Growth Agent
```

---

# V1核心结论

每个Agent只负责一个领域：

```text
Material Agent
负责发现证据

Personality Agent
负责人格建模

Knowledge Agent
负责知识管理

Memory Agent
负责记忆管理

Behavior Agent
负责行为预测

Consistency Agent
负责质量控制

Growth Agent
负责人格成长

Voice Agent
负责语音能力
```

最终形成可扩展、多Agent、可持续成长的数字人格系统。
