# 千鱼千寻 3.0 - 完整实施计划

> 日期：2026-03-11
> 状态：准备就绪 ✅

---

## 📋 总览

三大核心任务：
1. ✅ 迁移到 PostgreSQL
2. ✅ 配置 MCP Servers
3. ✅ 重构前端到 Next.js 15

---

## 🎯 第一阶段：数据库迁移（1-2 天）

### Day 1：PostgreSQL 设置

**上午**：
```bash
# 1. 注册 Neon PostgreSQL
# 访问 https://neon.tech/
# 创建项目：qianyu-qianxun
# 获取连接字符串

# 2. 执行 Schema
cd 千鱼千寻3.0/deployment
psql "postgresql://user:pass@neon.tech/qianyu" -f schema.sql

# 3. 验证表结构
psql "postgresql://user:pass@neon.tech/qianyu"
\dt  # 列出所有表
\d users  # 查看 users 表
```

**下午**：
```bash
# 4. 测试地理位置查询
psql "postgresql://user:pass@neon.tech/qianyu" << EOF
SELECT
    name,
    ST_Distance(
        location,
        ST_GeogFromText('POINT(113.9547 22.5167)')
    ) / 1000 as distance_km
FROM fishing_spots
WHERE ST_DWithin(
    location,
    ST_GeogFromText('POINT(113.9547 22.5167)'),
    10000
)
ORDER BY distance_km;
EOF

# 5. 测试全文搜索
# 6. 测试向量搜索（如果有数据）
```

### Day 2：数据迁移（如果有旧数据）

```bash
# 从 MySQL 导出数据
mysqldump -u root -p qianyu > qianyu_backup.sql

# 转换并导入（需要手动调整）
# 或使用 pgloader
pgloader mysql://user:pass@localhost/qianyu \
         postgresql://user:pass@neon.tech/qianyu
```

**检查清单**：
- [ ] Neon PostgreSQL 账号已创建
- [ ] 数据库已创建
- [ ] Schema 已执行
- [ ] 所有表已创建（10+ 个）
- [ ] 索引已创建
- [ ] 触发器已创建
- [ ] 测试数据已插入
- [ ] 地理位置查询测试通过
- [ ] 全文搜索测试通过

---

## 🔧 第二阶段：MCP Servers 配置（1 天）

### 上午：安装 MCP Servers

```bash
# 1. 安装 Node.js（如果没有）
node --version  # 应该 >= 18

# 2. 安装核心 MCP Servers
npm install -g @modelcontextprotocol/server-postgres
npm install -g @redis/mcp-server
npm install -g @supabase/mcp-server
npm install -g @modelcontextprotocol/server-github
npm install -g memory-bank-mcp

# 3. 验证安装
which mcp-server-postgres
which redis-mcp-server
```

### 下午：配置和测试

```bash
# 1. 创建配置文件
cd 千鱼千寻3.0
cat > mcp_config.json << 'EOF'
{
  "mcpServers": {
    "postgres": {
      "command": "mcp-server-postgres",
      "args": ["postgresql://user:pass@neon.tech/qianyu"]
    },
    "redis": {
      "command": "redis-mcp-server",
      "args": ["--url", "redis://localhost:6379"]
    }
  }
}
EOF

# 2. 测试 PostgreSQL MCP
mcp-server-postgres "postgresql://user:pass@neon.tech/qianyu"

# 3. 测试查询
# 通过 OpenClaw 或直接测试

# 4. 更新 openclaw.yaml
# 添加 MCP Servers 配置
```

**检查清单**：
- [ ] 所有 MCP Servers 已安装
- [ ] mcp_config.json 已创建
- [ ] 环境变量已配置
- [ ] PostgreSQL MCP 测试通过
- [ ] Redis MCP 测试通过
- [ ] Supabase MCP 测试通过
- [ ] GitHub MCP 测试通过
- [ ] openclaw.yaml 已更新
- [ ] 健康检查脚本已创建

---

## 🎨 第三阶段：Next.js 15 前端（3-5 天）

### Day 1：项目搭建

```bash
# 1. 创建 Next.js 项目
cd 千鱼千寻3.0
npx create-next-app@latest frontend --typescript --tailwind --app --src-dir

# 2. 安装依赖
cd frontend
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install zustand @tanstack/react-query axios
npm install react-hook-form zod @hookform/resolvers
npm install mapbox-gl react-map-gl
npm install recharts date-fns
npm install @supabase/supabase-js

# 3. 安装 shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card dialog form input textarea
```

### Day 2-3：核心页面开发

```bash
# 创建页面结构
mkdir -p src/app/\(main\)/{spots,catches,community,profile}
mkdir -p src/components/{ui,layout,features,shared}
mkdir -p src/lib src/hooks src/stores src/types

# 实现核心页面
# 1. 首页
# 2. 钓点地图
# 3. AI 教练
# 4. 渔获记录
# 5. 钓友圈
```

### Day 4：集成后端 API

```typescript
// 配置 API 客户端
// 实现认证
// 连接 Supabase
// 测试数据获取
```

### Day 5：测试和优化

```bash
# 1. 本地测试
npm run dev

# 2. 构建测试
npm run build
npm run start

# 3. 性能优化
# 4. 响应式设计调整
```

**检查清单**：
- [ ] Next.js 15 项目已创建
- [ ] 所有依赖已安装
- [ ] 项目结构已搭建
- [ ] Supabase 客户端已配置
- [ ] API 客户端已配置
- [ ] 首页已实现
- [ ] 钓点地图已实现
- [ ] AI 教练已实现
- [ ] 渔获记录页面已实现
- [ ] 钓友圈页面已实现
- [ ] 个人中心已实现
- [ ] 认证系统已实现
- [ ] 开发服务器正常运行
- [ ] 生产构建成功

---

## 🚀 第四阶段：集成和部署（2-3 天）

### Day 1：后端更新

```python
# 1. 更新 FastAPI 代码使用 PostgreSQL
# 2. 配置 Prisma ORM
# 3. 更新 API 端点
# 4. 测试 API
```

### Day 2：OpenClaw 集成

```yaml
# 1. 配置 OpenClaw 使用 MCP Servers
# 2. 实现 6 个 Agent
# 3. 配置飞书机器人
# 4. 测试主被动报告
```

### Day 3：部署

```bash
# 前端部署到 Vercel
cd frontend
vercel --prod

# 后端部署到 Railway
cd backend
railway up

# 配置域名和 SSL
# 测试生产环境
```

---

## 📊 时间线总览

```
Week 1:
├── Day 1-2: PostgreSQL 迁移 ✅
├── Day 3: MCP Servers 配置 ✅
└── Day 4-5: Next.js 项目搭建 ✅

Week 2:
├── Day 1-3: 前端页面开发
├── Day 4: 后端更新
└── Day 5: OpenClaw 集成

Week 3:
├── Day 1: 部署和测试
├── Day 2-3: 优化和修复
└── Day 4-5: 上线准备
```

---

## 💰 成本估算

### 开发阶段（免费）
- Neon PostgreSQL: 免费层（3GB）
- Upstash Redis: 免费层（10k 命令/天）
- Supabase: 免费层（500MB 存储）
- Vercel: 免费层（100GB 带宽）
- Railway: 免费层（$5 额度）

**总计**: $0/月

### 生产阶段（小规模）
- Neon PostgreSQL: $19/月（Pro 计划）
- Upstash Redis: $10/月
- Supabase: $25/月（Pro 计划）
- Vercel: $20/月（Pro 计划）
- Railway: $20/月

**总计**: ~$94/月

---

## 🎯 关键里程碑

### 里程碑 1：数据库迁移完成 ✅
- PostgreSQL 设置完成
- Schema 执行成功
- 测试查询通过

### 里程碑 2：MCP 配置完成 ✅
- 所有 MCP Servers 安装
- 配置文件创建
- 测试通过

### 里程碑 3：前端框架搭建 ✅
- Next.js 项目创建
- 依赖安装完成
- 基础结构搭建

### 里程碑 4：核心功能实现（进行中）
- 首页开发
- 钓点地图
- AI 教练
- 数据展示

### 里程碑 5：集成测试（待开始）
- 前后端联调
- OpenClaw 集成
- 飞书机器人测试

### 里程碑 6：生产部署（待开始）
- Vercel 部署
- Railway 部署
- 域名配置
- SSL 证书

---

## 📚 文档索引

### 已完成的文档
1. [PostgreSQL 迁移指南](POSTGRESQL_MIGRATION.md)
2. [MCP Servers 配置指南](MCP_SERVERS_SETUP.md)
3. [Next.js 15 前端指南](NEXTJS_FRONTEND_GUIDE.md)
4. [技术栈优化方案](TECH_STACK_OPTIMIZATION.md)
5. [OpenClaw 员工手册](OPENCLAW_EMPLOYEE_GUIDE.md)
6. [Web 部署指南](WEB_DEPLOYMENT_GUIDE.md)
7. [架构设计文档](ARCHITECTURE_V3_DESIGN.md)

### 代码文件
1. [PostgreSQL Schema](../deployment/schema.sql)
2. [MCP 配置模板](../deployment/mcp_config.json)
3. [Gemini UI Designer Skill](../skills/gemini-ui-designer/)
4. [Web Deployer Skill](../skills/web-deployer/)

---

## ✅ 下一步行动

### 立即可做（今天）

1. **注册 Neon PostgreSQL**
   ```bash
   # 访问 https://neon.tech/
   # 创建账号和项目
   ```

2. **执行 PostgreSQL Schema**
   ```bash
   cd 千鱼千寻3.0/deployment
   psql "your-connection-string" -f schema.sql
   ```

3. **安装 MCP Servers**
   ```bash
   npm install -g @modelcontextprotocol/server-postgres
   npm install -g @redis/mcp-server
   ```

4. **创建 Next.js 项目**
   ```bash
   cd 千鱼千寻3.0
   npx create-next-app@latest frontend --typescript --tailwind --app
   ```

### 本周完成

- [ ] PostgreSQL 迁移完成
- [ ] MCP Servers 配置完成
- [ ] Next.js 项目搭建完成
- [ ] 首页开发完成
- [ ] 钓点地图开发完成

### 下周完成

- [ ] 所有核心页面开发完成
- [ ] 后端 API 更新完成
- [ ] OpenClaw 集成完成
- [ ] 飞书机器人配置完成

### 两周后

- [ ] 前端部署到 Vercel
- [ ] 后端部署到 Railway
- [ ] 域名和 SSL 配置
- [ ] 生产环境测试
- [ ] 正式上线

---

## 🎉 总结

所有准备工作已完成！

**已完成**：
- ✅ 7 份详细文档
- ✅ PostgreSQL Schema 设计
- ✅ MCP Servers 配置方案
- ✅ Next.js 15 前端架构
- ✅ 2 个新 Skills（Gemini UI Designer + Web Deployer）
- ✅ 完整的技术栈优化方案

**准备就绪**：
- ✅ 数据库迁移方案
- ✅ MCP 集成方案
- ✅ 前端重构方案
- ✅ 部署方案
- ✅ 监控方案

**现在可以开始实施了！** 🚀

---

**需要帮助？**
- 查看对应的文档
- 按照检查清单逐步执行
- 遇到问题随时询问

**祝你实施顺利！** 🎣
