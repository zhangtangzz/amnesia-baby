# Sprint-7 真实 LLM 集成 MVP

## Sprint编号
Sprint-7

## Sprint名称
真实 LLM 集成 MVP

## Sprint目标
替换 mock LLM，接入真实 LLM 服务，支持多提供商、流式响应、重试降级。

## Sprint周期
预计：7天

## Sprint范围
包含：
- LLM 提供商抽象接口
- OpenAI 提供商
- 国产 LLM 提供商（DeepSeek / 通义千问）
- 提供商工厂与配置切换
- 重试与降级机制
- 流式响应（SSE）
- Token 统计
- API 更新

不包含：
- 本地模型部署
- 模型微调
- 多轮对话上下文窗口管理

---

# 一、架构设计

```
ChatService
    ↓
LLMRouter (路由器)
    ↓
LLMProvider (抽象接口)
    ├── OpenAIProvider
    ├── DeepSeekProvider
    └── QwenProvider
```

---

# 二、Sprint任务

## TASK-022 LLM提供商抽象接口
目标：定义 LLMProvider 基类，规范 generate() / stream() 接口
状态：TODO | 优先级：P0

## TASK-023 OpenAI 提供商实现
目标：基于 openai SDK 实现 OpenAIProvider
状态：TODO | 优先级：P0

## TASK-024 国产LLM提供商实现
目标：实现 DeepSeekProvider 和 QwenProvider（兼容 OpenAI 接口）
状态：TODO | 优先级：P0

## TASK-025 LLM路由器（工厂模式）
目标：根据配置自动选择 LLM 提供商，支持运行时切换
状态：TODO | 优先级：P0

## TASK-026 重试与降级机制
目标：调用失败自动重试，主提供商不可用时降级到备用提供商
状态：TODO | 优先级：P1

## TASK-027 流式响应支持
目标：实现 SSE 流式输出，前端实时展示回复
状态：TODO | 优先级：P1

## TASK-028 Token统计
目标：统计每次调用的 token 用量，记录日志
状态：TODO | 优先级：P2

## TASK-029 API更新与集成测试
目标：更新 Chat API 支持 provider 参数选择，端到端测试
状态：TODO | 优先级：P0

---

# 三、任务执行顺序

第一阶段：TASK-022 → TASK-023 → TASK-024
第二阶段：TASK-025 → TASK-026
第三阶段：TASK-027 → TASK-028
第四阶段：TASK-029 → 联调测试

---

# 四、目录结构

src/llm/
├── __init__.py
├── base.py            # LLMProvider 抽象基类
├── openai_provider.py
├── deepseek_provider.py
├── qwen_provider.py
├── router.py           # LLMRouter 工厂
├── retry.py            # 重试降级
└── models.py           # TokenUsage 等数据模型

---

# 五、验收标准

输入: {"character_id": "elon", "message": "你为什么喜欢创业？", "provider": "openai"}
输出: {"reply": "创业让我能够实现...", "provider": "openai", "model": "gpt-3.5-turbo", "usage": {"prompt_tokens": 320, "completion_tokens": 85, "total_tokens": 405}}

---

# 六、测试要求
覆盖率：>=80%
