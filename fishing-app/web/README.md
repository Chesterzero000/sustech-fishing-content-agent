# 千鱼千寻 2.0 Web 端

## 📋 项目说明

千鱼千寻 2.0 的 Web 端界面，提供友好的图形化界面访问所有钓鱼助手功能。

## 🎯 功能特性

### 7大核心功能

1. **🎓 钓鱼教练** - AI 问答系统
2. **🐟 鱼类识别** - 图片识别鱼种
3. **🌤️ 天气顾问** - 天气查询和钓鱼指数
4. **📍 钓点管理** - 钓点搜索和管理
5. **📊 渔获记录** - 记录和统计分析
6. **💬 钓友圈** - 社交互动
7. **🚁 无人船控制** - 遥测数据查询

## 🚀 快速开始

### 1. 安装依赖

```bash
cd web
pip install fastapi uvicorn python-multipart
```

### 2. 启动服务

```bash
# 启动 Web API 服务
python api.py
```

服务将在 `http://localhost:8000` 启动

### 3. 访问界面

在浏览器中打开：
```
http://localhost:8000
```

## 📁 文件结构

```
web/
├── index.html          # 前端页面
├── api.py              # FastAPI 后端
└── README.md          # 本文档
```

## 🎨 界面预览

### 首页
- 7个功能卡片
- 渐变紫色背景
- 响应式设计

### 功能模态框
- 钓鱼教练：输入问题，获取 AI 回答
- 鱼类识别：上传图片，识别鱼种
- 天气顾问：查询天气和钓鱼指数
- 其他功能...

## 🔧 API 端点

### 钓鱼教练
```
POST /api/coach/ask
GET  /api/coach/history
```

### 鱼类识别
```
POST /api/fish/identify
GET  /api/fish/tips
```

### 天气顾问
```
GET /api/weather/current
GET /api/weather/forecast
```

### 钓点管理
```
GET /api/spots/nearby
GET /api/spots/search
GET /api/spots/{spot_id}
```

### 渔获记录
```
POST /api/catch/log
GET  /api/catch/list
GET  /api/catch/stats
```

### 社交功能
```
GET /api/social/posts
GET /api/social/trending
```

### 无人船控制
```
GET /api/drone/status
GET /api/drone/history
```

## 🔌 集成实际服务

当前 API 返回的是模拟数据。要集成实际服务，需要：

### 1. 修改 api.py

```python
# 取消注释实际服务调用
from skills.fishing_coach.service import FishingCoachService
from skills.fish_identifier.service import FishIdentifierService
# ... 其他服务

# 在对应的端点中调用实际服务
@app.post("/api/coach/ask")
async def coach_ask(question: CoachQuestion):
    service = FishingCoachService()
    answer = service.ask_question(question.question, question.user_id)
    return {"success": True, "answer": answer}
```

### 2. 配置环境变量

确保 `.env` 文件配置正确：
```env
NEO4J_URI=bolt://192.168.1.79:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=fishing_hero_2025
```

### 3. 启动依赖服务

```bash
# 启动 Neo4j
# 启动 ChromaDB
# 其他必要的服务...
```

## 📱 响应式设计

- ✅ 桌面端（1200px+）
- ✅ 平板端（768px - 1200px）
- ✅ 移动端（< 768px）

## 🎨 自定义样式

### 修改主题色

在 `index.html` 中修改 CSS 变量：

```css
/* 渐变背景 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 按钮颜色 */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 修改布局

```css
/* 卡片网格 */
.skills-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
}
```

## 🔒 安全注意事项

1. **CORS 配置**
   - 生产环境需要限制允许的域名
   - 当前配置为 `allow_origins=["*"]`（仅用于开发）

2. **API 认证**
   - 建议添加 JWT 或 OAuth 认证
   - 保护敏感端点

3. **输入验证**
   - 前端和后端都需要验证用户输入
   - 防止 SQL 注入、XSS 等攻击

4. **文件上传**
   - 限制文件大小和类型
   - 扫描上传的文件

## 🚀 部署

### 开发环境
```bash
python api.py
```

### 生产环境

使用 Gunicorn + Nginx：

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Nginx 配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 性能优化

1. **静态资源缓存**
   - 使用 CDN
   - 启用浏览器缓存

2. **API 响应缓存**
   - Redis 缓存热门数据
   - 减少数据库查询

3. **图片优化**
   - 压缩上传的图片
   - 使用 WebP 格式

## 🐛 常见问题

### Q1: 无法访问 API
**A:** 检查防火墙设置，确保 8000 端口开放

### Q2: CORS 错误
**A:** 检查 API 的 CORS 配置，确保允许前端域名

### Q3: 图片上传失败
**A:** 检查文件大小限制和格式要求

## 📝 待完成功能

- [ ] 用户登录和注册
- [ ] 个人中心
- [ ] 数据可视化图表
- [ ] 实时通知
- [ ] 离线支持（PWA）
- [ ] 多语言支持

## 🔮 未来计划

1. **移动端优化**
   - 优化触摸交互
   - 添加手势支持

2. **实时功能**
   - WebSocket 支持
   - 实时位置共享

3. **社交功能增强**
   - 私信功能
   - 钓友推荐

4. **数据分析**
   - 钓鱼数据可视化
   - 趋势分析

---

**更新时间**: 2026-03-12
**版本**: v2.0.0
**作者**: Agent_Pro Team
