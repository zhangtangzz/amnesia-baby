# TASK-007 Personality Evidence Model

## 任务编号

TASK-007

---

## 任务名称

人格证据数据结构实现

---

## 所属模块

人格系统

---

## 优先级

P0

---

## 目标

定义系统统一的人格证据模型。

人格证据（Personality Evidence）是素材解析层与人格建模层之间的数据桥梁。

负责承载：

* 人格线索
* 人格评分
* 原始证据
* 置信度
* 来源信息

供 Personality Agent 使用。

---

## 参考文档

01_素材解析规范.md

02_人格建模规范.md

08_Agent设计规范.md

---

## 输入来源

Material Agent

---

## 输出目标

Personality Agent

---

## 实现内容

创建：

```text
src/personality/
└── evidence.py
```

---

实现数据模型：

```python
PersonalityEvidence
```

---

## 字段定义

### trait

人格维度

类型：

```python
str
```

允许值：

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

### score

证据强度

类型：

```python
float
```

范围：

```text
0.0 ~ 1.0
```

---

### evidence

原始证据

类型：

```python
str
```

示例：

```text
我喜欢挑战不可能
```

---

### source

证据来源

类型：

```python
str
```

示例：

```text
采访视频
人物自传
博客文章
```

---

### confidence

置信度

类型：

```python
float
```

范围：

```text
0.0 ~ 1.0
```

---

### metadata

扩展信息

类型：

```python
dict
```

示例：

```json
{
  "timestamp":"12:33",
  "speaker":"角色本人"
}
```

---

## 示例

```json
{
  "trait":"risk_preference",
  "score":0.91,
  "evidence":"创业最大的风险是不创业",
  "source":"采访视频",
  "confidence":0.88
}
```

---

## 验收标准

支持序列化

支持反序列化

支持范围校验

支持JSON导出

---

## 测试要求

正常输入

空值测试

非法trait测试

score边界测试

confidence边界测试

---

## 完成定义（DoD）

测试覆盖率 ≥ 80%

模型可被Material Agent调用

模型可被Personality Agent调用
