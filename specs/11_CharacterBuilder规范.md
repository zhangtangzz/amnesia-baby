# Character Builder规范

## 文档编号

SPEC-011

---

## 文档名称

Character Builder规范

---

## 目标

统一构建角色档案。

避免ChatAgent直接依赖多个Agent。

---

# 一、系统定位

Character Builder负责：

素材

↓

人格分析

↓

知识提取

↓

价值观提取

↓

角色档案

---

# 二、输入

Raw Material

例如：

文章

访谈

文本

---

# 三、流程

MaterialAgent

↓

PersonalityAgent

↓

KnowledgeAgent

↓

CharacterBuilder

---

# 四、输出

CharacterProfile

---

结构：

{
"character_id":"",
"personality":{},
"big_five":{},
"enneagram":{},
"knowledge":[],
"values":[],
"summary":""
}

---

# 五、职责

负责：

角色构建

角色更新

角色保存

---

不负责：

聊天

语音

行为预测

---

# 六、存储

CharacterProfile

作为系统统一角色对象。

所有后续Agent必须从：

CharacterProfile

读取角色信息。
