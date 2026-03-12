@echo off
echo ==========================================
echo Playwright 自动化登录 - 快速测试
echo ==========================================
echo.

REM 检查 .env 文件
if not exist ".env" (
    echo ❌ 错误：.env 文件不存在
    echo 请先运行: copy .env.example .env
    echo 然后编辑 .env 文件，填入你的账号密码
    pause
    exit /b 1
)

echo ✅ .env 文件已找到
echo.

REM 检查是否配置了账号
findstr "your-email@example.com" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️ 警告：.env 文件还没有配置
    echo 请编辑 .env 文件，把 your-email@example.com 替换成你的真实邮箱
    echo.
    set /p continue="是否继续测试？(y/n) "
    if /i not "%continue%"=="y" exit /b 1
)

echo 🚀 开始测试登录 Neon PostgreSQL...
echo.

node tests/index.js neon

echo.
echo ==========================================
echo 测试完成！
echo ==========================================
pause
