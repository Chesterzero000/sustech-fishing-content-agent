# 千鱼千寻 3.0 - 完整架构设计方案

> 版本：3.0
> 日期：2026-03-11
> 参考：openclaw-cn 项目架构

---

## 1. 项目目标

基于 openclaw-cn 的成功经验，重新设计千鱼千寻项目，实现：

1. **前端**：微信小程序 + Web 应用（UI 由 Gemini API 设计）
2. **后端**：容器化部署的 FastAPI 服务
3. **智能层**：OpenClaw 监控、审核、报告
4. **交互**：飞书作为管理员控制面
5. **自动化**：Agent 自主审核、主被动报告

---

## 2. 整体架构图

```mermaid
flowchart TB
    subgraph "用户层"
        U1[微信小程序用户]
        U2[Web 用户]
        U3[飞书管理员]
    end

    subgraph "前端层"
        MINI[微信小程序<br/>Gemini UI 设计]
        WEB[Web 应用<br/>Gemini UI 设计]
    end

    subgraph "OpenClaw 智能层"
        FEISHU[飞书机器人]
        CLAW[OpenClaw Gateway]

        subgraph "Agent 集群"
            REVIEW[review-agent<br/>内容审核]
            MONITOR[monitor-agent<br/>系统监控]
            REPORT[report-agent<br/>数据报告]
            SKILL_VERIFY[skill-verify-agent<br/>技能验证]
        end

        subgraph "Skills Runtime"
            SKILLS[12+ Skills]
        end
    end

    subgraph "后端层 (容器化)"
        API[FastAPI 服务<br/>Docker]
        INTERNAL[内部 API<br/>认证保护]
    end

    subgraph "数据层 (容器化)"
        MYSQL[(MySQL<br/>Docker)]
        REDIS[(Redis<br/>Docker)]
        NEO4J[(Neo4j<br/>Docker)]
        MINIO[(MinIO<br/>Docker)]
    end

    subgraph "基础设施"
        NGINX[Nginx<br/>反向代理]
        PROMETHEUS[Prometheus<br/>监控]
        GRAFANA[Grafana<br/>可视化]
    end

    U1 --> MINI
    U2 --> WEB
    U3 --> FEISHU

    MINI --> NGINX
    WEB --> NGINX
    NGINX --> API

    FEISHU --> CLAW
    CLAW --> REVIEW
    CLAW --> MONITOR
    CLAW --> REPORT
    CLAW --> SKILL_VERIFY
    CLAW --> SKILLS

    SKILLS --> INTERNAL
    REVIEW --> INTERNAL
    MONITOR --> INTERNAL
    REPORT --> INTERNAL

    INTERNAL --> API
    API --> MYSQL
    API --> REDIS
    API --> NEO4J
    API --> MINIO

    MONITOR --> PROMETHEUS
    PROMETHEUS --> GRAFANA
```

---

## 3. 核心组件设计

### 3.1 前端层（Gemini UI 设计）

#### 微信小程序
- **技术栈**：uni-app / 原生小程序
- **UI 设计**：由 Gemini API 生成设计稿
- **核心页面**：
  1. 首页 - 钓鱼助手入口
  2. 钓点地图 - 附近钓点展示
  3. AI 教练 - 智能问答
  4. 渔获记录 - 记录和统计
  5. 钓友圈 - 社交互动
  6. 我的 - 个人中心

#### Web 应用
- **技术栈**：Next.js / Vue 3
- **UI 设计**：由 Gemini API 生成设计稿
- **响应式设计**：支持桌面和移动端

#### UI 设计流程
```bash
# 1. 使用 Gemini UI Designer Skill 生成设计
fishing-cli ui design-kit \
  --app-name "千鱼千寻" \
  --pages "首页,钓点地图,AI教练,渔获记录,钓友圈,我的" \
  --style "现代简约" \
  --keywords "钓鱼,自然,科技"

# 2. 生成图标系统
fishing-cli ui design-icon --name "钓点" --style "扁平化"
fishing-cli ui design-icon --name "渔获" --style "扁平化"
fishing-cli ui design-icon --name "AI教练" --style "扁平化"

# 3. 生成配色方案
fishing-cli ui color-scheme \
  --theme "钓鱼" \
  --mood "平静、专业、自然"
```

---

### 3.2 后端层（容器化部署）

#### FastAPI 服务
```yaml
# docker-compose.yml
version: '3.8'

services:
  # FastAPI 主服务
  api:
    build: ./backend
    image: qianyu-api:3.0
    container_name: qianyu-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://user:pass@mysql:3306/qianyu
      - REDIS_URL=redis://redis:6379
      - NEO4J_URI=bolt://neo4j:7687
      - MINIO_ENDPOINT=http://minio:9000
    depends_on:
      - mysql
      - redis
      - neo4j
      - minio
    restart: unless-stopped
    networks:
      - qianyu-network

  # MySQL 数据库
  mysql:
    image: mysql:8.0
    container_name: qianyu-mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: qianyu
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    restart: unless-stopped
    networks:
      - qianyu-network

  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: qianyu-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - qianyu-network

  # Neo4j 知识图谱
  neo4j:
    image: neo4j:5.15
    container_name: qianyu-neo4j
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    restart: unless-stopped
    networks:
      - qianyu-network

  # MinIO 对象存储
  minio:
    image: minio/minio
    container_name: qianyu-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    restart: unless-stopped
    networks:
      - qianyu-network

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: qianyu-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - qianyu-network

volumes:
  mysql_data:
  redis_data:
  neo4j_data:
  minio_data:

networks:
  qianyu-network:
    driver: bridge
```

#### API 端点设计
```python
# 前台 API（给小程序/Web 用）
GET  /api/v1/agent                    # AI 问答
GET  /api/v1/weather/{city}           # 天气查询
GET  /api/v1/spots/nearby             # 附近钓点
POST /api/v1/fish/recognize           # 鱼种识别
GET  /api/circle/posts                # 钓友圈帖子
POST /api/circle/posts                # 发布帖子
GET  /api/v1/catch-records/stats      # 渔获统计

# 内部 API（给 OpenClaw 用）
POST /internal/review/content         # 内容审核
POST /internal/stats/daily            # 每日统计
POST /internal/health/check           # 健康检查
GET  /internal/users/active           # 活跃用户
GET  /internal/posts/trending         # 热门帖子
POST /internal/alerts/trigger         # 触发告警
```

---

### 3.3 OpenClaw 智能层

#### 飞书机器人配置
```yaml
# openclaw.yaml - 飞书配置
feishu:
  app_id: "${FEISHU_APP_ID}"
  app_secret: "${FEISHU_APP_SECRET}"

  # 管理员群
  admin_group:
    id: "${FEISHU_ADMIN_GROUP_ID}"
    name: "千鱼千寻管理员群"

  # Webhook
  webhooks:
    alerts: "${FEISHU_WEBHOOK_ALERTS}"
    reports: "${FEISHU_WEBHOOK_REPORTS}"

  # 命令配置
  commands:
    # 系统状态
    - command: "/status"
      description: "查询系统状态"
      agent: "monitor-agent"

    # 今日数据
    - command: "/stats today"
      description: "查询今日数据"
      agent: "report-agent"

    # 手动触发报告
    - command: "/report daily"
      description: "手动触发每日报告"
      agent: "report-agent"

    # 审核队列
    - command: "/review queue"
      description: "查看审核队列"
      agent: "review-agent"

    # 重试审核
    - command: "/review retry <post_id>"
      description: "重试内容审核"
      agent: "review-agent"
```

#### Agent 设计

##### 1. review-agent（内容审核）
```python
# 功能：自动审核用户发布的内容
# 触发：用户发帖/评论时自动触发
# 流程：
1. 接收待审核内容
2. AI 分析内容风险（违规、广告、敏感信息）
3. 低风险 -> 自动通过
4. 高风险 -> 标记并推送飞书管理员群
5. 管理员复核 -> 通过/拒绝
6. 记录审核日志
```

##### 2. monitor-agent（系统监控）
```python
# 功能：监控系统健康状态
# 触发：定时（每 5 分钟）
# 监控指标：
- API 响应时间
- 错误率
- 数据库连接状态
- Redis 状态
- MCP 服务器状态
- 容器健康状态

# 告警规则：
- API 错误率 > 5% -> 飞书告警
- 响应时间 > 2s -> 飞书告警
- 服务宕机 -> 立即飞书告警
```

##### 3. report-agent（数据报告）
```python
# 功能：生成数据报告
# 触发：定时（每日 8:00）或手动触发

# 每日报告内容：
1. 用户数据
   - 新增用户数
   - 活跃用户数
   - 留存率

2. 内容数据
   - 新增帖子数
   - 新增评论数
   - 热门帖子 Top 10

3. 渔获数据
   - 新增渔获记录
   - 热门钓点
   - 热门鱼种

4. 系统健康
   - API 调用量
   - 错误率
   - 响应时间

# 输出：
- 飞书管理员群推送
- 保存到数据库
- 生成 PDF 报告
```

##### 4. skill-verify-agent（技能验证）
```python
# 功能：验证新增的 Skill
# 触发：新 Skill 提交时

# 验证流程：
1. 静态代码检查
   - 语法检查
   - 安全扫描
   - 依赖检查

2. 沙箱测试
   - 隔离环境执行
   - 功能测试
   - 性能测试

3. AI 审核
   - 代码质量评估
   - 功能完整性检查

4. 结果报告
   - 通过 -> 自动部署
   - 失败 -> 推送飞书，人工复核
```

---

### 3.4 监控和告警

#### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
services:
  # Prometheus 监控
  prometheus:
    image: prom/prometheus
    container_name: qianyu-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped
    networks:
      - qianyu-network

  # Grafana 可视化
  grafana:
    image: grafana/grafana
    container_name: qianyu-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus
    restart: unless-stopped
    networks:
      - qianyu-network

  # Node Exporter（主机监控）
  node-exporter:
    image: prom/node-exporter
    container_name: qianyu-node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped
    networks:
      - qianyu-network

volumes:
  prometheus_data:
  grafana_data:
```

#### 监控指标
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  # FastAPI 服务
  - job_name: 'qianyu-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'

  # MCP 服务器
  - job_name: 'mcp-servers'
    static_configs:
      - targets:
        - 'localhost:8001'
        - 'localhost:8002'
        - 'localhost:8003'

  # 主机监控
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # MySQL
  - job_name: 'mysql'
    static_configs:
      - targets: ['mysql:3306']

  # Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

---

## 4. 部署流程

### 4.1 环境准备
```bash
# 1. 安装 Docker 和 Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. 克隆项目
git clone https://github.com/your-org/qianyu-qianxun-3.0.git
cd qianyu-qianxun-3.0

# 3. 配置环境变量
cp .env.example .env
vim .env  # 填写配置
```

### 4.2 启动服务
```bash
# 1. 启动数据层
docker-compose up -d mysql redis neo4j minio

# 2. 等待数据库初始化
sleep 30

# 3. 启动后端服务
docker-compose up -d api

# 4. 启动 Nginx
docker-compose up -d nginx

# 5. 启动监控
docker-compose -f docker-compose.monitoring.yml up -d

# 6. 启动 OpenClaw（在宿主机）
cd openclaw
python -m openclaw start
```

### 4.3 配置飞书机器人
```bash
# 1. 在飞书开放平台创建应用
# 2. 配置事件订阅 URL
https://your-domain.com/feishu/webhook

# 3. 配置机器人权限
- 接收消息
- 发送消息
- 获取群信息

# 4. 测试飞书命令
在管理员群发送：/status
```

---

## 5. 主被动报告机制

### 5.1 被动报告（响应式）
```python
# 飞书命令触发
@feishu_bot.command("/stats today")
async def handle_stats_today(message):
    """查询今日数据"""
    # 1. 调用 report-agent
    report = await report_agent.generate_daily_report()

    # 2. 格式化为飞书卡片
    card = format_feishu_card(report)

    # 3. 回复消息
    await feishu_bot.reply(message, card)

@feishu_bot.command("/review queue")
async def handle_review_queue(message):
    """查看审核队列"""
    # 1. 查询待审核内容
    queue = await review_agent.get_pending_queue()

    # 2. 格式化列表
    card = format_review_queue_card(queue)

    # 3. 回复消息
    await feishu_bot.reply(message, card)
```

### 5.2 主动报告（定时推送）
```python
# 定时任务配置
cron_jobs:
  # 每日报告（主动推送）
  - name: "daily_report"
    schedule: "0 8 * * *"  # 每天 8:00
    agent: "report-agent"
    action: "push_to_feishu"

  # 异常告警（主动推送）
  - name: "alert_monitor"
    schedule: "*/5 * * * *"  # 每 5 分钟
    agent: "monitor-agent"
    action: "check_and_alert"

  # 每周摘要（主动推送）
  - name: "weekly_summary"
    schedule: "0 9 * * 1"  # 每周一 9:00
    agent: "report-agent"
    action: "push_weekly_summary"
```

---

## 6. 自主审核机制

### 6.1 内容审核流程
```mermaid
sequenceDiagram
    participant User as 用户
    participant API as FastAPI
    participant Queue as Redis Queue
    participant Review as review-agent
    participant Feishu as 飞书管理员群

    User->>API: 发布帖子/评论
    API->>API: 基础校验
    API->>Queue: 投递审核任务
    API-->>User: 返回"审核中"

    Review->>Queue: 领取任务
    Review->>Review: AI 内容分析

    alt 低风险（自动通过）
        Review->>API: 标记为"已发布"
        API-->>User: 推送"审核通过"
    else 高风险（需人工）
        Review->>API: 标记为"待复核"
        Review->>Feishu: 推送复核请求
        Feishu-->>Review: 管理员操作
        Review->>API: 更新状态
        API-->>User: 推送结果
    end
```

### 6.2 审核规则
```python
# review_rules.py
REVIEW_RULES = {
    "auto_pass": {
        "risk_score": {"max": 0.3},
        "sensitive_words": {"count": 0},
        "spam_probability": {"max": 0.2}
    },
    "auto_reject": {
        "risk_score": {"min": 0.8},
        "illegal_content": True,
        "spam_probability": {"min": 0.8}
    },
    "manual_review": {
        "risk_score": {"min": 0.3, "max": 0.8},
        "sensitive_words": {"count": {"min": 1, "max": 5}}
    }
}
```

---

## 7. 技术栈总结

### 前端
- **小程序**：uni-app / 原生微信小程序
- **Web**：Next.js / Vue 3
- **UI 设计**：Gemini API

### 后端
- **API 框架**：FastAPI
- **数据库**：MySQL 8.0
- **缓存**：Redis 7
- **知识图谱**：Neo4j 5
- **对象存储**：MinIO
- **容器化**：Docker + Docker Compose

### OpenClaw
- **框架**：OpenClaw
- **Agent**：review-agent, monitor-agent, report-agent, skill-verify-agent
- **Skills**：13 个（12 个现有 + 1 个 Gemini UI Designer）
- **通信**：飞书机器人

### 监控
- **指标收集**：Prometheus
- **可视化**：Grafana
- **日志**：ELK Stack（可选）

### 基础设施
- **反向代理**：Nginx
- **SSL**：Let's Encrypt
- **CI/CD**：GitHub Actions

---

## 8. 实施路线图

### 阶段 1：基础设施（1 周）
- [ ] 配置 Docker 环境
- [ ] 部署数据库容器
- [ ] 配置 Nginx 反向代理
- [ ] 配置 SSL 证书

### 阶段 2：后端服务（2 周）
- [ ] 重构 FastAPI 服务
- [ ] 实现内部 API
- [ ] 容器化部署
- [ ] 性能优化

### 阶段 3：OpenClaw 集成（2 周）
- [ ] 配置飞书机器人
- [ ] 实现 4 个 Agent
- [ ] 配置定时任务
- [ ] 测试主被动报告

### 阶段 4：前端开发（3 周）
- [ ] 使用 Gemini 生成 UI 设计
- [ ] 开发微信小程序
- [ ] 开发 Web 应用
- [ ] 前后端联调

### 阶段 5：监控和优化（1 周）
- [ ] 部署 Prometheus + Grafana
- [ ] 配置告警规则
- [ ] 性能测试
- [ ] 安全审计

### 阶段 6：上线和运营（持续）
- [ ] 灰度发布
- [ ] 用户测试
- [ ] 数据分析
- [ ] 持续优化

---

## 9. 预期效果

### 用户体验
- ✅ 专业的 UI 设计（Gemini 生成）
- ✅ 流畅的交互体验
- ✅ 快速的响应速度（< 500ms）

### 管理效率
- ✅ 飞书一键控制
- ✅ 自动审核（90% 通过率）
- ✅ 每日自动报告
- ✅ 实时监控告警

### 系统稳定性
- ✅ 容器化部署（易扩展）
- ✅ 自动重启（高可用）
- ✅ 完善监控（快速定位问题）
- ✅ 数据备份（安全可靠）

---

## 10. 参考资源

- [openclaw-cn GitHub](https://github.com/jiulingyun/openclaw-cn)
- [OpenClaw 官方文档](https://openclawagent.net/)
- [Gemini API 文档](https://ai.google.dev/docs)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [飞书开放平台](https://open.feishu.cn/)

---

**架构设计完成！准备开始实施！** 🚀
