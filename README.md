# 🧠 失忆宝宝（Amnesia Baby）

通过人物素材重建数字人格，并与其持续对话。

---

## ✨ 核心功能

| 模块 | 说明 |
|------|------|
| 🎭 人格建模 | 大五人格 + 九型人格分析 |
| 📚 知识库 | 素材上传 → 知识提取 → 结构化存储 |
| 🔍 向量检索 | 语义搜索，Hash 嵌入 + 余弦相似度 |
| 🧠 记忆系统 | 短期/长期记忆 + 自动巩固 |
| 💬 角色对话 | 多 LLM 支持，角色扮演对话 |
| 🌐 Web UI | 聊天 / 知识库 / 画像 可视化界面 |

---

## 🛠 技术栈

- **后端**: FastAPI + Pydantic
- **LLM**: 小米 MIMO / OpenAI / DeepSeek / 通义千问
- **向量**: NumPy (Hash 嵌入)
- **前端**: Jinja2 + Vanilla JS + CSS Variables
- **测试**: pytest + pytest-cov (274 tests, 92% coverage)

---

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/zhangtangzz/amnesia-baby.git
cd amnesia-baby

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 5. 启动服务
uvicorn src.api.app:app --reload --port 8000

# 6. 访问
# 首页:   http://localhost:8000
# 聊天:   http://localhost:8000/chat
# 知识库: http://localhost:8000/knowledge
# 画像:   http://localhost:8000/profile
# API文档: http://localhost:8000/docs
```

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat/send` | 发送聊天消息 |
| POST | `/api/personality/analyze` | 人格分析 |
| POST | `/api/knowledge/process` | 处理知识 |
| POST | `/api/memory/add` | 添加记忆 |
| POST | `/api/vector/search` | 向量搜索 |
| GET  | `/health` | 健康检查 |

---

## 🧪 运行测试

```bash
pytest tests/ -v --cov=src
```

---

## 📁 项目结构

```
src/
├── api/          # FastAPI 应用 + 路由
├── chat/         # 对话引擎
├── knowledge/    # 知识库
├── llm/          # LLM 多提供商集成
├── material/     # 素材解析
├── memory/       # 记忆系统
├── personality/  # 人格建模
├── vector/       # 向量检索
└── web/          # 前端页面
```

---

## 📜 开发日志

详见 [CHANGELOG.md](CHANGELOG.md)