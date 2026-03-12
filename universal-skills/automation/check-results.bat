@echo off
echo ==========================================
echo 检查登录结果
echo ==========================================
echo.

echo 📂 检查 Cookies 文件...
if exist "cookies\neon.json" (
    echo ✅ cookies\neon.json 已创建
) else (
    echo ❌ cookies\neon.json 不存在
)
echo.

echo 📸 检查截图文件...
if exist "screenshots\neon-success.png" (
    echo ✅ screenshots\neon-success.png 已创建
) else if exist "screenshots\neon-error.png" (
    echo ⚠️ screenshots\neon-error.png 已创建（登录失败）
) else (
    echo ❌ 没有找到截图文件
)
echo.

echo 📁 所有 Cookies 文件：
dir /b cookies\*.json 2>nul
echo.

echo 📁 所有截图文件：
dir /b screenshots\*.png 2>nul
echo.

pause
