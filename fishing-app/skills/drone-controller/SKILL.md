---
skill: drone-controller
name: Drone Controller (OpenClaw Skill)
version: 0.1.0
open_claw: true
tags:
  - telemetry
  - trajectory
  - control
author: OpenAI Assistant
date: 2026-03-10
description: OpenClaw skill for maritime drone (USV) telemetry, trajectory retrieval and basic control command interface.
---

# Drone Controller Skill

此技能提供对无人船（USV）/ 水上无人遥控艇的遥测数据获取、历史轨迹查询以及基础指令发送能力。实现参考其他技能结构（如 fishing-coach、fish-identifier、catch-tracker），并遵循 Shared API 与 MCP 注册模式。

主要组件
- service.py：服务封装，提供获取实时遥测、历史轨迹、状态与发送指令的方法。
- cli.py：基于 Click 的命令行接口，分组名称为 drone，暴露具体能力。
- mcp_servers/drone_controller_server.py：MCP 服务器实现，注册所有工具。
- SKILL.md：本技能的前端文档，含前置知识、接口说明与使用示例。

API 入口（示意）
- get_telemetry(drone_id)
- get_trajectory(drone_id, start_time, end_time)
- get_status(drone_id)
- send_command(drone_id, command, params)

使用示例
- 通过 CLI:  drone telemetry --drone-id drone-01
- 通过 MCP 调用: 调用 drone.get_telemetry 服务
