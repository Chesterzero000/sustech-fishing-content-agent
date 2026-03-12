---
description: 智能平台操作 - 自动登录并操作各大平台（GitHub、小红书、抖音、B站等），支持链接解析和内容抓取
trigger: 当用户提供链接、要求查看平台内容、或需要在平台上执行操作时使用
---

# 智能平台操作 Skill

这个 skill 可以自动登录各大平台，并根据用户提供的链接或指令执行操作。

## 核心功能

### 1. 自动登录
- 使用保存的 Cookies 自动登录
- 如果 Cookies 失效，自动触发重新登录
- 支持多平台并发操作

### 2. 链接解析
- 识别链接所属平台
- 自动选择对应的登录方式
- 提取链接中的关键信息

### 3. 内容操作
- 查看帖子/仓库内容
- 获取评论和互动数据
- 执行点赞、评论、关注等操作
- 下载图片、视频等资源

## 支持的平台

### ✅ GitHub
- 查看仓库信息
- 读取 Issues 和 PR
- 查看代码和文档
- Star、Fork、Clone 操作

### ✅ 小红书
- 查看笔记内容
- 获取评论和点赞数
- 下载图片和视频
- 点赞、收藏、评论

### ✅ 抖音
- 查看视频信息
- 获取评论和互动数据
- 下载视频
- 点赞、评论、关注

### ✅ B站
- 查看视频信息
- 获取弹幕和评论
- 下载视频
- 点赞、投币、收藏

## 使用方法

### 方式 1: 提供链接

用户只需提供链接，skill 自动识别并操作：

```
用户: 帮我看看这个 GitHub 仓库 https://github.com/user/repo
助手: [自动登录 GitHub] → [访问仓库] → [提取信息] → [返回结果]

用户: 这个小红书笔记怎么样 https://www.xiaohongshu.com/explore/xxx
助手: [自动登录小红书] → [访问笔记] → [提取内容] → [返回结果]
```

### 方式 2: 执行操作

用户指定要执行的操作：

```
用户: 给这个 GitHub 仓库点个 Star https://github.com/user/repo
助手: [自动登录] → [访问仓库] → [点击 Star] → [确认成功]

用户: 评论这个小红书笔记：很棒的分享！
助手: [自动登录] → [访问笔记] → [发表评论] → [确认成功]
```

## 执行流程

### 1. 链接识别
```javascript
function identifyPlatform(url) {
  if (url.includes('github.com')) return 'github';
  if (url.includes('xiaohongshu.com')) return 'xiaohongshu';
  if (url.includes('douyin.com')) return 'douyin';
  if (url.includes('bilibili.com')) return 'bilibili';
  return 'unknown';
}
```

### 2. Cookies 验证
```javascript
async function verifyCookies(platform) {
  const cookiePath = `./cookies/${platform}.json`;
  if (!fs.existsSync(cookiePath)) {
    return { valid: false, reason: 'Cookies 不存在' };
  }

  // 验证 Cookies 是否有效
  const isValid = await testCookies(platform);
  return { valid: isValid };
}
```

### 3. 自动登录
```javascript
async function autoLogin(platform) {
  const cookiesValid = await verifyCookies(platform);

  if (!cookiesValid.valid) {
    console.log(`Cookies 失效，重新登录 ${platform}...`);
    await triggerLogin(platform);
  }

  return loadCookies(platform);
}
```

### 4. 内容提取
```javascript
async function extractContent(platform, url) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  // 加载 Cookies
  const cookies = await autoLogin(platform);
  await context.addCookies(cookies);

  const page = await context.newPage();
  await page.goto(url);

  // 根据平台提取内容
  const content = await extractByPlatform(platform, page);

  await browser.close();
  return content;
}
```

## 实现步骤

当用户触发此 skill 时：

### 步骤 1: 解析用户输入
```javascript
const input = parseUserInput(userMessage);
// {
//   url: 'https://github.com/user/repo',
//   platform: 'github',
//   action: 'view', // view, star, comment, download
//   params: {}
// }
```

### 步骤 2: 验证登录状态
```bash
cd "千鱼千寻3.0/automation"
node verify-cookies.js --platform github
```

### 步骤 3: 执行操作
```bash
# 查看内容
node smart-operation.js --action view --url <url>

# 执行操作
node smart-operation.js --action star --url <url>
node smart-operation.js --action comment --url <url> --content "评论内容"
```

### 步骤 4: 返回结果
```javascript
{
  success: true,
  platform: 'github',
  action: 'view',
  data: {
    title: '仓库标题',
    description: '仓库描述',
    stars: 1234,
    forks: 567,
    // ... 更多信息
  }
}
```

## 平台特定操作

### GitHub 操作
```javascript
// 查看仓库
await viewRepository(url);

// Star 仓库
await starRepository(url);

// Fork 仓库
await forkRepository(url);

// 查看 Issues
await viewIssues(url);

// 创建 Issue
await createIssue(url, { title, body });
```

### 小红书操作
```javascript
// 查看笔记
await viewNote(url);

// 点赞笔记
await likeNote(url);

// 收藏笔记
await collectNote(url);

// 评论笔记
await commentNote(url, content);

// 下载图片
await downloadImages(url);
```

### 抖音操作
```javascript
// 查看视频
await viewVideo(url);

// 点赞视频
await likeVideo(url);

// 评论视频
await commentVideo(url, content);

// 下载视频
await downloadVideo(url);
```

### B站操作
```javascript
// 查看视频
await viewVideo(url);

// 点赞视频
await likeVideo(url);

// 投币
await coinVideo(url, coins);

// 收藏视频
await collectVideo(url);

// 下载视频
await downloadVideo(url);
```

## 错误处理

### Cookies 失效
```javascript
if (cookiesExpired) {
  console.log('Cookies 已失效，正在重新登录...');
  await reLogin(platform);
  return retry(operation);
}
```

### 网络错误
```javascript
if (networkError) {
  console.log('网络错误，3秒后重试...');
  await sleep(3000);
  return retry(operation, maxRetries - 1);
}
```

### 平台限制
```javascript
if (rateLimited) {
  console.log('操作过于频繁，请稍后再试');
  return { success: false, reason: '平台限制' };
}
```

## 安全考虑

1. **Cookies 加密**
   - 使用加密存储 Cookies
   - 定期更新 Cookies

2. **操作频率限制**
   - 避免频繁操作触发平台限制
   - 添加随机延迟

3. **用户确认**
   - 敏感操作需要用户确认
   - 记录操作日志

## 使用示例

### 示例 1: 查看 GitHub 仓库
```
用户: 帮我看看这个项目 https://github.com/HKUDS/CLI-Anything

助手: 正在查看 GitHub 仓库...
✅ 已登录 GitHub
📦 仓库信息:
- 名称: CLI-Anything
- 描述: Making ALL Software Agent-Native
- Stars: 1.2k
- Forks: 89
- 语言: Python, JavaScript
- 最近更新: 2 天前
```

### 示例 2: 小红书笔记操作
```
用户: 这个小红书笔记不错，帮我点个赞 https://www.xiaohongshu.com/explore/xxx

助手: 正在操作...
✅ 已登录小红书
👍 已点赞
📊 笔记数据:
- 标题: 钓鱼技巧分享
- 点赞数: 1.2k → 1.2k+1
- 收藏数: 567
```

### 示例 3: 批量操作
```
用户: 帮我给这些 GitHub 仓库都点个 Star:
- https://github.com/user/repo1
- https://github.com/user/repo2
- https://github.com/user/repo3

助手: 正在批量操作...
✅ 已登录 GitHub
⭐ repo1 - 成功
⭐ repo2 - 成功
⭐ repo3 - 成功
完成！已为 3 个仓库点 Star
```

## 配置文件

```json
{
  "platforms": {
    "github": {
      "enabled": true,
      "cookiesPath": "./cookies/github.json",
      "operations": ["view", "star", "fork", "issue"]
    },
    "xiaohongshu": {
      "enabled": true,
      "cookiesPath": "./cookies/xiaohongshu.json",
      "operations": ["view", "like", "collect", "comment", "download"]
    },
    "douyin": {
      "enabled": true,
      "cookiesPath": "./cookies/douyin.json",
      "operations": ["view", "like", "comment", "download"]
    },
    "bilibili": {
      "enabled": true,
      "cookiesPath": "./cookies/bilibili.json",
      "operations": ["view", "like", "coin", "collect", "download"]
    }
  },
  "settings": {
    "autoRelogin": true,
    "maxRetries": 3,
    "timeout": 30000,
    "headless": true
  }
}
```

## 注意事项

1. **遵守平台规则**
   - 不要进行恶意操作
   - 遵守平台的使用条款
   - 避免频繁操作

2. **隐私保护**
   - 不要泄露 Cookies
   - 定期更新密码
   - 使用安全的网络环境

3. **操作确认**
   - 重要操作需要用户确认
   - 记录所有操作日志
   - 支持撤销操作

## 扩展功能

### 1. 内容分析
- 使用 AI 分析内容质量
- 提取关键信息
- 生成摘要

### 2. 批量操作
- 支持批量点赞、评论
- 支持批量下载
- 支持定时任务

### 3. 数据导出
- 导出为 JSON、CSV
- 生成报告
- 数据可视化
