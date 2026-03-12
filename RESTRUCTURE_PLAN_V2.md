# 千鱼千寻项目重构方案 V2

## 🎯 核心理念

- **千鱼千寻 2.0** = 钓鱼垂直领域的核心业务系统
- **千鱼千寻 3.0** = 通用的 Skills 工具集（可复用到其他项目）

---

## 📁 新的目录结构

```
千鱼千寻/                          # 项目根目录
├── .claude/                       # Claude 配置
│   ├── skills/                    # Claude 自动化 Skills（4个）
│   │   ├── auto-test.md
│   │   ├── github-login.md
│   │   ├── smart-platform-operation.md
│   │   └── social-login.md
│   ├── memory/                    # 项目记忆
│   │   ├── MEMORY.md             # 主记忆
│   │   ├── automation.md         # 自动化记忆
│   │   └── skills.md             # Skills 使用指南
│   └── settings.local.json
│
├── docs/                          # 文档
│   ├── PROJECT_OVERVIEW.md
│   ├── CLI_COMPARISON.md
│   ├── PROJECT_STRUCTURE_CLEANUP.md
│   └── RESTRUCTURE_PLAN_V2.md
│
├── fishing-app/                   # 千鱼千寻 2.0 - 钓鱼核心业务
│   ├── api/                       # FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/v1/           # API 路由
│   │   │   ├── core/             # 核心配置
│   │   │   ├── models/           # 数据模型
│   │   │   ├── services/         # 业务逻辑
│   │   │   └── schemas/          # Pydantic 模型
│   │   └── main.py
│   │
│   ├── web/                       # Web 前端
│   │   ├── index.html
│   │   └── api.py
│   │
│   ├── skills/                    # 钓鱼专属 Skills（7个核心）
│   │   ├── fish-identifier/      # 鱼类识别
│   │   ├── fishing-coach/        # 钓鱼教练
│   │   ├── spot-manager/         # 钓点管理
│   │   ├── weather-advisor/      # 天气顾问
│   │   ├── catch-tracker/        # 渔获记录
│   │   ├── social-manager/       # 社交管理
│   │   └── drone-controller/     # 无人船控制
│   │
│   ├── mcp_servers/               # 钓鱼业务 MCP 服务器
│   │   ├── base.py
│   │   ├── fishing_coach_server.py
│   │   ├── fish_identifier_server.py
│   │   └── ...
│   │
│   ├── backend/                   # 旧后端代码（待重构）
│   │   ├── agents/
│   │   ├── integrations/
│   │   └── internal_api.py
│   │
│   ├── openclaw/                  # OpenClaw 集成
│   │   ├── gateway.py
│   │   └── config_loader.py
│   │
│   ├── cli/                       # 钓鱼业务 CLI
│   │   ├── main.py
│   │   └── utils.py
│   │
│   ├── shared/                    # 钓鱼业务共享代码
│   │   ├── skill_base.py
│   │   ├── config_manager.py
│   │   └── response_formatter.py
│   │
│   ├── pyproject.toml
│   ├── setup.py
│   └── README.md
│
├── universal-skills/              # 千鱼千寻 3.0 - 通用 Skills 工具集
│   ├── automation/                # 自动化工具
│   │   ├── src/
│   │   │   ├── logins/           # 登录脚本
│   │   │   │   ├── github.js
│   │   │   │   ├── xiaohongshu.js
│   │   │   │   ├── douyin.js
│   │   │   │   └── bilibili.js
│   │   │   ├── utils/            # 工具函数
│   │   │   └── index.js
│   │   ├── cookies/              # Cookie 存储
│   │   ├── screenshots/          # 截图
│   │   ├── tests/                # 测试
│   │   ├── package.json
│   │   ├── .env.example
│   │   └── README.md
│   │
│   ├── skills/                    # 通用 Skills（可复用）
│   │   ├── gemini-ui-designer/   # UI 设计器
│   │   ├── web-deployer/         # Web 部署
│   │   ├── angler-radar/         # 用户雷达（通用化）
│   │   ├── user-manager/         # 用户管理
│   │   ├── fishing-report-manager/ # 报告管理（通用化）
│   │   ├── persona-manager/      # 人格管理
│   │   └── feedback-manager/     # 反馈管理
│   │
│   ├── experimental/              # 实验性 Skills
│   │   ├── code-checker/
│   │   ├── folder-organizer/
│   │   ├── permission-manager/
│   │   └── task-notifier/
│   │
│   ├── shared/                    # 通用共享代码
│   │   ├── skill_base.py
│   │   ├── config_manager.py
│   │   └── response_formatter.py
│   │
│   ├── cli/                       # 通用 CLI
│   │   ├── main.py
│   │   └── utils.py
│   │
│   ├── mcp_servers/               # 通用 MCP 服务器
│   │   ├── base.py
│   │   └── ...
│   │
│   ├── deployment/                # 部署配置
│   ├── docs/                      # 文档
│   ├── frontend/                  # 前端（如果有）
│   ├── pyproject.toml
│   └── README.md
│
├── .snapshots/                    # 快照
├── .gitignore
└── README.md                      # 项目总览
```

---

## 🔄 Skills 分类逻辑

### 钓鱼核心业务 Skills（fishing-app/skills/）
**特点**: 钓鱼垂直领域，不可复用
- fish-identifier - 鱼类识别
- fishing-coach - 钓鱼教练
- spot-manager - 钓点管理
- weather-advisor - 天气顾问
- catch-tracker - 渔获记录
- social-manager - 社交管理
- drone-controller - 无人船控制

### 通用 Skills（universal-skills/skills/）
**特点**: 可复用到其他项目
- gemini-ui-designer - UI 设计器（通用）
- web-deployer - Web 部署（通用）
- angler-radar - 用户雷达（可改名为 user-radar）
- user-manager - 用户管理（通用）
- fishing-report-manager - 报告管理（可改名为 report-manager）
- persona-manager - 人格管理（通用）
- feedback-manager - 反馈管理（通用）

### 实验性 Skills（universal-skills/experimental/）
**特点**: 仅有文档，未实现
- code-checker
- folder-organizer
- permission-manager
- task-notifier

---

## 📋 执行步骤

### Step 1: 备份
```bash
cd "e:/桌面/南科大/未来企业家俱乐部/声纳鱼探/Agent_Pro"
cp -r 千鱼千寻2.0 千鱼千寻2.0_backup_20260312
```

### Step 2: 创建新目录
```bash
cd 千鱼千寻2.0
mkdir -p fishing-app/{api,web,skills,mcp_servers,backend,openclaw,cli,shared}
mkdir -p universal-skills/{automation,skills,experimental,shared,cli,mcp_servers}
mkdir -p docs
mkdir -p .claude/memory
```

### Step 3: 移动钓鱼核心业务代码
```bash
# 移动核心 skills
mv skills/fish-identifier fishing-app/skills/
mv skills/fishing-coach fishing-app/skills/
mv skills/spot-manager fishing-app/skills/
mv skills/weather-advisor fishing-app/skills/
mv skills/catch-tracker fishing-app/skills/
mv skills/social-manager fishing-app/skills/
mv skills/drone-controller fishing-app/skills/

# 移动其他钓鱼业务代码
mv mcp_servers/* fishing-app/mcp_servers/
mv backend/* fishing-app/backend/
mv openclaw/* fishing-app/openclaw/
mv cli/* fishing-app/cli/
mv shared/* fishing-app/shared/
mv web/* fishing-app/web/
mv pyproject.toml fishing-app/
mv setup.py fishing-app/
```

### Step 4: 移动通用 Skills 代码
```bash
# 移动 3.0 的自动化代码
mv 千鱼千寻3.0/automation/* universal-skills/automation/

# 移动通用 skills
mv skills/gemini-ui-designer universal-skills/skills/
mv 千鱼千寻3.0/skills/web-deployer universal-skills/skills/
mv skills/angler-radar universal-skills/skills/
mv skills/user-manager universal-skills/skills/
mv skills/fishing-report-manager universal-skills/skills/
mv skills/persona-manager universal-skills/skills/
mv skills/feedback-manager universal-skills/skills/

# 移动实验性 skills
mv skills/code-checker universal-skills/experimental/
mv skills/folder-organizer universal-skills/experimental/
mv skills/permission-manager universal-skills/experimental/
mv skills/task-notifier universal-skills/experimental/

# 移动 3.0 的共享代码
mv 千鱼千寻3.0/shared/* universal-skills/shared/
mv 千鱼千寻3.0/cli/* universal-skills/cli/
mv 千鱼千寻3.0/mcp_servers/* universal-skills/mcp_servers/
```

### Step 5: 移动文档
```bash
mv PROJECT_OVERVIEW.md docs/
mv CLI_COMPARISON.md docs/
mv PROJECT_STRUCTURE_CLEANUP.md docs/
mv RESTRUCTURE_PLAN_V2.md docs/
```

### Step 6: 移动项目记忆
```bash
# 从全局记忆复制到项目记忆
cp "C:/Users/Administrator/.claude/projects/e-----------------------Agent-Pro-----2-0/memory/MEMORY.md" .claude/memory/
```

### Step 7: 清理旧目录
```bash
# 删除空目录
rmdir skills 2>/dev/null || true
rmdir mcp_servers 2>/dev/null || true
rmdir backend 2>/dev/null || true
rmdir openclaw 2>/dev/null || true
rmdir cli 2>/dev/null || true
rmdir shared 2>/dev/null || true
rmdir web 2>/dev/null || true

# 删除 3.0 目录（已整合）
rm -rf 千鱼千寻3.0
```

---

## ✅ 整理后的优势

1. **清晰的业务边界**
   - 钓鱼业务 vs 通用工具
   - 核心功能 vs 实验功能

2. **可复用性**
   - 通用 Skills 可以用到其他项目
   - 自动化工具独立维护

3. **易于维护**
   - 每个子项目有独立的配置
   - 清晰的依赖关系

4. **可扩展性**
   - 新的垂直业务可以创建新的 app
   - 新的通用工具加入 universal-skills

---

## 🚀 后续优化

1. 为 fishing-app 和 universal-skills 创建独立的 README
2. 更新所有导入路径
3. 创建 Docker Compose 配置
4. 设置 Git 子模块（如果需要）
5. 创建统一的 CLI 入口
