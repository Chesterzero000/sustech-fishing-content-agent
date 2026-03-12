#!/bin/bash
# MCP 服务器启动脚本 - 启动所有 12 个 MCP 服务器

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$BASE_DIR/../skills"
LOG_DIR="/var/log/qianyu/mcp"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "🚀 启动所有 MCP 服务器..."

# Skills 列表
SKILLS=(
    "fishing-coach:8001"
    "weather-advisor:8002"
    "spot-manager:8003"
    "fish-identifier:8004"
    "catch-tracker:8005"
    "social-manager:8006"
    "drone-controller:8007"
    "fishing-report-manager:8008"
    "angler-radar:8009"
    "user-manager:8010"
    "persona-manager:8011"
    "feedback-manager:8012"
)

# 启动每个 MCP 服务器
for skill_port in "${SKILLS[@]}"; do
    IFS=':' read -r skill port <<< "$skill_port"
    
    echo "  启动 $skill (端口 $port)..."
    
    # 设置环境变量
    export MCP_PORT=$port
    
    # 启动 MCP 服务器（后台运行）
    nohup python -m skills.${skill}.mcp_server \
        > "$LOG_DIR/${skill}.log" 2>&1 &
    
    # 保存 PID
    echo $! > "$LOG_DIR/${skill}.pid"
    
    echo "    ✅ $skill 已启动 (PID: $!)"
done

echo ""
echo "✅ 所有 MCP 服务器已启动！"
echo "📋 日志目录: $LOG_DIR"
echo ""
echo "查看日志: tail -f $LOG_DIR/*.log"
echo "停止服务: ./stop_all.sh"
