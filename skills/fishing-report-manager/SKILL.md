# Fishing Report Manager Skill

> 渔获报告管理 Skill - 提供渔获报告的创建、查询和管理功能

## 📋 功能概述

- 创建渔获报告
- 查询报告列表
- 查询附近的报告
- 统计分析

## 🔌 API 端点

### 创建报告
```
POST /api/v1/fishing-reports
```

### 查询报告
```
GET /api/v1/fishing-reports
```

### 附近报告
```
GET /api/v1/fishing-reports/nearby
```

## 💻 CLI 命令

### 创建报告
```bash
python -m skills.fishing-report-manager.cli create \
  --user-id USER_ID \
  --spot-id SPOT_ID \
  --fish-species "鲫鱼" \
  --weight 1.5 \
  --length 25
```

### 查询报告
```bash
python -m skills.fishing-report-manager.cli list --limit 20
```

### 附近报告
```bash
python -m skills.fishing-report-manager.cli nearby \
  --latitude 22.5 \
  --longitude 114.0 \
  --radius 10
```

## 🔧 MCP 工具

- `create_fishing_report` - 创建渔获报告
- `get_fishing_reports` - 获取报告列表
- `get_nearby_reports` - 获取附近报告
- `get_report_stats` - 获取统计数据

## 📦 安装

```bash
pip install httpx click
```

## 🚀 使用示例

### Python API
```python
from skills.fishing_report_manager import FishingReportService

service = FishingReportService()
result = await service.create_report(
    user_id="user123",
    spot_id="spot456",
    fish_species="鲫鱼",
    weight=1.5,
    length=25
)
```

### MCP Server
```bash
python -m skills.fishing-report-manager.mcp_server
```

## 📝 配置

环境变量：
- `API_BASE_URL` - API 基础 URL
- `INTERNAL_API_KEY` - 内部 API Key

## 🔗 相关 Skills

- catch-tracker - 渔获记录
- spot-manager - 钓点管理
