#!/bin/bash
# MCP 服务器停止脚本

set -e

LOG_DIR="/var/log/qianyu/mcp"

echo "🛑 停止所有 MCP 服务器..."

# 读取所有 PID 文件并停止进程
for pid_file in "$LOG_DIR"/*.pid; do
    if [ -f "$pid_file" ]; then
        skill=$(basename "$pid_file" .pid)
        pid=$(cat "$pid_file")
        
        if kill -0 "$pid" 2>/dev/null; then
            echo "  停止 $skill (PID: $pid)..."
            kill "$pid"
            rm "$pid_file"
            echo "    ✅ $skill 已停止"
        else
            echo "    ⚠️  $skill 进程不存在 (PID: $pid)"
            rm "$pid_file"
        fi
    fi
done

echo ""
echo "✅ 所有 MCP 服务器已停止！"
