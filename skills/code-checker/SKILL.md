---
name: code_checker
description: 检查代码质量，发现重复、错误和安全问题
---

# Code Checker

写完代码后自动检查代码规范。

## 功能

- 检测代码重复
- 检查命名规范（camelCase）
- 发现常见错误（console.log, 空 catch 块, == vs ===）
- 分析代码复杂度（函数长度、嵌套深度）
- 扫描安全问题（硬编码密钥、eval）
- 生成 Markdown 报告

## 使用

```bash
# 检查当前目录
bash scripts/check-code-quality.sh

# 检查指定目录
bash scripts/check-code-quality.sh /path/to/code
```

## Git Hook 集成

```bash
# 提交前自动检查
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
bash scripts/check-code-quality.sh .
if [ $? -ne 0 ]; then
    echo "代码检查失败，请修复后再提交"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

## 自定义规则

编辑 `scripts/check-code-quality.sh` 添加检查函数。
