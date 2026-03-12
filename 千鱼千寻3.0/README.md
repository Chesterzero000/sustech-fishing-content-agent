# 千鱼千寻 2.0 - OpenClaw 技能集成

## 项目简介

千鱼千寻 2.0 是对原有钓鱼小程序的重大升级，将所有功能封装为 OpenClaw 技能，提供 CLI 和 MCP 接口。

## 技术架构

- **Python 3.10+**
- **CLI框架**: Click
- **MCP协议**: Model Context Protocol (stdio传输)
- **技能系统**: OpenClaw兼容的技能定义

## 目录结构

```
千鱼千寻2.0/
├── shared/                    # 共享基础设施
│   ├── skill_base.py         # 技能基类
│   ├── config_manager.py     # 配置管理
│   ├── response_formatter.py # 响应格式化
│   └── __init__.py
│
├── cli/                       # CLI命令行界面
│   ├── main.py               # CLI主程序
│   ├── utils.py              # CLI工具
│   └── __init__.py
│
├── mcp_servers/               # MCP服务器
│   ├── base.py               # MCP基础服务器
│   ├── fishing_coach_server.py
│   ├── fish_identifier_server.py
│   ├── weather_advisor_server.py
│   ├── spot_manager_server.py
│   └── __init__.py
│
├── skills/                    # OpenClaw技能
│   ├── fishing-coach/        # 钓鱼教练
│   │   ├── SKILL.md
│   │   ├── service.py
│   │   ├── cli.py
│   │   └── __init__.py
│   ├── fish-identifier/      # 鱼类识别
│   ├── weather-advisor/      # 天气顾问
│   └── spot-manager/         # 钓点管理
│
├── setup.py                   # 安装配置
├── pyproject.toml            # 项目配置
└── README.md                 # 本文件
```

## 已实现的技能

### 1. 🎓 fishing-coach (钓鱼教练)
AI驱动的钓鱼问答，集成RAG和知识图谱。

**CLI命令**:
```bash
fishing-cli coach ask "鲫鱼怎么钓?"
fishing-cli coach chat --user-id user123 --question "今天适合钓鱼吗?"
fishing-cli coach memory --user-id user123
```

**MCP工具**:
- `coach_ask` - 提问AI教练
- `coach_chat` - 多轮对话
- `get_user_memory` - 获取用户记忆

---

### 2. 🐟 fish-identifier (鱼类识别)
基于AI视觉的鱼类物种识别，支持3000+鱼种。

**CLI命令**:
```bash
fishing-cli fish recognize ./my_catch.jpg
fishing-cli fish tips "鲫鱼"
```

**MCP工具**:
- `identify_fish` - 从图片识别鱼种
- `identify_fish_base64` - 从base64数据识别
- `get_fish_tips` - 获取钓鱼技巧

---

### 3. 🌤️ weather-advisor (天气顾问)
实时天气预报和钓鱼适宜度分析。

**CLI命令**:
```bash
fishing-cli weather current --city "深圳"
fishing-cli weather forecast --city "深圳" --days 7
fishing-cli weather fishing-index --lat 22.5 --lon 114.0
```

**MCP工具**:
- `get_weather` - 获取当前天气
- `get_forecast` - 获取天气预报
- `calculate_fishing_index` - 计算钓鱼指数

---

### 4. 📍 spot-manager (钓点管理)
钓点搜索和管理，包含99个深圳钓点数据库。

**CLI命令**:
```bash
fishing-cli spots nearby --lat 22.5 --lon 114.0 --radius 10
fishing-cli spots search --fish "鲫鱼"
fishing-cli spots details --id 123
fishing-cli spots list --limit 20
```

**MCP工具**:
- `get_nearby_spots` - 查找附近钓点
- `search_spots` - 按鱼种搜索
- `get_spot_details` - 获取钓点详情
- `list_spots` - 列出所有钓点

---

### 5. 📊 catch-tracker (渔获记录追踪)
渔获记录的 CRUD、统计和分析。

**CLI命令**:
```bash
fishing-cli catch log --user-id user123 --species "鲫鱼" --weight 0.5
fishing-cli catch list --user-id user123 --limit 20
fishing-cli catch stats --user-id user123
fishing-cli catch delete --catch-id 123 --user-id user123
```

**MCP工具**:
- `log_catch` - 记录渔获
- `get_catches` - 获取渔获历史
- `get_statistics` - 获取统计数据
- `delete_catch` - 删除记录

---

### 6. 💬 social-manager (社交功能管理)
钓友圈帖子、评论和点赞管理。

**CLI命令**:
```bash
fishing-cli social posts --limit 20
fishing-cli social trending --period week
fishing-cli social post --content "今天钓了5条鲫鱼"
fishing-cli social like --post-id 123
fishing-cli social comment --post-id 123 --content "厉害！"
```

**MCP工具**:
- `list_posts` - 列出帖子
- `get_trending_posts` - 获取热门帖子
- `create_post` - 发布帖子
- `like_post` - 点赞
- `comment_post` - 评论

---

### 7. 🚁 drone-controller (无人船遥测控制)
无人船遥测数据查询和轨迹回放。

**CLI命令**:
```bash
fishing-cli drone status --device-id drone123
fishing-cli drone history --device-id drone123 --hours 24
fishing-cli drone track --track-id 456
fishing-cli drone analyze --track-id 456
```

**MCP工具**:
- `get_drone_status` - 获取状态
- `get_telemetry_history` - 获取历史数据
- `get_track_data` - 获取轨迹
- `analyze_track` - 分析轨迹

## 安装说明

### 1. 安装依赖

```bash
cd 千鱼千寻2.0
pip install -e .
```

### 2. 配置环境变量

需要在父目录（Agent_Pro）中配置 `.env` 或 `config.env` 文件：

```env
# Neo4j 图数据库
NEO4J_URI=bolt://192.168.1.79:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=fishing_hero_2025

# AI模型
EMBED_MODEL=shibing624/text2vec-base-chinese
HF_ENDPOINT=https://hf-mirror.com

# 微信配置
WX_APPID=wxcea48780209aa522
WX_APPSECRET=your_secret_here
```

### 3. 测试CLI

```bash
# 查看版本
fishing-cli --version

# 查看所有技能
fishing-cli skills

# 查看配置
fishing-cli config

# 测试命令
fishing-cli coach ask "鲫鱼怎么钓?"
```

### 4. 启动MCP服务器

```bash
# 启动钓鱼教练MCP服务器
python mcp_servers/fishing_coach_server.py

# 启动鱼类识别MCP服务器
python mcp_servers/fish_identifier_server.py

# 启动天气顾问MCP服务器
python mcp_servers/weather_advisor_server.py

# 启动钓点管理MCP服务器
python mcp_servers/spot_manager_server.py
# 启动渔获记录MCP服务器
python mcp_servers/catch_tracker_server.py

# 启动社交管理MCP服务器
python mcp_servers/social_manager_server.py

# 启动无人船控制MCP服务器
python mcp_servers/drone_controller_server.py
```

---

## OpenClaw 集成

### 技能注册

每个技能都有 `SKILL.md` 文件，包含 OpenClaw 元数据：

```yaml
---
name: fishing-coach
description: "AI fishing coach with RAG and knowledge graph..."
metadata:
  {
    "openclaw": {
      "emoji": "🎓",
      "requires": {
        "env": ["NEO4J_URI"]
      },
      "os": ["linux", "darwin", "win32"]
    }
  }
---
```

### 使用 OpenClaw 调用

```bash
# 验证技能
openclaw skills validate skills/fishing-coach/SKILL.md

# 列出技能
openclaw skills list

# 使用技能
openclaw agent --message "use fishing-coach to answer: 鲫鱼怎么钓?"
```

---

## 依赖说明

### 核心依赖
- `click>=8.1.0` - CLI框架
- `python-dotenv>=1.0.0` - 环境变量管理
- `fastapi>=0.100.0` - Web框架（父项目）
- `uvicorn>=0.23.0` - ASGI服务器（父项目）

### 可选依赖
- `mcp>=0.5.0` - MCP SDK（可选，有降级实现）
- `pytest>=7.0.0` - 测试框架（开发）

### 父项目依赖
这些技能需要访问父项目（Agent_Pro）的模块：
- `advanced_agent_v4_reasoning.py` - AI教练
- `fusion_fish_recognition.py` - 鱼类识别
- `volc_tools.py` - 天气工具
- `fishing_spots_db.py` - 钓点数据库
- `neo4j` - 知识图谱
- `chromadb` - 向量数据库

---

## 开发指南

### 添加新技能

1. 创建技能目录：
```bash
mkdir skills/new-skill
```

2. 创建必需文件：
```
skills/new-skill/
├── SKILL.md          # OpenClaw技能定义
├── service.py        # 服务实现
├── cli.py            # CLI命令
└── __init__.py       # 包导出
```

3. 创建MCP服务器：
```python
# mcp_servers/new_skill_server.py
from mcp_servers import MCPServerBase
from skills.new_skill.service import NewSkillService

class NewSkillMCPServer(MCPServerBase):
    def __init__(self):
        super().__init__("new-skill", "1.0.0")
        self.service = NewSkillService()
    
    def setup_tools(self):
        # 注册工具
        pass
```

4. 在 `cli/main.py` 中添加命令组

---

## 测试

### 单元测试
```bash
pytest tests/
```

### 集成测试
```bash
# 测试CLI
fishing-cli coach ask "测试问题"

# 测试MCP服务器
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_servers/fishing_coach_server.py
```

---

## 项目状态

### 已完成 ✅
- Wave 1: 基础设施 (100%)
- Wave 2: 核心技能 (100%)
  - ✅ fishing-coach
  - ✅ fish-identifier
  - ✅ weather-advisor
  - ✅ spot-manager
- Wave 3: 数据技能 (100%)
  - ✅ catch-tracker (渔获记录)
  - ✅ social-manager (社交功能)
  - ✅ drone-controller (无人船遥测)

### 待完成 ⏳

---

## 统计数据

- **总文件数**: 50+个
- **总代码行数**: ~4,000行
- **技能数量**: 7个（全部完成）
- **MCP服务器**: 7个
- **CLI命令**: 25+个
- **零破坏性变更**: ✅

---

## 许可证

MIT License

---

## 联系方式

- 项目: 千鱼千寻 (QianYuQianXun)
- 版本: 2.0.0
- 团队: Agent_Pro Team

---

## 更新日志

### v2.0.0 (2026-03-10)
- ✅ 实现基础设施框架
- ✅ 实现4个核心技能
- ✅ CLI和MCP双接口
- ✅ OpenClaw兼容的技能定义
- ✅ 完整的文档和示例
