# 千鱼千寻 3.0 自动化系统

社交媒体自动化营销系统，支持多平台自动登录、内容发布和数据分析。

## 📦 安装

```bash
cd automation
npm install
npx playwright install
```

## 🔧 配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的账号密码：
```bash
# Neon PostgreSQL
NEON_EMAIL=your-email@example.com
NEON_PASSWORD=your-password

# GitHub
GITHUB_USERNAME=your-username
GITHUB_PASSWORD=your-password

# 其他网站...
```

## 🚀 快速开始

### 1. 安装依赖
```bash
cd automation
npm install
npx playwright install
```

### 2. 配置账号
编辑 `.env` 文件，添加你的账号信息：
```env
# GitHub
GITHUB_USERNAME=your_email@example.com
GITHUB_PASSWORD=your_password

# 小红书
XIAOHONGSHU_PHONE=your_phone_number

# 其他平台...
```

### 3. 首次登录
```bash
# GitHub 手动辅助登录
node manual-login.js

# 小红书登录
node tests/logins/xiaohongshu.js

# 抖音登录
node tests/logins/douyin.js

# B站登录
node tests/logins/bilibili.js
```

### 4. 验证登录状态
```bash
node verify-cookies.js
```

### 5. 批量测试所有平台
```bash
node run-all-tests.js
```

## 📁 项目结构

```
automation/
├── tests/
│   └── logins/            # 各平台登录脚本
│       ├── github.js      # GitHub 登录
│       ├── xiaohongshu.js # 小红书登录
│       ├── douyin.js      # 抖音登录
│       └── bilibili.js    # B站登录
├── cookies/               # 保存的登录状态
│   ├── github.json
│   ├── xiaohongshu.json
│   ├── douyin.json
│   └── bilibili.json
├── screenshots/           # 测试截图
├── manual-login.js        # 手动辅助登录（GitHub）
├── run-all-tests.js       # 批量测试所有平台
├── verify-cookies.js      # Cookies 有效性验证
├── .env                   # 环境变量配置
├── package.json
└── README.md             # 本文档
```

## 🎯 功能特性

### 支持的平台
- ✅ GitHub - 手动辅助登录
- ✅ 小红书 - 扫码/手机号登录
- ✅ 抖音 - 扫码登录
- ✅ B站 - 扫码/密码/短信登录
- 🔄 微博（开发中）
- 🔄 知乎（开发中）

### 核心功能
- ✅ 自动登录和 Cookies 管理
- ✅ 批量测试和验证
- ✅ 测试报告生成（JSON + TXT）
- ✅ Cookies 有效性验证
- ✅ 自动截图保存
- ✅ Claude Skills 集成
- 🔄 定时任务支持（开发中）

## 📝 常见问题

### Q1: GitHub 登录失败，提示 "Incorrect username or password"
**A:** 检查 `.env` 文件中的邮箱和密码是否正确。

### Q2: 提示 "ERR_CONNECTION_CLOSED"
**A:** 网络连接问题，可能原因：
- GitHub 访问受限（需要代理）
- 网络不稳定
- 防火墙阻止

### Q3: 小红书/抖音无法自动填写账号密码
**A:** 这些平台主要使用扫码登录，需要手动扫码。脚本会等待 120 秒供你完成登录。

### Q4: Cookies 多久会过期？
**A:** 不同平台的 Cookies 有效期不同：
- GitHub: 约 30 天
- 小红书: 约 7-14 天
- 抖音: 约 7-14 天
- B站: 约 30 天

建议每周运行一次 `verify-cookies.js` 检查状态。

### Q5: 如何查看测试报告？
**A:** 运行 `node run-all-tests.js` 后，会生成：
- `test-report.json` - JSON 格式报告
- `test-report.txt` - 文本格式报告

查看文本报告：
```bash
# Windows
type test-report.txt

# Linux/Mac
cat test-report.txt
```

## ⚠️ 注意事项

1. **安全性**：不要提交 `.env` 文件到 Git
2. **验证码**：某些网站需要手动输入验证码，脚本会等待 120 秒
3. **双因素认证**：GitHub 等网站如果开启了 2FA，需要手动输入验证码
4. **扫码登录**：小红书、抖音、B站支持扫码登录
5. **Cookies 有效期**：保存的 Cookies 可能会过期，需要重新登录
6. **网络环境**：建议在稳定的网络环境下运行

## 🔧 命令参考

### 登录命令
```bash
# GitHub 手动辅助登录
node manual-login.js

# 小红书登录
node tests/logins/xiaohongshu.js

# 抖音登录
node tests/logins/douyin.js

# B站登录
node tests/logins/bilibili.js
```

### 测试命令
```bash
# 批量测试所有平台
node run-all-tests.js

# 验证 Cookies 有效性
node verify-cookies.js

# 单独测试某个平台
node tests/logins/github.js
```

### 维护命令
```bash
# 清理旧的截图
rm -rf screenshots/*

# 清理旧的 Cookies
rm -rf cookies/*

# 重新安装依赖
npm install

# 更新 Playwright
npx playwright install
```

## 🎨 Claude Skills

系统已集成 Claude Code Skills，可以使用以下命令：

```bash
# GitHub 登录
/github-login

# 社交媒体登录
/social-login

# 自动化测试
/auto-test

# 智能平台操作（新增）
/smart-platform-operation
```

## 🚀 新功能：智能平台操作

### 功能 1: 链接智能识别和操作

只需提供链接，系统自动识别平台并执行操作：

```bash
# 查看 GitHub 仓库
node smart-operation.js https://github.com/user/repo

# 给仓库点 Star
node smart-operation.js https://github.com/user/repo --action=star

# 查看小红书笔记
node smart-operation.js https://www.xiaohongshu.com/explore/xxx

# 给笔记点赞
node smart-operation.js https://www.xiaohongshu.com/explore/xxx --action=like
```

### 功能 2: CLI Anything 风格的自动包装

自动将任何网站转换为 CLI 接口：

```bash
# 包装网站
node cli-anything-wrapper.js --wrap https://example.com

# 执行生成的命令
node cli-anything-wrapper.js --execute ./cli-wrappers/example.json --command click-button-0
```

### 使用场景

1. **快速查看内容**
   ```
   用户: 帮我看看这个 GitHub 项目 https://github.com/HKUDS/CLI-Anything
   助手: [自动登录] → [提取信息] → [返回结果]
   ```

2. **批量操作**
   ```
   用户: 给这些仓库都点个 Star
   助手: [批量登录] → [依次点 Star] → [返回结果]
   ```

3. **自动化任务**
   ```
   用户: 每天自动点赞小红书热门笔记
   助手: [定时任务] → [自动登录] → [点赞] → [记录日志]
   ```

## 📊 更新日志

### v3.0.0 (2026-03-12)
- ✅ 完成 GitHub 手动辅助登录
- ✅ 创建小红书、抖音、B站登录脚本
- ✅ 实现批量测试功能
- ✅ 实现 Cookies 验证功能
- ✅ 生成测试报告（JSON + TXT）
- ✅ 集成 Claude Skills
- ✅ 完善使用文档

---

**祝使用愉快！🎉**

如有问题，请联系：hc3571591632@163.com
