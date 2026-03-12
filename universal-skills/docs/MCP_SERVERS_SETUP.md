# MCP Servers 配置指南

> 日期：2026-03-11
> Model Context Protocol 服务器配置

---

## 📦 核心 MCP Servers 安装

### 1. PostgreSQL MCP Server

```bash
# 安装官方 PostgreSQL MCP Server
npm install -g @modelcontextprotocol/server-postgres

# 或使用更强大的版本
npm install -g crystaldba/postgres-mcp
```

**配置**：
```json
{
  "mcpServers": {
    "postgres": {
      "command": "mcp-server-postgres",
      "args": [
        "postgresql://user:password@ep-xxx.neon.tech/qianyu?sslmode=require"
      ],
      "env": {
        "POSTGRES_READ_ONLY": "false"
      }
    }
  }
}
```

### 2. Redis MCP Server

```bash
# 安装 Redis MCP Server
npm install -g @redis/mcp-server
```

**配置**：
```json
{
  "mcpServers": {
    "redis": {
      "command": "redis-mcp-server",
      "args": [
        "--url", "redis://default:password@redis.upstash.io:6379"
      ]
    }
  }
}
```

### 3. Supabase MCP Server

```bash
# 安装 Supabase MCP Server
npm install -g @supabase/mcp-server
```

**配置**：
```json
{
  "mcpServers": {
    "supabase": {
      "command": "supabase-mcp-server",
      "env": {
        "SUPABASE_URL": "https://xxx.supabase.co",
        "SUPABASE_KEY": "your-anon-key"
      }
    }
  }
}
```

### 4. GitHub MCP Server

```bash
# 安装 GitHub MCP Server
npm install -g @modelcontextprotocol/server-github
```

**配置**：
```json
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

### 5. Memory Bank MCP Server

```bash
# 安装 Memory Bank MCP Server
npm install -g memory-bank-mcp
```

**配置**：
```json
{
  "mcpServers": {
    "memory-bank": {
      "command": "memory-bank-mcp",
      "args": [
        "--storage-path", "./data/memory"
      ]
    }
  }
}
```

---

## 🔧 完整的 MCP 配置文件

创建 `mcp_config.json`：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "mcp-server-postgres",
      "args": [
        "${POSTGRES_CONNECTION_STRING}"
      ],
      "env": {
        "POSTGRES_READ_ONLY": "false"
      }
    },
    "redis": {
      "command": "redis-mcp-server",
      "args": [
        "--url", "${REDIS_URL}"
      ]
    },
    "supabase": {
      "command": "supabase-mcp-server",
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_ANON_KEY}"
      }
    },
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "memory-bank": {
      "command": "memory-bank-mcp",
      "args": [
        "--storage-path", "./data/memory"
      ]
    },
    "brave-search": {
      "command": "mcp-server-brave-search",
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

---

## 🚀 OpenClaw 集成

更新 `openclaw.yaml`：

```yaml
# OpenClaw 配置文件
name: "千鱼千寻 OpenClaw"
version: "3.0.0"

# MCP Servers 配置
mcp:
  enabled: true
  config_file: "./mcp_config.json"

  servers:
    # 数据库访问
    - name: "postgres"
      enabled: true
      description: "PostgreSQL 数据库访问"
      tools:
        - query_database
        - get_schema
        - execute_sql

    # 缓存管理
    - name: "redis"
      enabled: true
      description: "Redis 缓存管理"
      tools:
        - get_cache
        - set_cache
        - delete_cache

    # 后端服务
    - name: "supabase"
      enabled: true
      description: "Supabase 后端服务"
      tools:
        - query_table
        - insert_row
        - update_row
        - delete_row
        - upload_file
        - get_file_url

    # 代码管理
    - name: "github"
      enabled: true
      description: "GitHub 代码管理"
      tools:
        - create_issue
        - create_pr
        - get_repo_info
        - search_code

    # 用户记忆
    - name: "memory-bank"
      enabled: true
      description: "用户记忆管理"
      tools:
        - store_memory
        - retrieve_memory
        - search_memory

    # 网页搜索
    - name: "brave-search"
      enabled: true
      description: "网页搜索"
      tools:
        - web_search
        - local_search

# Agent 配置
agents:
  # 数据分析师（使用 PostgreSQL MCP）
  - name: "report-agent"
    description: "数据报告生成"
    mcp_servers:
      - postgres
      - redis
    tools:
      - query_database
      - get_cache
      - set_cache

  # 内容审核员（使用 Memory Bank MCP）
  - name: "review-agent"
    description: "内容审核"
    mcp_servers:
      - postgres
      - memory-bank
    tools:
      - query_database
      - retrieve_memory

  # 系统监控员（使用 Redis MCP）
  - name: "monitor-agent"
    description: "系统监控"
    mcp_servers:
      - redis
      - postgres
    tools:
      - get_cache
      - query_database

  # 技能验证员（使用 GitHub MCP）
  - name: "skill-verify-agent"
    description: "技能验证"
    mcp_servers:
      - github
      - postgres
    tools:
      - get_repo_info
        - search_code
      - query_database
```

---

## 🧪 测试 MCP Servers

### 测试 PostgreSQL MCP

```bash
# 启动 MCP Server
mcp-server-postgres "postgresql://user:pass@neon.tech/qianyu"

# 测试查询（通过 OpenClaw）
openclaw mcp call postgres query_database \
  --query "SELECT * FROM users LIMIT 5"
```

### 测试 Redis MCP

```bash
# 启动 MCP Server
redis-mcp-server --url "redis://localhost:6379"

# 测试缓存
openclaw mcp call redis set_cache \
  --key "test_key" \
  --value "test_value"

openclaw mcp call redis get_cache \
  --key "test_key"
```

### 测试 Supabase MCP

```bash
# 启动 MCP Server
supabase-mcp-server

# 测试查询
openclaw mcp call supabase query_table \
  --table "users" \
  --limit 5
```

---

## 📝 环境变量配置

创建 `.env` 文件：

```bash
# PostgreSQL (Neon)
POSTGRES_CONNECTION_STRING=postgresql://user:password@ep-xxx.neon.tech/qianyu?sslmode=require

# Redis (Upstash)
REDIS_URL=redis://default:password@redis.upstash.io:6379

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# GitHub
GITHUB_TOKEN=ghp_your_token_here

# Brave Search
BRAVE_API_KEY=your-brave-api-key

# Gemini
GEMINI_API_KEY=your-gemini-api-key
```

---

## 🔒 安全配置

### 1. 只读 PostgreSQL 连接（给 MCP 用）

```sql
-- 创建只读用户
CREATE ROLE mcp_readonly WITH LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE qianyu TO mcp_readonly;
GRANT USAGE ON SCHEMA public TO mcp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
```

**MCP 配置**：
```json
{
  "mcpServers": {
    "postgres-readonly": {
      "command": "mcp-server-postgres",
      "args": [
        "postgresql://mcp_readonly:password@neon.tech/qianyu"
      ],
      "env": {
        "POSTGRES_READ_ONLY": "true"
      }
    }
  }
}
```

### 2. Redis 访问控制

```bash
# 创建 Redis ACL
redis-cli ACL SETUSER mcp_user on >password ~* +@read -@write
```

---

## 📊 MCP Server 监控

创建监控脚本 `mcp_health_check.py`：

```python
#!/usr/bin/env python3
"""
MCP Servers 健康检查
"""
import subprocess
import json
from datetime import datetime

MCP_SERVERS = [
    "postgres",
    "redis",
    "supabase",
    "github",
    "memory-bank"
]

def check_mcp_server(server_name):
    """检查 MCP Server 状态"""
    try:
        result = subprocess.run(
            ["openclaw", "mcp", "ping", server_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking {server_name}: {e}")
        return False

def main():
    print(f"🔍 MCP Servers 健康检查 - {datetime.now()}\n")

    results = {}
    for server in MCP_SERVERS:
        status = check_mcp_server(server)
        results[server] = "✅ 正常" if status else "❌ 异常"
        print(f"{server}: {results[server]}")

    # 保存结果
    with open("mcp_health.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)

if __name__ == "__main__":
    main()
```

---

## 🎯 使用示例

### 示例 1：通过 MCP 查询数据库

```python
# 使用 OpenClaw 调用 PostgreSQL MCP
from openclaw import OpenClaw

claw = OpenClaw()

# 查询用户
users = claw.mcp.call("postgres", "query_database", {
    "query": "SELECT * FROM users WHERE is_active = true LIMIT 10"
})

print(users)
```

### 示例 2：通过 MCP 管理缓存

```python
# 设置缓存
claw.mcp.call("redis", "set_cache", {
    "key": "user:123:profile",
    "value": json.dumps(user_data),
    "ttl": 3600
})

# 获取缓存
cached_data = claw.mcp.call("redis", "get_cache", {
    "key": "user:123:profile"
})
```

### 示例 3：通过 MCP 搜索代码

```python
# 搜索 GitHub 代码
results = claw.mcp.call("github", "search_code", {
    "query": "fishing skill",
    "repo": "your-org/qianyu-qianxun"
})
```

---

## ✅ 配置检查清单

- [ ] 所有 MCP Servers 已安装
- [ ] `mcp_config.json` 已创建
- [ ] 环境变量已配置
- [ ] `openclaw.yaml` 已更新
- [ ] PostgreSQL 连接测试通过
- [ ] Redis 连接测试通过
- [ ] Supabase 连接测试通过
- [ ] GitHub 连接测试通过
- [ ] Memory Bank 测试通过
- [ ] 健康检查脚本已创建
- [ ] 安全配置已完成

---

**MCP Servers 配置完成！** 🎉
