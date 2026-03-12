# 千鱼千寻项目记忆

## 项目概述
- 项目名称：千鱼千寻 2.0/3.0
- 项目路径：`e:/桌面/南科大/未来企业家俱乐部/声纳鱼探/Agent_Pro/千鱼千寻2.0`
- 主要功能：社交媒体自动化营销系统

## 自动化配置

### 账号信息
- GitHub: hc3571591632@163.com / hc001024
- 其他平台账号配置在 `.env` 文件中

### 自动化目录结构
```
千鱼千寻3.0/automation/
├── .env                    # 环境变量配置
├── tests/logins/          # 登录测试脚本
│   ├── github.js
│   ├── xiaohongshu.js
│   ├── douyin.js
│   └── bilibili.js
├── cookies/               # 保存的登录状态
├── screenshots/           # 测试截图
└── manual-login.js        # 手动辅助登录脚本
```

## Claude Skills

已创建的自动化 skills（位于 `.claude/skills/`）：

1. **github-login** - GitHub 手动辅助登录
   - 自动填写账号密码，手动完成验证
   - 保存 Cookies 到 `cookies/github.json`
   - 脚本：`manual-login.js`
   - 使用：`/github-login`

2. **social-login** - 社交媒体平台登录
   - 支持：小红书、抖音、B站、微博、知乎
   - 自动化登录和 Cookies 管理
   - 脚本：`tests/logins/{platform}.js`
   - 使用：`/social-login`

3. **auto-test** - 自动化测试套件
   - 批量测试所有平台登录状态
   - 验证 Cookies 有效性
   - 生成测试报告（JSON + TXT）
   - 脚本：`run-all-tests.js`
   - 使用：`/auto-test`

## 核心脚本

### 登录脚本
- `manual-login.js` - GitHub 手动辅助登录
- `tests/logins/xiaohongshu.js` - 小红书登录
- `tests/logins/douyin.js` - 抖音登录
- `tests/logins/bilibili.js` - B站登录

### 工具脚本
- `run-all-tests.js` - 批量测试所有平台
- `verify-cookies.js` - Cookies 有效性验证
- `quick-test.js` - 快速测试（用于调试）

## 技术栈
- Node.js + Playwright（浏览器自动化）
- Python（后端逻辑）
- dotenv（环境变量管理）

## 常见问题

### GitHub 登录问题
- 错误：`ERR_CONNECTION_CLOSED` → 网络问题，需要稳定网络
- 错误：`You can't perform that action at this time` → GitHub 检测到自动化，使用 `manual-login.js` 手动辅助登录
- 解决方案：使用手动辅助登录保存 Cookies，后续使用 Cookies 自动登录

### Cookies 管理
- Cookies 保存在 `automation/cookies/` 目录
- 定期检查 Cookies 有效性
- 过期后需要重新登录

## 工作流程
1. 配置 `.env` 文件（账号密码）
2. 首次登录使用手动辅助脚本
3. 保存 Cookies 后可自动登录
4. 定期运行测试套件验证状态

## 已完成的任务（2026-03-12）
- ✅ 创建 GitHub 手动辅助登录脚本
- ✅ 创建小红书、抖音、B站登录脚本
- ✅ 实现批量测试功能（run-all-tests.js）
- ✅ 实现 Cookies 验证功能（verify-cookies.js）
- ✅ 生成测试报告（JSON + TXT 格式）
- ✅ 创建 3 个 Claude Skills（github-login, social-login, auto-test）
- ✅ 完善使用文档（README.md）
- ✅ 更新全局记忆
- ✅ 更新和完善所有 Skills 文档（添加详细的触发条件、使用方法、常见问题）
- ✅ 创建智能平台操作 Skill（smart-platform-operation）
- ✅ 实现链接自动识别和操作功能（smart-operation.js）
- ✅ 借鉴 CLI Anything 技术，实现自动包装器（cli-anything-wrapper.js）
- ✅ 对比分析 CLI Anything 与千鱼千寻 2.0（CLI_COMPARISON.md）

## 待完成的任务
- 🔄 完善 .env 配置文件（添加所有平台账号）
- 🔄 创建定时任务自动更新 Cookies
- 🔄 添加微博、知乎登录支持
- 🔄 实现内容自动发布功能
