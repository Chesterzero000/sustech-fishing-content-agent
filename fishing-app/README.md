# 千鱼千寻 2.0 - 钓鱼核心业务系统

> 钓鱼垂直领域的 AI Agent Skills 系统

---

## 📦 包含内容

### Skills（7个核心钓鱼技能）

1. **fish-identifier** - 鱼类识别
   - AI 视觉识别 3000+ 鱼种
   - 提供钓鱼技巧建议

2. **fishing-coach** - 钓鱼教练
   - RAG + 知识图谱
   - 多轮对话支持
   - 用户记忆管理

3. **spot-manager** - 钓点管理
   - 99个深圳钓点数据库
   - 地理位置搜索
   - 鱼种筛选

4. **weather-advisor** - 天气顾问
   - 实时天气预报
   - 钓鱼适宜度分析
   - 7天预报

5. **catch-tracker** - 渔获记录
   - CRUD 操作
   - 统计分析
   - 历史记录

6. **social-manager** - 社交功能
   - 帖子管理
   - 评论点赞
   - 热门内容

7. **drone-controller** - 无人船控制
   - 遥测数据查询
   - 轨迹回放
   - 状态监控

---

## 🚀 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用

```bash
# 查看版本
fishing-cli --version

# 钓鱼教练
fishing-cli coach ask "鲫鱼怎么钓?"

# 鱼类识别
fishing-cli fish recognize ./my_catch.jpg

# 天气查询
fishing-cli weather current --city "深圳"

# 钓点搜索
fishing-cli spots nearby --lat 22.5 --lon 114.0
```

### MCP 服务器

```bash
# 启动所有 MCP 服务器
cd mcp_servers
./start_all.sh

# 或单独启动
python fishing_coach_server.py
python fish_identifier_server.py
```

### Web API

```bash
# 启动 Web 服务
python web/api.py

# 访问
# http://localhost:8000
# http://localhost:8000/docs (API 文档)
```

---

## 📁 目录结构

```
fishing-app/
├── skills/              # 7个核心 Skills
├── mcp_servers/         # MCP 服务器
├── api/                 # FastAPI 后端（未来）
├── web/                 # Web 前端
├── backend/             # 旧后端代码
├── openclaw/            # OpenClaw 集成
├── cli/                 # CLI 工具
├── shared/              # 共享代码
├── pyproject.toml       # 项目配置
└── README.md            # 本文件
```

---

## 🔧 配置

需要在父目录配置 `.env` 文件：

```env
# Neo4j 图数据库
NEO4J_URI=bolt://192.168.1.79:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# AI 模型
EMBED_MODEL=shibing624/text2vec-base-chinese
HF_ENDPOINT=https://hf-mirror.com

# 微信配置
WX_APPID=your_appid
WX_APPSECRET=your_secret
```

---

## 📚 文档

详见父目录 `docs/` 文件夹。

---

## 🛠️ 技术栈

- Python 3.10+
- FastAPI
- Click (CLI)
- MCP Protocol
- Neo4j (知识图谱)
- ChromaDB (向量数据库)

---

**返回**: [项目主页](../README.md)
