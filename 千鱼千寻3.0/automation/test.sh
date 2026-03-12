#!/bin/bash

echo "=========================================="
echo "Playwright 自动化登录 - 快速测试"
echo "=========================================="
echo ""

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 错误：.env 文件不存在"
    echo "请先运行: cp .env.example .env"
    echo "然后编辑 .env 文件，填入你的账号密码"
    exit 1
fi

echo "✅ .env 文件已找到"
echo ""

# 检查是否配置了 Neon 账号
if grep -q "your-email@example.com" .env; then
    echo "⚠️ 警告：.env 文件还没有配置"
    echo "请编辑 .env 文件，把 your-email@example.com 替换成你的真实邮箱"
    echo ""
    read -p "是否继续测试？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🚀 开始测试登录 Neon PostgreSQL..."
echo ""

node tests/index.js neon

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
