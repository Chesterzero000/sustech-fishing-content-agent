# 千鱼千寻项目目录整理方案

## 📊 当前问题分析

### 1. 重复目录
- **千鱼千寻2.0/** (根目录) 和 **千鱼千寻3.0/** 存在大量重复代码
- `shared/`, `cli/`, `mcp_servers/`, `skills/` 在两个版本中都有

### 2. Skills 混乱
根目录 `skills/` 包含 **17 个技能**，分为三类：

#### A. 完整实现的核心技能（7个）✅
- `fish-identifier/` - 鱼类识别
- `fishing-coach/` - 钓鱼教练
- `spot-manager/` - 钓点管理
- `weather-advisor/` - 天气顾问
- `catch-tracker/` - 渔获记录
- `social-manager/` - 社交管理
- `drone-controller/` - 无人船控制

#### B. 部分实现的扩展技能（6个）⚠️
- `angler-radar/` - 钓友雷达（有 service.py）
- `fishing-report-manager/` - 钓鱼报告管理（有 service.py）
- `user-manager/` - 用户管理（有 service.py）
- `persona-manager/` - 人格管理（只有 service.py）
- `feedback-manager/` - 反馈管理（只有 service.py）
- `gemini-ui-designer/` - UI 设计器（完整实现）

#### C. 仅有文档的占位技能（4个）📄
- `code-checker/` - 代码检查（只有 SKILL.md）
- `folder-organizer/` - 文件夹整理（只有 SKILL.md）
- `permission-manager/` - 权限管理（只有 SKILL.md）
- `task-notifier/` - 任务通知（只有 SKILL.md）

### 3. Claude Skills 位置混乱
- **项目级 Skills**: `.claude/skills/` (4个自动化 skills)
  - `auto-test.md`
  - `github-login.md`
  - `smart-platform-operation.md`
  - `social-login.md`

- **全局记忆**: `C:/Users/Administrator/.claude/projects/e-----------------------Agent-Pro-----2-0/memory/`
  - `MEMORY.md` (项目记忆，应该是项目级的)

---

## 🎯 整理方案

### 方案 A: 合并版本（推荐）

```
千鱼千寻/                          # 统一项目根目录
├── .claude/                       # Claude 配置（项目级）
│   ├── skills/                    # Claude 自动化 Skills
│   │   ├── auto-test.md
│   │   ├── github-login.md
│   │   ├── smart-platform-operation.md
│   │   └── social-login.md
│   ├── memory/                    # 项目记忆（移到这里）
│   │   └── MEMORY.md
│   └── settings.local.json
│
├── docs/                          # 文档
│   ├── PROJECT_OVERVIEW.md
│   ├── CLI_COMPARISON.md
│   └── API_DOCS.md
│
├── apps/                          # 应用层
│   ├── api/                       # FastAPI 后端
│   │   ├── app/
│   │   │   ├── api/v1/           # API 路由
│   │   │   ├── core/             # 核心配置
│   │   │   ├── models/           # 数据模型
│   │   │   ├── services/         # 业务逻辑
│   │   │   └── schemas/          # Pydantic 模型
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   ├── web/                       # Web 前端（未来）
│   │   └── index.html
│   │
│   └── automation/                # 自动化服务
│       ├── src/
│       │   ├── logins/           # 登录脚本
│       │   ├── utils/            # 工具函数
│       │   └── index.js
│       ├── cookies/              # Cookie 存储
│       ├── screenshots/          # 截图
│       ├── package.json
│       └── .env
│
├── packages/                      # 共享代码
│   ├── shared/                    # Python 共享模块
│   │   ├── skill_base.py
│   │   ├── config_manager.py
│   │   └── response_formatter.py
│   │
│   └── cli/                       # CLI 工具
│       ├── main.py
│       └── utils.py
│
├── skills/                        # OpenClaw Skills
│   ├── core/                      # 核心技能（7个）
│   │   ├── fish-identifier/
│   │   ├── fishing-coach/
│   │   ├── spot-manager/
│   │   ├── weather-advisor/
│   │   ├── catch-tracker/
│   │   ├── social-manager/
│   │   └── drone-controller/
│   │
│   ├── extended/                  # 扩展技能（6个）
│   │   ├── angler-radar/
│   │   ├── fishing-report-manager/
│   │   ├── user-manager/
│   │   ├── persona-manager/
│   │   ├── feedback-manager/
│   │   └── gemini-ui-designer/
│   │
│   └── experimental/              # 实验性技能（4个）
│       ├── code-checker/
│       ├── folder-organizer/
│       ├── permission-manager/
│       └── task-notifier/
│
├── mcp_servers/                   # MCP 服务器
│   ├── base.py
│   ├── fishing_coach_server.py
│   ├── fish_identifier_server.py
│   └── ...
│
├── backend/                       # 后端服务（旧代码）
│   ├── agents/
│   ├── integrations/
│   └── internal_api.py
│
├── openclaw/                      # OpenClaw 集成
│   ├── gateway.py
│   ├── config_loader.py
│   └── feishu_handler.py
│
├── tests/                         # 测试
│   ├── unit/
│   └── integration/
│
├── .snapshots/                    # 快照
├── pyproject.toml
├── setup.py
└── README.md
```

### 方案 B: 保留双版本（不推荐）

如果你想保留 2.0 和 3.0 的区分：

```
千鱼千寻/
├── v2/                            # 2.0 版本（稳定版）
│   ├── skills/
│   ├── cli/
│   └── ...
│
├── v3/                            # 3.0 版本（开发版）
│   ├── automation/
│   ├── skills/
│   └── ...
│
└── shared/                        # 共享代码
    ├── packages/
    └── docs/
```

---

## 🔧 执行步骤

### Step 1: 备份当前项目
```bash
cd "e:/桌面/南科大/未来企业家俱乐部/声纳鱼探/Agent_Pro"
cp -r 千鱼千寻2.0 千鱼千寻2.0_backup_$(date +%Y%m%d)
```

### Step 2: 创建新目录结构
```bash
cd 千鱼千寻2.0
mkdir -p apps/{api,web,automation}
mkdir -p packages/{shared,cli}
mkdir -p skills/{core,extended,experimental}
mkdir -p docs
mkdir -p .claude/memory
```

### Step 3: 移动 Skills
```bash
# 核心技能
mv skills/fish-identifier skills/core/
mv skills/fishing-coach skills/core/
mv skills/spot-manager skills/core/
mv skills/weather-advisor skills/core/
mv skills/catch-tracker skills/core/
mv skills/social-manager skills/core/
mv skills/drone-controller skills/core/

# 扩展技能
mv skills/angler-radar skills/extended/
mv skills/fishing-report-manager skills/extended/
mv skills/user-manager skills/extended/
mv skills/persona-manager skills/extended/
mv skills/feedback-manager skills/extended/
mv skills/gemini-ui-designer skills/extended/

# 实验性技能
mv skills/code-checker skills/experimental/
mv skills/folder-organizer skills/experimental/
mv skills/permission-manager skills/experimental/
mv skills/task-notifier skills/experimental/
```

### Step 4: 整合自动化代码
```bash
# 移动 3.0 的自动化代码到统一位置
mv 千鱼千寻3.0/automation/* apps/automation/
```

### Step 5: 移动共享代码
```bash
mv shared/* packages/shared/
mv cli/* packages/cli/
```

### Step 6: 移动项目记忆
```bash
# 从全局记忆移到项目记忆
cp "C:/Users/Administrator/.claude/projects/e-----------------------Agent-Pro-----2-0/memory/MEMORY.md" .claude/memory/
```

### Step 7: 清理旧目录
```bash
# 删除空目录和重复代码
rm -rf 千鱼千寻3.0/shared
rm -rf 千鱼千寻3.0/cli
rm -rf 千鱼千寻3.0/mcp_servers
# 保留 千鱼千寻3.0 作为参考，稍后决定是否删除
```

---

## 📝 记忆文件整理

### 全局记忆 vs 项目记忆

**全局记忆** (`C:/Users/Administrator/.claude/memory/`)
- 跨项目的通用知识
- Claude 使用技巧
- 个人偏好设置
- 常用命令和工具

**项目记忆** (`.claude/memory/MEMORY.md`)
- 项目特定的配置
- 账号信息
- 技术栈选择
- 已完成/待完成任务
- 常见问题解决方案

### 建议的记忆文件结构

```
.claude/memory/
├── MEMORY.md              # 主记忆文件（项目概览）
├── automation.md          # 自动化相关记忆
├── skills.md              # Skills 使用指南
└── troubleshooting.md     # 常见问题
```

---

## ✅ 整理后的优势

1. **清晰的分层**
   - 核心技能 vs 扩展技能 vs 实验性技能
   - 应用层 vs 包层 vs 服务层

2. **消除重复**
   - 统一的 shared 代码
   - 统一的 CLI 工具
   - 统一的自动化脚本

3. **易于维护**
   - 明确的目录职责
   - 清晰的依赖关系
   - 便于测试和部署

4. **可扩展性**
   - 新技能有明确的归属
   - 易于添加新的应用
   - 支持微服务拆分

---

## 🚀 下一步

选择一个方案后，我可以帮你：
1. 自动执行目录重组
2. 更新所有导入路径
3. 更新文档和配置文件
4. 创建新的 README
5. 设置 Git 忽略规则

你想选择哪个方案？我推荐**方案 A（合并版本）**。
