@echo off
echo ========================================
echo 千鱼千寻 3.0 - PostgreSQL 数据库初始化
echo ========================================
echo.

REM 请在下面填入你的 Neon 连接字符串
set DB_URL=postgresql://neondb_owner:***@ep-muddy-rain-a1a71fxj-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

echo 正在连接到数据库...
echo.

REM 检查是否安装了 psql
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 psql 命令
    echo.
    echo 请选择以下方法之一：
    echo.
    echo 方法 1: 使用 Neon Web SQL 编辑器（推荐）
    echo   1. 在浏览器中打开 Neon 控制台
    echo   2. 点击左侧 "SQL 编辑器"
    echo   3. 复制 schema.sql 的内容并粘贴
    echo   4. 点击 "运行" 按钮
    echo.
    echo 方法 2: 安装 PostgreSQL 客户端
    echo   访问: https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo [成功] 找到 psql 命令
echo.
echo 正在执行 schema.sql...
echo.

psql "%DB_URL%" -f schema.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo [成功] 数据库初始化完成！
    echo ========================================
    echo.
    echo 已创建的表：
    echo   - users (用户表)
    echo   - fishing_spots (钓点表)
    echo   - catch_records (渔获记录表)
    echo   - posts (帖子表)
    echo   - comments (评论表)
    echo   - likes (点赞表)
    echo   - knowledge_nodes (知识节点表)
    echo   - knowledge_relations (知识关系表)
    echo   - user_memories (用户记忆表)
    echo   - audit_logs (审计日志表)
    echo   - system_configs (系统配置表)
    echo.
    echo 下一步：配置 MCP Servers
    echo.
) else (
    echo.
    echo [错误] 数据库初始化失败
    echo 请检查连接字符串是否正确
    echo.
)

pause
