# Agent开发规范

## 文档编号

SPEC-015

---

## 文档名称

Agent开发规范

---

## 目标

规范AI Agent参与项目开发行为。

保证：

- 代码质量稳定
- 开发流程统一
- 避免架构污染
- 避免AI自由发挥

---

# 一、开发原则

Agent必须遵循：

任务驱动开发

禁止：

需求猜测开发

---

Agent只能执行：

已存在Task

例如：

TASK-001

TASK-004

TASK-008

---

禁止：

自行创建功能

自行扩展需求

自行修改架构

---

# 二、开发流程

必须按照：

阅读规范

↓

阅读Task

↓

输出设计

↓

等待确认

↓

实现代码

↓

编写测试

↓

运行测试

↓

提交结果

---

禁止：

直接写代码

---

# 三、文档优先级

冲突时：

SPEC

>

TASK

>

README

>

Prompt

---

Agent必须优先遵守：

specs/

中的规范

---

# 四、目录约束

必须遵守：

SPEC-013

项目目录规范

---

禁止：

创建未定义目录

---

禁止：

跨模块写代码

---

示例：

chat/

禁止直接访问：

material/

内部实现

---

# 五、单一职责原则

一个Agent只负责一个模块。

---

Material Agent

负责：

素材解析

---

Personality Agent

负责：

人格分析

---

Knowledge Agent

负责：

知识管理

---

Chat Agent

负责：

角色对话

---

禁止职责混合

---

# 六、代码规范

必须：

类型注解

Docstring

异常处理

日志记录

---

禁止：

硬编码

Magic Number

全局变量

---

示例：

错误

score = 0.83

---

正确

DEFAULT_SCORE = 0.83

---

# 七、测试规范

所有代码必须生成测试。

---

要求：

pytest

覆盖率 >= 80%

---

禁止：

无测试提交

---

# 八、接口规范

必须遵守：

SPEC-012 API规范

---

禁止：

私自新增API

---

禁止：

修改响应格式

---

统一格式：

{
  "success": true,
  "data": {}
}

---

# 九、人格系统规范

必须遵守：

SPEC-010 人格计算规范

---

禁止：

修改大五映射公式

---

禁止：

修改人格聚合公式

---

禁止：

修改九型概率逻辑

---

# 十、Prompt规范

Prompt必须放置：

src/**/prompts/

---

禁止：

Prompt写入Python代码

---

错误：

prompt = """
你是...
"""

---

正确：

load_prompt("chat_prompt.txt")

---

# 十一、日志规范

所有Agent必须记录：

开始执行

结束执行

异常信息

耗时

---

格式：

[AgentName]

Start

End

Duration

Error

---

# 十二、异常处理

所有Agent必须捕获：

业务异常

模型异常

解析异常

网络异常

---

禁止：

裸except

---

错误：

except:
    pass

---

正确：

except ModelError as e:
    logger.error(e)

---

# 十三、数据库规范

Agent禁止直接访问数据库

---

Agent

↓

Service

↓

Repository

↓

Database

---

必须分层

---

# 十四、LLM调用规范

统一使用：

LLMClient

---

禁止：

各模块直接调用模型

---

错误：

client.chat()

---

正确：

llm_service.generate()

---

# 十五、配置规范

所有配置：

.env

config.py

---

禁止：

API Key硬编码

---

# 十六、Git规范

提交格式：

feat:

fix:

refactor:

test:

docs:

---

示例：

feat(personality):
add personality aggregation

---

# 十七、评审规范

Agent完成任务后必须输出：

实现内容

影响范围

测试结果

风险分析

---

模板：

## Summary

## Files Changed

## Tests

## Risks

---

# 十八、禁止事项

禁止修改规范

禁止跳过测试

禁止跳过设计

禁止跨模块开发

禁止自行增加需求

禁止删除历史功能

---

# 十九、完成定义（DoD）

代码完成

测试通过

规范符合

文档更新

CI通过

Review通过