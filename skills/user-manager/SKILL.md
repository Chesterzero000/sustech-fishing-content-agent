# User Manager Skill

> 用户管理 - 认证和资料管理

## 功能
- 微信登录
- 用户资料管理
- 钓鱼记录

## API 端点
- POST /api/v1/wx/login
- GET /api/v1/user/{user_id}/profile
- POST /api/v1/user/{user_id}/fishing-record

## CLI 命令
```bash
python -m skills.user-manager.cli login --code WX_CODE
python -m skills.user-manager.cli profile --user-id USER_ID
```

## MCP 工具
- wx_login
- get_user_profile
