---
description: GitHub 手动辅助登录 - 自动填写账号密码，手动完成验证，保存登录状态
trigger: 当用户说"登录 GitHub"、"GitHub 登录"、"保存 GitHub Cookies"、"测试 GitHub"时使用
---

# GitHub 手动辅助登录

这个 skill 帮助用户完成 GitHub 登录并保存登录状态（Cookies），用于后续的自动化操作。

## 工作流程

1. **检查环境配置**
   - 确认 `.env` 文件中的 GitHub 账号密码配置
   - 确认 Playwright 已安装

2. **运行手动辅助登录脚本**
   - 自动打开浏览器
   - 自动填写账号密码
   - 等待用户手动完成验证（验证码、双因素认证等）
   - 自动保存 Cookies 和截图

3. **验证登录状态**
   - 检查是否成功保存 Cookies
   - 确认截图已生成

## 使用场景

- 首次设置 GitHub 自动化
- Cookies 过期需要重新登录
- 测试 GitHub 账号是否正常
- 绕过 GitHub 的自动化检测

## 注意事项

- 脚本会等待 120 秒供用户手动操作
- 需要用户在浏览器窗口中完成验证
- 成功后会保存 Cookies 到 `千鱼千寻3.0/automation/cookies/github.json`
- 保存的 Cookies 可用于后续自动登录

## 执行步骤

当用户触发此 skill 时：

1. **检查环境**
   ```bash
   cd "千鱼千寻3.0/automation"
   ```

2. **运行登录脚本**
   ```bash
   node manual-login.js
   ```

3. **提示用户**
   - 告知用户注意浏览器窗口
   - 说明需要手动完成验证码
   - 提醒等待时间为 120 秒

4. **验证结果**
   - 检查 `cookies/github.json` 是否生成
   - 检查 `screenshots/github-success.png` 是否存在
   - 告知用户登录状态

5. **后续操作**
   - 建议运行 `node verify-cookies.js` 验证 Cookies
   - 说明 Cookies 有效期约 30 天
   - 提示可以使用 Cookies 进行自动登录

## 常见问题处理

- **错误：Incorrect username or password**
  - 检查 `.env` 文件中的邮箱和密码
  - 确认邮箱是 `@163.com` 而不是 `@qq.com`

- **错误：ERR_CONNECTION_CLOSED**
  - 网络连接问题，建议检查网络
  - 可能需要代理访问 GitHub

- **错误：You can't perform that action at this time**
  - GitHub 检测到自动化行为
  - 使用手动辅助登录可以绕过检测
