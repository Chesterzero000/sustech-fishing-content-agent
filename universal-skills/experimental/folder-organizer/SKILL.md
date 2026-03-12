---
name: folder_organizer
description: 自动整理文件夹，创建标准目录结构，清理临时文件
---

# Folder Organizer

每 24 小时自动整理文件夹。

## 功能

- 创建标准目录结构（docs, scripts, configs, plugins, temp, archive, projects）
- 清理临时文件（*.tmp, *.bak, *.log 等）
- 整理文档文件到 docs/
- 整理脚本文件到 scripts/
- 整理配置文件到 configs/
- 生成整理报告

## 使用

```bash
# 预览模式
DRY_RUN=true bash scripts/organize-folders.sh

# 执行整理
bash scripts/organize-folders.sh

# 指定目录
bash scripts/organize-folders.sh /path/to/folder
```

## 定时任务

```bash
# 每天凌晨 2 点执行
crontab -e
# 添加: 0 2 * * * bash ~/Desktop/寻鱼器/小龙虾/scripts/organize-folders.sh
```

## 配置

编辑 `scripts/organize-folders.sh` 自定义规则：
- 文档类型：doc_extensions
- 临时文件：temp_patterns
- 目录结构：dirs
