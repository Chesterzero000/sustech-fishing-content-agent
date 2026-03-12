---
description: 自动化测试套件 - 批量测试所有平台的登录状态和 Cookies 有效性
trigger: 当用户说"测试所有平台"、"批量测试"、"验证登录"、"检查 Cookies"、"运行测试"时使用
---

# 自动化测试套件

这个 skill 帮助用户批量测试所有配置的平台，验证登录状态和自动化配置是否正常。

## 功能特性

- 批量测试所有平台登录
- 验证 Cookies 有效性
- 检查环境配置
- 生成测试报告
- 自动截图保存

## 测试流程

1. **环境检查**
   - 检查 Node.js 和 npm 版本
   - 检查 Playwright 安装状态
   - 验证 `.env` 配置文件
   - 确认必要的目录结构

2. **平台测试**
   - 依次测试每个平台
   - 记录成功/失败状态
   - 保存错误信息和截图
   - 生成详细日志

3. **结果汇总**
   - 统计成功/失败数量
   - 列出需要重新登录的平台
   - 提供修复建议
   - 生成测试报告

## 测试的平台

### ✅ 已实现
- GitHub
- 小红书
- 抖音
- B站

### 🔄 开发中
- 微博
- 知乎

## 使用方法

当用户触发此 skill 时：

### 选项 1: 批量测试所有平台

1. **切换目录**
   ```bash
   cd "千鱼千寻3.0/automation"
   ```

2. **运行批量测试**
   ```bash
   node run-all-tests.js
   ```

3. **等待完成**
   - 测试过程需要 5-10 分钟
   - 会依次测试所有平台
   - 自动生成测试报告

4. **查看报告**
   - JSON 报告：`test-report.json`
   - 文本报告：`test-report.txt`
   - 使用 `type test-report.txt` (Windows) 或 `cat test-report.txt` (Linux/Mac) 查看

### 选项 2: 仅验证 Cookies 有效性

1. **切换目录**
   ```bash
   cd "千鱼千寻3.0/automation"
   ```

2. **运行验证脚本**
   ```bash
   node verify-cookies.js
   ```

3. **查看结果**
   - 显示每个平台的 Cookies 状态
   - 列出需要重新登录的平台
   - 生成验证报告：`cookie-verification-report.json`

## 测试报告示例

```
自动化测试报告
==========================================

测试时间: 2026-03-12 14:30:00

总测试数: 4
成功: 3
失败: 1
总耗时: 45.23秒

详细结果:
------------------------------------------
1. GitHub: ✅ 成功 (12.34秒)
2. 小红书: ❌ 失败 (8.56秒)
   错误: 登录状态已失效
3. 抖音: ✅ 成功 (15.67秒)
4. B站: ✅ 成功 (8.66秒)

需要重新登录的平台:
  - 小红书: 登录状态已失效
```

## 测试报告内容

- 测试时间和环境信息
- 每个平台的测试结果
- 失败原因和错误信息
- Cookies 有效期信息
- 修复建议和下一步操作

## 快速命令参考

```bash
# 批量测试所有平台
node run-all-tests.js

# 仅验证 Cookies 有效性
node verify-cookies.js

# 测试单个平台
node tests/logins/github.js
node tests/logins/xiaohongshu.js
node tests/logins/douyin.js
node tests/logins/bilibili.js

# 查看测试报告
type test-report.txt          # Windows
cat test-report.txt           # Linux/Mac

# 查看 Cookies 验证报告
type cookie-verification-report.json    # Windows
cat cookie-verification-report.json     # Linux/Mac

# 清理旧的截图
rm -rf screenshots/*

# 清理旧的 Cookies
rm -rf cookies/*
```

## 修复失败的平台

根据测试报告，如果某个平台失败：

1. **登录状态已失效**
   ```bash
   # 重新登录该平台
   node tests/logins/{platform}.js
   ```

2. **网络连接问题**
   - 检查网络连接
   - 尝试使用代理
   - 稍后重试

3. **脚本错误**
   - 检查脚本是否存在
   - 更新 Playwright：`npx playwright install`
   - 重新安装依赖：`npm install`

## 最佳实践

- **定期测试**：建议每周运行一次批量测试
- **及时更新**：发现 Cookies 失效立即重新登录
- **保存报告**：测试报告可用于追踪历史状态
- **网络稳定**：在网络稳定时运行测试，避免误报

## 注意事项

- 测试过程可能需要 5-10 分钟
- 某些平台可能需要手动干预
- 建议在网络稳定时运行
- 失败的平台需要重新登录
