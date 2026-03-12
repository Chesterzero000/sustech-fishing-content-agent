-- ============================================
-- 千鱼千寻 PostgreSQL Schema
-- 版本: 3.0
-- 日期: 2026-03-11
-- ============================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID 生成
CREATE EXTENSION IF NOT EXISTS "postgis";        -- 地理位置
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- 模糊搜索
CREATE EXTENSION IF NOT EXISTS "vector";         -- 向量搜索（需要 pgvector）

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
    preferences JSONB DEFAULT '{}',
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
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    district VARCHAR(50),
    fish_species TEXT[],
    facilities TEXT[],
    price_range VARCHAR(50),
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    rating DECIMAL(3,2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    images TEXT[],
    tags TEXT[],
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT false,
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('chinese',
            coalesce(name, '') || ' ' ||
            coalesce(description, '') || ' ' ||
            coalesce(address, '')
        )
    ) STORED
);

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
    fish_species VARCHAR(100) NOT NULL,
    weight DECIMAL(10,2),
    length DECIMAL(10,2),
    quantity INTEGER DEFAULT 1,
    catch_time TIMESTAMP NOT NULL,
    weather_condition VARCHAR(50),
    temperature DECIMAL(5,2),
    bait_used VARCHAR(100),
    technique VARCHAR(100),
    images TEXT[],
    notes TEXT,
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
    content TEXT NOT NULL,
    images TEXT[],
    video_url TEXT,
    spot_id UUID REFERENCES fishing_spots(id),
    catch_id UUID REFERENCES catch_records(id),
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'published',
    is_pinned BOOLEAN DEFAULT false,
    review_status VARCHAR(20) DEFAULT 'pending',
    review_note TEXT,
    reviewed_at TIMESTAMP,
    reviewed_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('chinese', coalesce(content, ''))
    ) STORED
);

CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status, created_at DESC);
CREATE INDEX idx_posts_search ON posts USING gin(search_vector);

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES comments(id),
    content TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post ON comments(post_id, created_at);
CREATE INDEX idx_comments_user ON comments(user_id);

CREATE TABLE likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    target_type VARCHAR(20) NOT NULL,
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
    node_type VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    properties JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_type ON knowledge_nodes(node_type);
CREATE INDEX idx_knowledge_embedding ON knowledge_nodes USING ivfflat(embedding vector_cosine_ops);

CREATE TABLE knowledge_relations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node_id UUID REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    to_node_id UUID REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL,
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
    memory_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
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

CREATE TABLE system_configs (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 8. 触发器
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spots_updated_at BEFORE UPDATE ON fishing_spots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_catch_updated_at BEFORE UPDATE ON catch_records
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 9. 视图
-- ============================================

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

INSERT INTO users (openid, nickname, avatar_url) VALUES
('test_user_001', '钓鱼达人', 'https://example.com/avatar1.jpg'),
('test_user_002', '新手钓友', 'https://example.com/avatar2.jpg');

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

-- 完成！
