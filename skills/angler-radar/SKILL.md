# Angler Radar Skill

> 钓友雷达 - 位置共享和附近钓友查询

## 功能
- 更新用户位置
- 查询附近钓友
- 位置共享设置

## API 端点
- POST /api/v1/angler-radar/location
- GET /api/v1/angler-radar/nearby
- POST /api/v1/angler-radar/sharing

## CLI 命令
```bash
python -m skills.angler-radar.cli update-location --user-id USER --latitude 22.5 --longitude 114.0
python -m skills.angler-radar.cli nearby --latitude 22.5 --longitude 114.0 --radius 5
```

## MCP 工具
- update_angler_location
- get_nearby_anglers
