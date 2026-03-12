@echo off
echo ==========================================
echo GitHub 账号验证
echo ==========================================
echo.

echo 请确认以下信息是否正确：
echo.
echo 邮箱/用户名: hc3571591632@qq.com
echo 密码: hc001024
echo.

echo 建议操作：
echo 1. 在浏览器中手动访问 https://github.com/login
echo 2. 使用上述账号密码尝试登录
echo 3. 确认账号密码是否正确
echo.

set /p continue="账号密码确认无误？(y/n) "
if /i not "%continue%"=="y" (
    echo.
    echo 请先确认账号密码，然后重新运行测试
    pause
    exit /b 1
)

echo.
echo 开始测试登录...
echo.

node test-github.js

pause
