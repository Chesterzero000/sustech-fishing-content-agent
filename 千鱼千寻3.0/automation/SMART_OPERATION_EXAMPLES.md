# 智能平台操作 - 使用示例

## 🎯 核心功能

### 1. 链接智能识别

只需提供链接，系统自动识别平台并登录操作。

## 📝 使用示例

### 示例 1: 查看 GitHub 仓库

**用户输入**:
```
帮我看看这个 GitHub 项目 https://github.com/HKUDS/CLI-Anything
```

**系统执行**:
```bash
cd "千鱼千寻3.0/automation"
node smart-operation.js https://github.com/HKUDS/CLI-Anything
```

**输出结果**:
```
🚀 智能平台操作
==========================================

📱 平台: github
🔗 链接: https://github.com/HKUDS/CLI-Anything
⚡ 操作: view

🔐 正在登录 github...
📝 找到已保存的 Cookies，验证中...
✅ Cookies 有效，已自动登录

🌐 访问页面...
👀 提取内容...

📊 提取结果:
{
  "title": "CLI-Anything",
  "description": "Making ALL Software Agent-Native",
  "stars": "1,234",
  "forks": "89",
  "languages": ["Python", "JavaScript"]
}

📸 截图已保存: ./screenshots/github-view-1234567890.png

==========================================
✅ 操作完成
```

### 示例 2: 给 GitHub 仓库点 Star

**用户输入**:
```
给这个仓库点个 Star https://github.com/user/repo
```

**系统执行**:
```bash
node smart-operation.js https://github.com/user/repo --action=star
```

**输出结果**:
```
🚀 智能平台操作
==========================================

📱 平台: github
🔗 链接: https://github.com/user/repo
⚡ 操作: star

✅ 已自动登录
⭐ 点击 Star...
✅ Star 成功

📸 截图已保存: ./screenshots/github-star-1234567890.png

==========================================
✅ 操作完成
```

### 示例 3: 查看小红书笔记

**用户输入**:
```
这个小红书笔记怎么样 https://www.xiaohongshu.com/explore/xxx
```

**系统执行**:
```bash
node smart-operation.js https://www.xiaohongshu.com/explore/xxx
```

**输出结果**:
```
🚀 智能平台操作
==========================================

📱 平台: xiaohongshu
🔗 链接: https://www.xiaohongshu.com/explore/xxx
⚡ 操作: view

✅ 已自动登录
👀 提取内容...

📊 提取结果:
{
  "title": "钓鱼技巧分享",
  "content": "今天分享一些钓鲫鱼的技巧...",
  "likes": "1.2k",
  "collects": "567",
  "comments": "89"
}

==========================================
✅ 操作完成
```

### 示例 4: 批量操作

**用户输入**:
```
帮我给这些 GitHub 仓库都点个 Star:
- https://github.com/user/repo1
- https://github.com/user/repo2
- https://github.com/user/repo3
```

**系统执行**:
```bash
# 批量执行
for url in repo1 repo2 repo3; do
  node smart-operation.js $url --action=star
done
```

**输出结果**:
```
✅ repo1 - Star 成功
✅ repo2 - Star 成功
✅ repo3 - Star 成功

完成！已为 3 个仓库点 Star
```

## 🔧 CLI Anything 风格的自动包装

### 示例 5: 包装任意网站

**用户输入**:
```
帮我把这个网站包装成 CLI https://example.com
```

**系统执行**:
```bash
node cli-anything-wrapper.js --wrap https://example.com
```

**输出结果**:
```
🎁 CLI Anything - 自动包装网站
==========================================

📊 步骤 1: 分析网站结构...
✅ 找到 45 个可交互元素

🔧 步骤 2: 生成 CLI 命令...
✅ 生成 45 个 CLI 命令

💾 配置已保存: ./cli-wrappers/example-com.json

📋 可用命令:
  - click-button-0: 点击按钮: 登录
  - click-button-1: 点击按钮: 注册
  - fill-input-0: 填写输入框: 用户名
  - fill-input-1: 填写输入框: 密码
  - click-link-0: 点击链接: 首页
  ... 还有 40 个命令

==========================================
✅ 包装完成！

使用方法:
  node cli-anything-wrapper.js --execute ./cli-wrappers/example-com.json --command <command-name>
```

### 示例 6: 执行包装后的命令

**用户输入**:
```
执行登录按钮点击
```

**系统执行**:
```bash
node cli-anything-wrapper.js --execute ./cli-wrappers/example-com.json --command click-button-0
```

**输出结果**:
```
⚡ 执行命令: click-button-0
✅ 点击成功: 点击按钮: 登录
📸 截图已保存: ./screenshots/cli-anything-1234567890.png

✅ 执行成功
```

## 🎨 与 Claude Code 集成

### 在对话中直接使用

**对话示例 1**:
```
用户: 帮我看看这个 GitHub 项目 https://github.com/HKUDS/CLI-Anything

Claude: 好的，我来帮你查看这个项目。
[自动执行 smart-operation.js]

这是一个名为 "CLI-Anything" 的项目：
- 描述: Making ALL Software Agent-Native
- Stars: 1,234
- Forks: 89
- 主要语言: Python, JavaScript
- 最近更新: 2 天前

这个项目的目标是将任何软件转换为 AI agent 可控的 CLI 接口。
```

**对话示例 2**:
```
用户: 给这个仓库点个 Star https://github.com/user/repo

Claude: 好的，正在为你点 Star...
[自动执行 smart-operation.js --action=star]

✅ 已成功为仓库点 Star！
```

**对话示例 3**:
```
用户: 这个小红书笔记不错，帮我点个赞 https://www.xiaohongshu.com/explore/xxx

Claude: 好的，正在为你点赞...
[自动执行 smart-operation.js --action=like]

✅ 已成功点赞！
笔记数据:
- 标题: 钓鱼技巧分享
- 点赞数: 1.2k → 1.2k+1
```

## 🔒 安全注意事项

1. **Cookies 安全**
   - Cookies 文件包含敏感信息
   - 不要分享或提交到 Git
   - 定期更新 Cookies

2. **操作频率**
   - 避免频繁操作触发平台限制
   - 添加随机延迟
   - 遵守平台规则

3. **用户确认**
   - 重要操作需要用户确认
   - 记录所有操作日志
   - 支持撤销操作

## 📊 支持的操作

| 平台 | 查看 | 点赞 | 评论 | 收藏 | 下载 | Star | Fork |
|------|------|------|------|------|------|------|------|
| GitHub | ✅ | - | - | - | - | ✅ | ✅ |
| 小红书 | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| 抖音 | ✅ | ✅ | ✅ | - | ✅ | - | - |
| B站 | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |

## 🚀 未来扩展

1. **更多平台支持**
   - 微博
   - 知乎
   - Twitter
   - Instagram

2. **更多操作类型**
   - 关注/取消关注
   - 分享
   - 举报
   - 私信

3. **批量操作**
   - 批量点赞
   - 批量评论
   - 批量下载

4. **定时任务**
   - 定时点赞
   - 定时发布
   - 定时检查

---

**更新时间**: 2026-03-12
**版本**: v3.0.0
