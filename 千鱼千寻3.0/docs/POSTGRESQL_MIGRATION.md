# PostgreSQL 数据库迁移指南

> 日期：2026-03-11
> 从 MySQL + Neo4j 迁移到 PostgreSQL

---

## 📋 迁移前准备

### 1. 注册 Neon PostgreSQL（推荐）

```bash
# 访问 https://neon.tech/
# 1. 注册账号（GitHub 登录）
# 2. 创建项目：qianyu-qianxun
# 3. 选择区域：Asia Pacific (Singapore)
# 4. 获取连接字符串
```

**连接字符串示例**：
```
postgresql://user:password@ep-xxx.ap-southeast-1.aws.neon.tech/qianyu?sslmode=require
```

### 2. 安装工具

```bash
# 安装 PostgreSQL 客户端
# Windows
choco install postgresql

# 安装 Prisma（ORM）
npm install -g prisma

# 安装数据迁移工具
pip install pgloader  # MySQL -> PostgreSQL
```

---

## 🗄️ 数据库设计

### PostgreSQL Schema 设计

```sql
-- ============================================
-- 千鱼千寻 PostgreSQL Schema
-- ============================================

-- 启用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID 生成
CREATE EXTENSION IF NOT EXISTS "postgis";        -- 地理位置
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- 模糊搜索
CREATE EXTENSION IF NOT EXISTS "vector";         -- 向量搜索

-- ============================================
-- 1. 用户系统
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(100),
    avatar_url TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- 用户偏好（JSON）
    preferences JSONB DEFAULT '{}',

    -- 全文搜索索引
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('chinese', coalesce(nickname, ''))
    ) STORED
);

CREATE INDEX idx_users_openid ON users(openid);
CREATE INDEX idx_users_search ON users USING gin(search_vector);

-- ============================================
-- 2. 钓点系统
-- ============================================

CREATE TABLE fishing_spots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,

    -- 地理位置（PostGIS）
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    district VARCHAR(50),

    -- 钓点信息
    fish_species TEXT[],  -- 鱼种数组
    facilities TEXT[],    -- 设施数组
    price_range VARCHAR(50),
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),

    -- 评分
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,

    -- 元数据
    images TEXT[],
    tags TEXT[],
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT false,

    -- 全文搜索
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('chinese',
            coalesce(name, '') || ' ' ||
            coalesce(description, '') || ' ' ||
            coalesce(address, '')
        )
    ) STORED
);

-- 地理位置索引（重要！）
CREATE INDEX idx_spots_location ON fishing_spots USING gist(location);
CREATE INDEX idx_spots_search ON fishing_spots USING gin(search_vector);
CREATE INDEX idx_spots_city ON fishing_spots(city);

-- ============================================
-- 3. 渔获记录
-- ============================================

CREATE TABLE catch_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    spot_id UUID REFERENCES fishing_spots(id),

    -- 渔获信息
    fish_species VARCHAR(100) NOT NULL,
    weight DECIMAL(10,2),  -- kg
    length DECIMAL(10,2),  -- cm
    quantity INTEGER DEFAULT 1,

    -- 钓鱼详情
    catch_time TIMESTAMP NOT NULL,
    weather_condition VARCHAR(50),
    temperature DECIMAL(5,2),
    bait_used VARCHAR(100),
    technique VARCHAR(100),

    -- 媒体
    images TEXT[],
    notes TEXT,

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_catch_user ON catch_records(user_id);
CREATE INDEX idx_catch_spot ON catch_records(spot_id);
CREATE INDEX idx_catch_time ON catch_records(catch_time DESC);
CREATE INDEX idx_catch_species ON catch_records(fish_species);

-- ============================================
-- 4. 钓友圈（社交）
-- ============================================

CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- 内容
    content TEXT NOT NULL,
    images TEXT[],
    video_url TEXT,

    -- 关联
    spot_id UUID REFERENCES fishing_spots(id),
    catch_id UUID REFERENCES catch_records(id),

    -- 统计
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,

    -- 状态
    status VARCHAR(20) DEFAULT 'published',  -- draft, published, hidden, deleted
    is_pinned BOOLEAN DEFAULT false,

    -- 审核
    review_status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected
    review_note TEXT,
    reviewed_at TIMESTAMP,
    reviewed_by UUID REFERENCES users(id),

    -- 元数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 全文搜索
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('chinese', coalesce(content, ''))
    ) STORED
);

CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status, created_at DESC);
CREATE INDEX idx_posts_search ON posts USING gin(search_vector);

-- 评论表
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES comments(id),  -- 回复评论

    content TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post ON comments(post_id, created_at);
CREATE INDEX idx_comments_user ON comments(user_id);

-- 点赞表
CREATE TABLE likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL,  -- post, comment
    target_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, target_type, target_id)
);

CREATE INDEX idx_likes_target ON likes(target_type, target_id);

-- ============================================
-- 5. AI 知识库（替代 Neo4j）
-- ============================================

CREATE TABLE knowledge_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_type VARCHAR(50) NOT NULL,  -- fish, technique, spot, weather
    name VARCHAR(200) NOT NULL,
    description TEXT,

    -- 属性（JSON）
    properties JSONB DEFAULT '{}',

    -- 向量嵌入（用于语义搜索）
    embedding vector(1536),  -- OpenAI embedding 维度

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_type ON knowledge_nodes(node_type);
CREATE INDEX idx_knowledge_embedding ON knowledge_nodes USING ivfflat(embedding vector_cosine_ops);

-- 知识关系表
CREATE TABLE knowledge_relations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node_id UUID REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    to_node_id UUID REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL,  -- suitable_for, requires, related_to
    weight DECIMAL(3,2) DEFAULT 1.0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(from_node_id, to_node_id, relation_type)
);

CREATE INDEX idx_relations_from ON knowledge_relations(from_node_id);
CREATE INDEX idx_relations_to ON knowledge_relations(to_node_id);

-- ============================================
-- 6. 用户记忆（替代 ChromaDB）
-- ============================================

CREATE TABLE user_memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- 记忆内容
    memory_type VARCHAR(50) NOT NULL,  -- preference, conversation, behavior
    content TEXT NOT NULL,

    -- 向量嵌入
    embedding vector(1536),

    -- 元数据
    metadata JSONB DEFAULT '{}',
    importance DECIMAL(3,2) DEFAULT 0.5,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0
);

CREATE INDEX idx_memories_user ON user_memories(user_id);
CREATE INDEX idx_memories_embedding ON user_memories USING ivfflat(embedding vector_cosine_ops);

-- ============================================
-- 7. 系统表
-- ============================================

-- 审核日志
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);

-- 系统配置
CREATE TABLE system_configs (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 8. 触发器和函数
-- ============================================

-- 自动更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 应用到所有表
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spots_updated_at BEFORE UPDATE ON fishing_spots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_catch_updated_at BEFORE UPDATE ON catch_records
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 9. 视图（常用查询）
-- ============================================

-- 热门钓点视图
CREATE VIEW popular_spots AS
SELECT
    s.*,
    COUNT(DISTINCT c.id) as catch_count,
    COUNT(DISTINCT p.id) as post_count
FROM fishing_spots s
LEFT JOIN catch_records c ON s.id = c.spot_id
LEFT JOIN posts p ON s.id = p.spot_id
GROUP BY s.id
ORDER BY catch_count DESC, post_count DESC;

-- 用户统计视图
CREATE VIEW user_stats AS
SELECT
    u.id,
    u.nickname,
    COUNT(DISTINCT c.id) as total_catches,
    COUNT(DISTINCT p.id) as total_posts,
    COUNT(DISTINCT l.id) as total_likes
FROM users u
LEFT JOIN catch_records c ON u.id = c.user_id
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN likes l ON u.id = l.user_id
GROUP BY u.id, u.nickname;

-- ============================================
-- 10. 示例数据
-- ============================================

-- 插入测试用户
INSERT INTO users (openid, nickname, avatar_url) VALUES
('test_user_001', '钓鱼达人', 'https://example.com/avatar1.jpg'),
('test_user_002', '新手钓友', 'https://example.com/avatar2.jpg');

-- 插入测试钓点（深圳湾公园）
INSERT INTO fishing_spots (name, description, location, address, city, fish_species, facilities) VALUES
(
    '深圳湾公园',
    '深圳最受欢迎的钓点之一，环境优美，交通便利',
    ST_GeogFromText('POINT(113.9547 22.5167)'),
    '深圳市南山区深圳湾公园',
    '深圳',
    ARRAY['鲈鱼', '鲫鱼', '黑鱼'],
    ARRAY['停车场', '洗手间', '便利店']
);

-- ============================================
-- 完成！
-- ============================================
```

---

## 🔄 数据迁移步骤

### 方法 1：使用 Prisma Migrate（推荐）

```bash
# 1. 初始化 Prisma
cd 千鱼千寻3.0/backend
npm install prisma @prisma/client

# 2. 创建 Prisma Schema
npx prisma init

# 3. 编辑 schema.prisma（见下文）

# 4. 生成迁移
npx prisma migrate dev --name init

# 5. 应用迁移
npx prisma migrate deploy
```

### 方法 2：直接执行 SQL

```bash
# 连接到 Neon PostgreSQL
psql "postgresql://user:password@ep-xxx.neon.tech/qianyu?sslmode=require"

# 执行 SQL 文件
\i schema.sql

# 验证
\dt  # 列出所有表
\d users  # 查看 users 表结构
```

### 方法 3：从 MySQL 迁移数据

```bash
# 使用 pgloader
pgloader mysql://user:pass@localhost/qianyu \
         postgresql://user:pass@neon.tech/qianyu

# 或者导出 MySQL 数据
mysqldump -u root -p qianyu > qianyu_mysql.sql

# 转换并导入（需要手动调整）
```

---

## 🧪 测试查询

### 1. 地理位置查询（附近钓点）

```sql
-- 查找距离某个位置 10km 内的钓点
SELECT
    id,
    name,
    ST_Distance(
        location,
        ST_GeogFromText('POINT(113.9547 22.5167)')
    ) / 1000 as distance_km
FROM fishing_spots
WHERE ST_DWithin(
    location,
    ST_GeogFromText('POINT(113.9547 22.5167)'),
    10000  -- 10km
)
ORDER BY distance_km;
```

### 2. 全文搜索

```sql
-- 搜索钓点
SELECT name, description
FROM fishing_spots
WHERE search_vector @@ to_tsquery('chinese', '深圳 & 鲈鱼')
ORDER BY ts_rank(search_vector, to_tsquery('chinese', '深圳 & 鲈鱼')) DESC;
```

### 3. 向量搜索（语义搜索）

```sql
-- 查找相似的知识节点
SELECT name, description
FROM knowledge_nodes
ORDER BY embedding <-> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

### 4. JSON 查询

```sql
-- 查询用户偏好
SELECT nickname, preferences->>'favorite_fish' as favorite_fish
FROM users
WHERE preferences->>'favorite_fish' IS NOT NULL;
```

---

## 📊 性能优化

### 1. 创建必要的索引

```sql
-- 已在 schema 中创建，这里是补充

-- 复合索引
CREATE INDEX idx_catch_user_time ON catch_records(user_id, catch_time DESC);
CREATE INDEX idx_posts_user_status ON posts(user_id, status, created_at DESC);

-- 部分索引（只索引活跃数据）
CREATE INDEX idx_active_users ON users(id) WHERE is_active = true;
CREATE INDEX idx_published_posts ON posts(id) WHERE status = 'published';
```

### 2. 配置连接池

```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@neon.tech/qianyu",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_recycle=3600    # 1小时回收连接
)
```

---

## 🔐 安全配置

### 1. 创建只读用户（给 MCP Server 用）

```sql
-- 创建只读角色
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'secure_password';

-- 授予只读权限
GRANT CONNECT ON DATABASE qianyu TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- 自动授予新表的只读权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO readonly_user;
```

### 2. 行级安全（RLS）

```sql
-- 启用 RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 用户只能看到自己的草稿
CREATE POLICY posts_select_policy ON posts
FOR SELECT
USING (status = 'published' OR user_id = current_user_id());

-- 用户只能修改自己的帖子
CREATE POLICY posts_update_policy ON posts
FOR UPDATE
USING (user_id = current_user_id());
```

---

## ✅ 迁移检查清单

- [ ] Neon PostgreSQL 账号已创建
- [ ] 数据库连接字符串已获取
- [ ] Schema SQL 已执行
- [ ] 所有表已创建
- [ ] 索引已创建
- [ ] 触发器已创建
- [ ] 测试数据已插入
- [ ] 地理位置查询测试通过
- [ ] 全文搜索测试通过
- [ ] 向量搜索测试通过
- [ ] 性能测试通过
- [ ] 安全配置已完成

---

## 📚 下一步

1. **配置 Prisma ORM**
2. **更新 FastAPI 代码**
3. **配置 PostgreSQL MCP Server**
4. **测试 API 端点**

---

**PostgreSQL 迁移准备完成！** 🎉
