---
name: permission_manager
description: 管理终端权限，配置 sudo 和管理员访问
---

# Permission Manager

配置终端控制权限。

## 功能

- 智能 sudo 包装器（自动检测环境）
- Git Bash 管理员快捷方式
- WSL2 sudo 配置
- 权限测试工具

## 使用

### 智能 Sudo

```bash
# 自动检测环境并提升权限
bash scripts/smart-sudo.sh <命令>

# 示例
bash scripts/smart-sudo.sh apt-get update
```

### 测试权限

```bash
bash scripts/test-sudo.sh
```

### Git Bash 管理员快捷方式

```powershell
# 在 PowerShell 中运行
powershell.exe -Command "
\$gitBashPath = 'C:\Program Files\Git\git-bash.exe'
\$desktopPath = [Environment]::GetFolderPath('Desktop')
\$shortcutPath = Join-Path \$desktopPath 'Git Bash (Admin).lnk'
\$WScriptShell = New-Object -ComObject WScript.Shell
\$Shortcut = \$WScriptShell.CreateShortcut(\$shortcutPath)
\$Shortcut.TargetPath = \$gitBashPath
\$Shortcut.Save()
\$bytes = [System.IO.File]::ReadAllBytes(\$shortcutPath)
\$bytes[0x15] = \$bytes[0x15] -bor 0x20
[System.IO.File]::WriteAllBytes(\$shortcutPath, \$bytes)
"
```

### WSL2 Sudo 配置

```bash
# 在 WSL2 中
sudo visudo
# 添加: your_username ALL=(ALL) NOPASSWD: ALL
```

## 环境支持

- Git Bash (MinGW) - 使用 PowerShell 提升权限
- WSL2 / Linux - 使用 sudo
- macOS - 使用 sudo
