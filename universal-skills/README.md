# 千鱼千寻 3.0 - 通用 Skills 工具集

> 可复用的 AI Agent Skills 和自动化工具

---

## 📦 包含内容

### 自动化工具（automation/）

**社交媒体自动登录：**
- GitHub
- 小红书
- 抖音
- B站
- 微信
- 飞书
- Neon
- Supabase
- Vercel

**功能：**
- 🍪 Cookies 管理和持久化
- 📸 自动截图和测试报告
- 🔄 批量测试和验证
- 🔧 CLI Anything 包装器

### 通用 Skills（skills/）

1. **gemini-ui-designer** - UI 设计器
2. **web-deployer** - Web 部署工具
3. **angler-radar** - 用户雷达（可改名为 user-radar）
4. **user-manager** - 用户管理
5. **fishing-report-manager** - 报告管理（可改名为 report-manager）
6. **persona-manager** - 人格管理
7. **feedback-manager** - 反馈管理

### 实验性 Skills（experimental/）

- **code-checker** - 代码检查（仅文档）
- **folder-organizer** - 文件夹整理（仅文档）
- **permission-manager** - 权限管理（仅文档）
- **task-notifier** - 任务通知（仅文档）

---

## 🚀 快速开始

### 自动化工具

```bash
cd automation

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入账号密码

# 测试单个平台
npm run login:github
npm run login:xiaohongshu

# 批量测试所有平台
npm run login:all

# 验证 Cookies
node verify-cookies.js

# 智能操作（自动识别链接）
node smart-operation.js "https://github.com/user/repo"
```

### 通用 Skills

```bash
# 安装依赖
pip install -e .

# 使用 CLI
# （具体命令取决于各个 Skill 的实现）
```

---

## 📁 目录结构

```
universal-skills/
├── automation/          # 自动化工具
│   ├── src/
│   │   ├── logins/     # 登录脚本
│   │   └── utils/      # 工具函数
│   ├── cookies/        # Cookie 存储
│   ├── screenshots/    # 截图
│   ├── tests/          # 测试
│   └── package.json
│
├── skills/              # 通用 Skills（7个）
├── experimental/        # 实验性 Skills（4个）
├── shared/              # 共享代码
├── cli/                 # CLI 工具
├── mcp_servers/         # MCP 服务器
├── deployment/          # 部署配置
├── docs/                # 文档
└── README.md            # 本文件
```

---

## 🔧 配置

### 自动化工具配置（.env）

```env
# GitHub
GITHUB_EMAIL=your_email@example.com
GITHUB_PASSWORD=your_password

# 小红书
XIAOHONGSHU_PHONE=your_phone
XIAOHONGSHU_PASSWORD=your_password

# 抖音
DOUYIN_PHONE=your_phone
DOUYIN_PASSWORD=your_password

# B站
BILIBILI_USERNAME=your_username
BILIBILI_PASSWORD=your_password

# 其他平台...
```

---

## 📚 文档

### 自动化工具文档

- [README](automation/README.md) - 使用指南
- [TUTORIAL](automation/TUTORIAL.md) - 详细教程
- [SMART_OPERATION_EXAMPLES](automation/SMART_OPERATION_EXAMPLES.md) - 智能操作示例

### 通用 Skills 文档

详见各个 Skill 目录下的 `SKILL.md` 文件。

---

## 🛠️ 技术栈

### 自动化
- Node.js 18+
- Playwright
- dotenv

### Skills
- Python 3.10+
- Click (CLI)
- MCP Protocol

---

## 🔄 复用到其他项目

这些工具和 Skills 设计为通用的，可以轻松复用到其他项目：

1. **复制整个 `automation/` 目录**
2. **配置 `.env` 文件**
3. **运行 `npm install`**
4. **开始使用**

Skills 同理，可以单独复制到其他项目。

---

## 📝 待办事项

- [ ] 添加微博、知乎登录支持
- [ ] 实现内容自动发布功能
- [ ] 完善实验性 Skills
- [ ] 添加更多通用 Skills
- [ ] 创建 Docker 镜像
- [ ] 添加单元测试

---

**返回**: [项目主页](../README.md)
