# TASK-009 Text Material Parser

## 任务编号

TASK-009

---

## 任务名称

文本素材解析器实现

---

## 所属模块

素材解析系统（Material System）

---

## 优先级

P0

---

## 目标

实现 V1 版本文本素材解析能力。

从：

* 人物访谈
* 自传
* 新闻报道
* 博客文章
* 网页资料

中提取：

* 人格证据（Personality Evidence）
* 知识证据（Knowledge Evidence）
* 行为证据（Behavior Evidence）
* 价值观证据（Value Evidence）

供后续：

```text
Personality Agent
Knowledge Agent
Behavior Agent
```

使用。

---

## 参考文档

01_素材解析规范.md

02_人格建模规范.md

03_角色知识库规范.md

08_Agent设计规范.md

09_总体架构设计.md

---

## 输入

```json
{
  "text":"创业最大的风险是不创业。"
}
```

---

## 输出

```json
{
  "personality_evidence": [],
  "knowledge_evidence": [],
  "behavior_evidence": [],
  "value_evidence": []
}
```

---

## 创建目录

```text
src/material/

├── text_parser.py
├── material_agent.py

├── prompts/
│   ├── extract_personality.txt
│   ├── extract_knowledge.txt
│   ├── extract_behavior.txt
│   └── extract_values.txt

├── models/
│   ├── knowledge_evidence.py
│   ├── behavior_evidence.py
│   └── value_evidence.py
```

---

# Step 1 文本预处理

## 目标

清洗原始文本。

---

## 实现内容

支持：

* 去除HTML标签
* 去除特殊字符
* 去除重复空格
* 文本切分

---

## 输入

```text
原始文章
```

---

## 输出

```text
标准文本块
```

---

# Step 2 人格证据提取

## 目标

提取人格相关内容。

---

## 示例

原文：

```text
我喜欢挑战不可能。
```

输出：

```json
{
  "trait":"risk_preference",
  "score":0.91,
  "evidence":"喜欢挑战不可能"
}
```

---

## 输出对象

```python
PersonalityEvidence
```

---

# Step 3 知识证据提取

## 目标

提取客观事实。

---

## 示例

原文：

```text
2015年创办某公司
```

输出：

```json
{
  "fact":"创办公司",
  "year":2015
}
```

---

## 输出对象

```python
KnowledgeEvidence
```

---

# Step 4 行为证据提取

## 目标

提取行为模式。

---

## 示例

原文：

```text
连续三次创业
```

输出：

```json
{
  "behavior":"continuous_entrepreneurship"
}
```

---

## 输出对象

```python
BehaviorEvidence
```

---

# Step 5 价值观提取

## 目标

提取角色价值观。

---

## 示例

原文：

```text
家庭比事业更重要
```

输出：

```json
{
  "value":"family",
  "weight":0.92
}
```

---

## 输出对象

```python
ValueEvidence
```

---

# Step 6 Material Agent封装

## 创建

```python
MaterialAgent
```

---

## 方法

```python
parse_text(text)
```

---

## 返回

```json
{
  "personality_evidence": [],
  "knowledge_evidence": [],
  "behavior_evidence": [],
  "value_evidence": []
}
```

---

# MVP限制

V1仅支持：

```text
文本解析
```

暂不支持：

```text
视频解析

音频解析

OCR解析

网页爬取
```

后续任务实现。

---

# 验收标准

支持中文文本

支持长文本

支持多段文本

返回统一结构

---

# 测试要求

## Case1

短文本

```text
我喜欢挑战不可能
```

应提取：

```text
risk_preference
```

---

## Case2

知识文本

```text
2015年创办公司
```

应提取：

```text
KnowledgeEvidence
```

---

## Case3

价值观文本

```text
家庭比事业更重要
```

应提取：

```text
family
```

---

## Case4

空文本

```text
""
```

返回空结果

---

# 完成定义（DoD）

文本解析成功

结构输出正确

测试覆盖率 ≥ 80%

MaterialAgent可独立调用

通过集成测试
