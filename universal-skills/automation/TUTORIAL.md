# Playwright 自动化登录 - 完整教程

## 📚 目录

1. [快速开始](#快速开始)
2. [配置步骤](#配置步骤)
3. [使用方法](#使用方法)
4. [工作原理](#工作原理)
5. [常见问题](#常见问题)
6. [高级用法](#高级用法)

---

## 🚀 快速开始

### 前置要求

- ✅ Node.js 已安装（v18+）
- ✅ npm 已安装
- ✅ 网络连接正常

### 一键安装

```bash
cd automation
npm install
npx playwright install
```

---

## ⚙️ 配置步骤

### 步骤 1：复制环境变量模板

**Windows:**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### 步骤 2：编辑 .env 文件

用文本编辑器打开 `.env` 文件：

```bash
# Neon PostgreSQL
NEON_EMAIL=你的邮箱@gmail.com
NEON_PASSWORD=你的密码

# GitHub
GITHUB_USERNAME=你的用户名
GITHUB_PASSWORD=你的密码

# 其他网站...
```

**⚠️ 重要提示：**
- 不要有空格：`NEON_EMAIL=test@gmail.com` ✅
- 不要加引号：`NEON_EMAIL="test@gmail.com"` ❌
- 不要提交到 Git：`.env` 已在 `.gitignore` 中

### 步骤 3：测试单个网站

```bash
# 测试 Neon PostgreSQL
npm run login:neon

# 或使用测试脚本
test.bat
```

---

## 📖 使用方法

### 方法 1：使用 npm scripts（推荐）

```bash
# 登录单个网站
npm run login:neon       # Neon PostgreSQL
npm run login:github     # GitHub
npm run login:wechat     # 微信公众平台
npm run login:supabase   # Supabase
npm run login:vercel     # Vercel
npm run login:feishu     # 飞书

# 批量登录所有网站
npm run login:all
```

### 方法 2：直接运行脚本

```bash
# 登录单个网站
node tests/index.js neon
node tests/index.js github

# 批量登录
node tests/index.js
```

### 方法 3：使用测试脚本

```bash
# Windows
test.bat              # 测试 Neon 登录
check-results.bat     # 检查登录结果

# Mac/Linux
./test.sh
```

---

## 🔍 工作原理

### 1. 通用登录助手 (loginHelper.js)

```javascript
const helper = new LoginHelper();

// 初始化浏览器
await helper.init();

// 执行登录
await helper.login({
  url: '登录页面 URL',
  usernameSelector: '用户名输入框的 CSS 选择器',
  passwordSelector: '密码输入框的 CSS 选择器',
  submitSelector: '登录按钮的 CSS 选择器',
  username: '你的用户名',
  password: '你的密码',
  waitForSelector: '登录成功后的元素选择器',
});

// 保存 Cookies
await helper.saveCookies('./cookies/site.json');

// 截图
await helper.screenshot('./screenshots/site-success.png');

// 关闭浏览器
await helper.close();
```

### 2. 登录流程

```
1. 启动浏览器（Chrome）
   ↓
2. 访问登录页面
   ↓
3. 等待页面加载完成
   ↓
4. 输入用户名
   ↓
5. 输入密码
   ↓
6. 执行提交前操作（可选）
   ↓
7. 点击登录按钮
   ↓
8. 等待登录成功
   ↓
9. 执行提交后操作（可选）
   ↓
10. 保存 Cookies
   ↓
11. 截图
   ↓
12. 关闭浏览器
```

### 3. 文件结构

```
automation/
├── tests/
│   ├── logins/
│   │   ├── neon.js          # 每个网站的登录脚本
│   │   ├── github.js
│   │   └── ...
│   └── index.js             # 主入口（批量登录）
├── utils/
│   └── loginHelper.js       # 通用登录助手类
├── cookies/                 # 保存的 Cookies
│   └── neon.json
├── screenshots/             # 截图
│   └── neon-success.png
└── .env                     # 环境变量（账号密码）
```

---

## ❓ 常见问题

### Q1: 登录失败怎么办？

**检查步骤：**

1. **查看截图**：`screenshots/网站名-error.png`
2. **检查 .env 配置**：确保账号密码正确
3. **检查网络**：确保能访问目标网站
4. **查看控制台输出**：看具体错误信息

**常见错误：**

```bash
# 错误 1：找不到元素
❌ Error: Timeout waiting for selector "input[type='email']"
解决：网站可能更新了页面结构，需要更新选择器

# 错误 2：登录失败
❌ Error: Timeout waiting for selector ".dashboard"
解决：可能需要验证码或双因素认证

# 错误 3：账号密码错误
❌ 登录失败：Invalid credentials
解决：检查 .env 文件中的账号密码
```

### Q2: 如何处理验证码？

**方法 1：手动输入**

脚本会等待 60 秒，你可以手动输入验证码：

```javascript
afterSubmit: async (page) => {
  const hasCaptcha = await page.$('input[name="captcha"]');
  if (hasCaptcha) {
    console.log('⚠️ 需要验证码，请手动输入');
    await page.waitForTimeout(60000); // 等待 60 秒
  }
}
```

**方法 2：使用验证码识别服务**

可以集成第三方验证码识别 API（如 2Captcha）。

### Q3: 如何处理双因素认证（2FA）？

**GitHub 示例：**

```javascript
afterSubmit: async (page) => {
  const has2FA = await page.$('input[name="otp"]');
  if (has2FA) {
    console.log('⚠️ 需要双因素认证，请手动输入验证码');
    await page.waitForTimeout(60000);
  }
}
```

脚本会暂停 60 秒，你可以手动输入 2FA 验证码。

### Q4: 如何处理扫码登录？

**微信公众平台示例：**

```javascript
// 微信使用扫码登录
console.log('📱 请使用微信扫描二维码登录');
await page.waitForSelector('.weui-desktop-account__nickname', {
  timeout: 60000
});
```

脚本会等待你扫码，扫码成功后自动继续。

### Q5: Cookies 有效期多久？

不同网站的 Cookies 有效期不同：

- **Neon**: 约 7 天
- **GitHub**: 约 30 天
- **Supabase**: 约 7 天
- **Vercel**: 约 30 天

过期后需要重新登录。

### Q6: 如何使用保存的 Cookies？

```javascript
const helper = new LoginHelper();
await helper.init();

// 加载 Cookies
const loaded = await helper.loadCookies('./cookies/neon.json');

if (loaded) {
  // 直接访问需要登录的页面
  await helper.page.goto('https://console.neon.tech/projects');
  console.log('✅ 使用 Cookies 登录成功');
} else {
  // Cookies 不存在，需要重新登录
  await helper.login({ ... });
}
```

---

## 🎓 高级用法

### 1. 添加新网站

创建 `tests/logins/yoursite.js`：

```javascript
const LoginHelper = require('../utils/loginHelper');
require('dotenv').config();

async function loginYourSite() {
  const helper = new LoginHelper();

  try {
    await helper.init();

    await helper.login({
      url: 'https://yoursite.com/login',
      usernameSelector: 'input[name="email"]',
      passwordSelector: 'input[name="password"]',
      submitSelector: 'button[type="submit"]',
      username: process.env.YOURSITE_EMAIL,
      password: process.env.YOURSITE_PASSWORD,
      waitForSelector: '.dashboard',

      // 提交前操作（可选）
      beforeSubmit: async (page) => {
        // 例如：勾选"记住我"
        await page.click('input[name="remember"]');
      },

      // 提交后操作（可选）
      afterSubmit: async (page) => {
        // 例如：处理欢迎弹窗
        const popup = await page.$('.welcome-popup');
        if (popup) {
          await page.click('.close-button');
        }
      },
    });

    await helper.saveCookies('./cookies/yoursite.json');
    await helper.screenshot('./screenshots/yoursite-success.png');
    await helper.page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await helper.screenshot('./screenshots/yoursite-error.png');
  } finally {
    await helper.close();
  }
}

if (require.main === module) {
  loginYourSite();
}

module.exports = loginYourSite;
```

### 2. 自定义浏览器选项

```javascript
await helper.init({
  headless: true,      // 无头模式（不显示浏览器）
  slowMo: 500,         // 每个操作延迟 500ms
});
```

### 3. 批量操作

```javascript
// 登录后执行操作
await helper.login({ ... });

// 访问其他页面
await helper.page.goto('https://console.neon.tech/projects');

// 点击按钮
await helper.page.click('button[data-testid="create-project"]');

// 填写表单
await helper.page.fill('input[name="project-name"]', 'My Project');

// 提交
await helper.page.click('button[type="submit"]');
```

### 4. 错误处理

```javascript
try {
  await helper.login({ ... });
} catch (error) {
  if (error.message.includes('Timeout')) {
    console.error('❌ 超时：页面加载太慢或选择器错误');
  } else if (error.message.includes('Invalid credentials')) {
    console.error('❌ 账号密码错误');
  } else {
    console.error('❌ 未知错误:', error.message);
  }

  // 截图保存错误现场
  await helper.screenshot('./screenshots/error.png');
}
```

---

## 🔒 安全建议

1. **不要提交 .env 文件**
   - `.env` 已在 `.gitignore` 中
   - 不要把账号密码提交到 Git

2. **使用强密码**
   - 定期更换密码
   - 不要在多个网站使用相同密码

3. **保护 Cookies 文件**
   - `cookies/*.json` 已在 `.gitignore` 中
   - 不要分享 Cookies 文件

4. **使用专用账号**
   - 建议为自动化创建专用账号
   - 不要使用主账号

5. **定期清理**
   - 定期删除旧的 Cookies
   - 定期删除截图文件

---

## 📊 性能优化

### 1. 无头模式（更快）

```javascript
await helper.init({ headless: true });
```

### 2. 并行登录

```javascript
const sites = [loginNeon, loginGitHub, loginSupabase];

await Promise.all(sites.map(fn => fn()));
```

### 3. 复用 Cookies

```javascript
// 先尝试加载 Cookies
const loaded = await helper.loadCookies('./cookies/neon.json');

if (!loaded) {
  // Cookies 不存在或过期，重新登录
  await helper.login({ ... });
  await helper.saveCookies('./cookies/neon.json');
}
```

---

## 🎉 总结

现在你已经学会了：

- ✅ 配置环境变量
- ✅ 运行自动化登录
- ✅ 保存和使用 Cookies
- ✅ 处理验证码和 2FA
- ✅ 添加新网站
- ✅ 错误处理和调试

**下一步：**

1. 配置你的 `.env` 文件
2. 运行 `npm run login:neon` 测试
3. 查看 `screenshots/` 和 `cookies/` 目录
4. 根据需要添加更多网站

祝你使用愉快！🚀
