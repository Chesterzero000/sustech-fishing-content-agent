---
name: social-manager
type: skill
version: 0.1.0
author: Agent Pro / Sisyphus-Junior
description: OpenClaw Open Code Skill - Backend social features: posts, comments, likes.
tags:
  - social
  - posts
  - comments
  - likes
dependencies: []
---

Overview
- Implements a simple social manager backend with posts, comments and like/unlike capabilities.
- Light-weight data access layer delegates to the project's DB via backend_routes.get_db_connection().
- Exposes a service layer (skills/social-manager/service.py) and a CLI (skills/social-manager/cli.py).
- Provides an MCP server (mcp_servers/social_manager_server.py) to register the available tools.

API surface (service.py)
- create_post(user_id, content, images, spot_id)
- get_posts(user_id, limit, offset)
- delete_post(post_id, user_id)
- add_comment(post_id, user_id, content)
- get_comments(post_id, limit, offset)
- like_post(post_id, user_id)
- unlike_post(post_id, user_id)

CLI surface (cli.py)
- group: social
- Commands: create_post, get_posts, delete_post, add_comment, get_comments, like_post, unlike_post

MCP registration (mcp_servers/social_manager_server.py)
- Registers all CLI service entry points with MCPServerBase for runtime exposure.

Notes
- This skill follows the project conventions used by fishing-coach and catch-tracker for structure and wiring.
