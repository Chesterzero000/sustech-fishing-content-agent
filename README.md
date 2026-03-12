# 千鱼千寻 - 钓鱼社交平台 + AI Agent Skills 系统

> 南科大钓鱼协会自动化内容创作系统 - 利用 AI Agent、MCP 工具和 Skills 实现智能钓鱼服务

[![GitHub](https://img.shields.io/badge/GitHub-fishing--agent--robot-blue)](https://github.com/Chesterzero000/fishing-agent-robot)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green)](https://nodejs.org/)

---

## 📁 项目结构

```
千鱼千寻/
├── fishing-app/              # 千鱼千寻 2.0 - 钓鱼核心业务
│   ├── skills/               # 钓鱼专属 Skills（7个）
│   ├── api/                  # FastAPI 后端
│   ├── web/                  # Web 前端
│   ├── mcp_servers/          # MCP 服务器
│   └── ...
│
├── universal-skills/         # 千鱼千寻 3.0 - 通用工具集
│   ├── automation/           # 自动化工具（Playwright）
│   ├── skills/               # 通用 Skills（7个）
│   ├── experimental/         # 实验性 Skills（4个）
│   └── ...
│
├── .claude/                  # Claude 配置
│   ├── skills/               # Claude 自动化 Skills（4个）
│   └── memory/               # 项目记忆
│
└── docs/                     # 文档
```

---

## 🎯 项目组成

### 1. 钓鱼核心业务（fishing-app/）

**7 个钓鱼专属 Skills：**
- 🐟 **fish-identifier** - 鱼类识别（AI 视觉）
- 🎓 **fishing-coach** - 钓鱼教练（RAG + 知识图谱）
- 📍 **spot-manager** - 钓点管理（99个深圳钓点）
- 🌤️ **weather-advisor** - 天气顾问（钓鱼指数）
- 📊 **catch-tracker** - 渔获记录追踪
- 💬 **social-manager** - 社交功能管理
- 🚁 **drone-controller** - 无人船遥测控制

### 2. 通用工具集（universal-skills/）

**自动化工具（automation/）：**
- 🤖 社交媒体自动登录（GitHub、小红书、抖音、B站等）
- 🍪 Cookies 管理和验证
- 📸 自动截图和测试报告
- 🔧 CLI Anything 包装器

**7 个通用 Skills：**
- 🎨 **gemini-ui-designer** - UI 设计器
- 🚀 **web-deployer** - Web 部署
- 🔍 **angler-radar** - 用户雷达
- 👤 **user-manager** - 用户管理
- 📝 **fishing-report-manager** - 报告管理
- 🎭 **persona-manager** - 人格管理
- 💭 **feedback-manager** - 反馈管理

**4 个实验性 Skills：**
- code-checker、folder-organizer、permission-manager、task-notifier

### 3. Claude 自动化 Skills（.claude/skills/）

- **github-login** - GitHub 手动辅助登录
- **social-login** - 社交媒体平台登录
- **auto-test** - 自动化测试套件
- **smart-platform-operation** - 智能平台操作

---

## 🚀 快速开始

### 钓鱼业务系统

```bash
cd fishing-app

# 安装依赖
pip install -e .

# 测试 CLI
fishing-cli --version
fishing-cli coach ask "鲫鱼怎么钓?"

# 启动 Web API
python web/api.py
```

### 自动化工具

```bash
cd universal-skills/automation

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入账号密码

# 测试登录
npm run login:github
npm run login:all
```

---

## 📚 文档

- [项目概览](docs/PROJECT_OVERVIEW.md)
- [CLI 对比分析](docs/CLI_COMPARISON.md)
- [目录结构整理方案](docs/PROJECT_STRUCTURE_CLEANUP.md)
- [重构计划 V2](docs/RESTRUCTURE_PLAN_V2.md)

---

## 🛠️ 技术栈

### 后端
- **Python 3.10+** - 主要编程语言
- **FastAPI** - Web 框架
- **Click** - CLI 框架
- **MCP Protocol** - Model Context Protocol

### 前端
- **HTML/CSS/JavaScript** - Web 前端
- **Next.js**（计划中）- React 框架

### 自动化
- **Node.js 18+** - JavaScript 运行时
- **Playwright** - 浏览器自动化
- **dotenv** - 环境变量管理

### AI/数据
- **Neo4j** - 知识图谱
- **ChromaDB** - 向量数据库
- **Sentence Transformers** - 文本嵌入

---

## 📊 项目统计

- **总文件数**: 200+ 个
- **总代码行数**: ~25,000 行
- **Skills 数量**: 18 个（核心 7 + 通用 7 + 实验 4）
- **MCP 服务器**: 7 个
- **CLI 命令**: 30+ 个
- **自动化脚本**: 10+ 个

---

## 🔧 开发指南

### 添加新的钓鱼 Skill

```bash
cd fishing-app/skills
mkdir new-skill
cd new-skill

# 创建必需文件
touch SKILL.md service.py cli.py __init__.py
```

### 添加新的通用 Skill

```bash
cd universal-skills/skills
mkdir new-skill
cd new-skill

# 创建必需文件
touch SKILL.md service.py cli.py __init__.py
```

---

## 📝 待办事项

- [ ] 完善 .env 配置文件
- [ ] 创建 Docker Compose 配置
- [ ] 添加微博、知乎登录支持
- [ ] 实现内容自动发布功能
- [ ] 创建 Next.js 前端
- [ ] 数据库迁移到 PostgreSQL
- [ ] 添加单元测试
- [ ] 完善 API 文档

---

## 📄 许可证

MIT License

---

## 👥 团队

- **项目**: 千鱼千寻 (QianYuQianXun)
- **版本**: 2.0.0 / 3.0.0
- **团队**: Agent_Pro Team
- **组织**: 南科大钓鱼协会

---

## 🔗 相关链接

- [GitHub 仓库](https://github.com/Chesterzero000/fishing-agent-robot)
- [问题反馈](https://github.com/Chesterzero000/fishing-agent-robot/issues)

---

**最后更新**: 2026-03-12
