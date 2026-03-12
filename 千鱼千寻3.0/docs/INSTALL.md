# 千鱼千寻 2.0 - 安装和使用指南

## 快速开始

### 1. 环境要求

- Python 3.10+
- 父项目（Agent_Pro）的依赖已安装

### 2. 安装步骤

```bash
# 进入千鱼千寻2.0目录
cd 千鱼千寻2.0

# 安装依赖（如果需要）
pip install click python-dotenv

# 测试CLI
python -m cli.main --version
```

### 3. 配置环境变量

在父目录（Agent_Pro）中确保有 `.env` 或 `config.env` 文件：

```env
# Neo4j 图数据库
NEO4J_URI=bolt://192.168.1.79:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=fishing_hero_2025

# AI模型
EMBED_MODEL=shibing624/text2vec-base-chinese
HF_ENDPOINT=https://hf-mirror.com
```

## 使用示例

### CLI命令

```bash
# 查看所有技能
python -m cli.main skills

# 钓鱼教练
python -m cli.main coach ask "鲫鱼怎么钓?"

# 鱼类识别
python -m cli.main fish recognize ./my_catch.jpg

# 天气查询
python -m cli.main weather current --city "深圳"

# 钓点搜索
python -m cli.main spots nearby --lat 22.5 --lon 114.0
```

### MCP服务器

```bash
# 启动钓鱼教练MCP服务器
python mcp_servers/fishing_coach_server.py

# 启动鱼类识别MCP服务器
python mcp_servers/fish_identifier_server.py

# 启动天气顾问MCP服务器
python mcp_servers/weather_advisor_server.py

# 启动钓点管理MCP服务器
python mcp_servers/spot_manager_server.py
```

## 目录说明

```
千鱼千寻2.0/
├── README.md              # 项目说明文档
├── INSTALL.md             # 本安装指南
├── setup.py               # 安装配置
├── pyproject.toml         # 项目配置
│
├── shared/                # 共享基础设施
│   ├── skill_base.py      # 技能基类
│   ├── config_manager.py  # 配置管理
│   ├── response_formatter.py  # 响应格式化
│   └── __init__.py
│
├── cli/                   # CLI命令行界面
│   ├── main.py            # CLI主程序
│   ├── utils.py           # CLI工具
│   └── __init__.py
│
├── mcp_servers/           # MCP服务器
│   ├── base.py            # MCP基础服务器
│   ├── fishing_coach_server.py
│   ├── fish_identifier_server.py
│   ├── weather_advisor_server.py
│   ├── spot_manager_server.py
│   └── __init__.py
│
└── skills/                # OpenClaw技能
    ├── fishing-coach/     # 钓鱼教练
    │   ├── SKILL.md       # 技能定义
    │   ├── service.py     # 服务实现
    │   ├── cli.py         # CLI命令
    │   └── __init__.py
    ├── fish-identifier/   # 鱼类识别
    ├── weather-advisor/   # 天气顾问
    └── spot-manager/      # 钓点管理
```

## 技能说明

### 1. 🎓 fishing-coach (钓鱼教练)
- **功能**: AI驱动的钓鱼问答，集成RAG和知识图谱
- **CLI**: `python -m cli.main coach ask "问题"`
- **MCP工具**: `coach_ask`, `coach_chat`, `get_user_memory`

### 2. 🐟 fish-identifier (鱼类识别)
- **功能**: 基于AI视觉的鱼类物种识别，支持3000+鱼种
- **CLI**: `python -m cli.main fish recognize 图片路径`
- **MCP工具**: `identify_fish`, `get_fish_tips`

### 3. 🌤️ weather-advisor (天气顾问)
- **功能**: 实时天气预报和钓鱼适宜度分析
- **CLI**: `python -m cli.main weather current --city "深圳"`
- **MCP工具**: `get_weather`, `get_forecast`, `calculate_fishing_index`

### 4. 📍 spot-manager (钓点管理)
- **功能**: 钓点搜索和管理，包含99个深圳钓点数据库
- **CLI**: `python -m cli.main spots nearby --lat 22.5 --lon 114.0`
- **MCP工具**: `get_nearby_spots`, `search_spots`, `get_spot_details`

## 依赖说明

### 核心依赖
- `click>=8.1.0` - CLI框架
- `python-dotenv>=1.0.0` - 环境变量管理

### 父项目依赖
这些技能需要访问父项目（Agent_Pro）的模块：
- `advanced_agent_v4_reasoning.py` - AI教练
- `fusion_fish_recognition.py` - 鱼类识别
- `volc_tools.py` - 天气工具
- `fishing_spots_db.py` - 钓点数据库

## 故障排除

### 问题1: 导入错误
```
ModuleNotFoundError: No module named 'advanced_agent_v4_reasoning'
```

**解决方案**: 确保在父目录（Agent_Pro）中运行，或者将父目录添加到Python路径：
```python
import sys
sys.path.insert(0, '../')
```

### 问题2: 配置文件未找到
```
FileNotFoundError: config.env
```

**解决方案**: 在父目录（Agent_Pro）中创建 `config.env` 文件，包含必要的环境变量。

### 问题3: 数据库连接失败
```
Neo4j connection failed
```

**解决方案**: 检查 Neo4j 服务是否运行，确认连接信息正确。

## 开发说明

### 添加新技能

1. 在 `skills/` 目录下创建新技能文件夹
2. 创建必需文件：`SKILL.md`, `service.py`, `cli.py`, `__init__.py`
3. 在 `mcp_servers/` 中创建对应的MCP服务器
4. 在 `cli/main.py` 中添加CLI命令组

### 测试技能

```bash
# 测试CLI
python -m cli.main <skill> <command> <args>

# 测试MCP服务器
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_servers/<skill>_server.py
```

## 联系方式

- 项目: 千鱼千寻 (QianYuQianXun)
- 版本: 2.0.0
- 团队: Agent_Pro Team

## 许可证

MIT License
