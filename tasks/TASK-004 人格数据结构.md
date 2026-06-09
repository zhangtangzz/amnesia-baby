# TASK-004 人格数据结构

## 任务编号

TASK-004

---

## 任务名称

人格向量模型实现

---

## 所属模块

人格系统

---

## 优先级

P0

---

## 目标

实现系统核心人格模型。

---

## 参考文档

02_人格建模规范.md

---

## 实现内容

创建：

PersonalityProfile

---

字段：

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

---

数据范围：

0.0 ~ 1.0

---

## 输出

personality.py

---

## 验收标准

支持初始化

支持序列化

支持反序列化

支持范围校验

---

## 测试要求

字段测试

边界值测试

异常测试

---

## 完成定义（DoD）

测试覆盖率 ≥ 80%
