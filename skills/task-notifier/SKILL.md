---
name: task_notifier
description: 任务完成时播放提示音和显示通知
---

# Task Notifier

任务完成时播放提示音。

## 功能

- 播放提示音（跨平台）
- 显示系统通知
- 自动生成默认音效
- 支持自定义音频文件

## 使用

```bash
# 基本使用
bash scripts/task-complete-notification.sh

# 自定义消息
bash scripts/task-complete-notification.sh "标题" "消息内容"

# 在命令完成后播放
make build && bash scripts/task-complete-notification.sh "构建完成" "项目构建成功"
```

## 集成到脚本

```bash
#!/bin/bash
# 你的任务
echo "执行任务..."
# ...

# 完成后通知
source scripts/task-complete-notification.sh
main "任务完成" "所有操作已完成"
```

## 自定义提示音

```bash
# 复制你的音频文件
cp /path/to/sound.wav ~/.claude-sounds/task-complete.wav

# 或使用 sox 生成
sox -n ~/.claude-sounds/task-complete.wav synth 0.3 sine 1000
```

## 安装依赖

```bash
# Linux
sudo apt-get install sox libsox-fmt-all

# macOS
brew install sox
```
