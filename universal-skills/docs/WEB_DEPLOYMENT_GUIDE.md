# Web 端部署完整指南

> 版本：1.0
> 日期：2026-03-11
> 适用项目：千鱼千寻 3.0

---

## 📋 部署前准备

### 1. 服务器要求
- **操作系统**：Ubuntu 20.04+ / CentOS 7+
- **内存**：至少 2GB
- **磁盘**：至少 20GB
- **网络**：公网 IP 或域名

### 2. 软件要求
```bash
# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Nginx
sudo apt-get install -y nginx

# 安装 Certbot (SSL 证书)
sudo apt-get install -y certbot python3-certbot-nginx

# 安装 rsync
sudo apt-get install -y rsync
```

### 3. 域名配置
将域名解析到服务器 IP：
```
A 记录: qianyu.iepose.cn -> 你的服务器IP
A 记录: www.qianyu.iepose.cn -> 你的服务器IP
```

---

## 🚀 自动化部署（推荐）

### 方式 1：使用 web-deployer skill

#### 步骤 1：配置环境变量
```bash
# 在本地创建 .env 文件
cat > .env << EOF
DEPLOY_SERVER_HOST=你的服务器IP
DEPLOY_SERVER_USER=root
DEPLOY_SSH_KEY=~/.ssh/id_rsa
DEPLOY_DOMAIN=qianyu.iepose.cn
DEPLOY_SSL_EMAIL=admin@qianyu.com
DEPLOY_PATH=/var/www/qianyu
EOF
```

#### 步骤 2：首次部署
```bash
# 进入项目目录
cd 千鱼千寻3.0/frontend

# 执行部署
fishing-cli deploy init \
  --project-path . \
  --domain qianyu.iepose.cn \
  --server root@你的服务器IP \
  --build-command "npm run build" \
  --dist-dir "dist"
```

#### 步骤 3：配置 SSL
```bash
fishing-cli deploy ssl \
  --domain qianyu.iepose.cn \
  --email admin@qianyu.com
```

#### 步骤 4：验证部署
```bash
# 查看部署状态
fishing-cli deploy status

# 访问网站
curl https://qianyu.iepose.cn
```

### 方式 2：通过飞书命令（OpenClaw）

```
# 在飞书管理员群发送
/deploy web

# 查看部署状态
/deploy status

# 如果失败，回滚
/deploy rollback
```

---

## 🛠️ 手动部署

### 步骤 1：构建前端代码

```bash
# 进入前端项目目录
cd 千鱼千寻3.0/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 构建完成后，dist 目录包含所有静态文件
```

### 步骤 2：上传到服务器

```bash
# 使用 rsync 上传
rsync -avz --delete dist/ root@你的服务器IP:/var/www/qianyu/

# 或使用 scp
scp -r dist/* root@你的服务器IP:/var/www/qianyu/
```

### 步骤 3：配置 Nginx

```bash
# SSH 登录服务器
ssh root@你的服务器IP

# 创建 Nginx 配置文件
sudo nano /etc/nginx/sites-available/qianyu
```

粘贴以下配置：
```nginx
server {
    listen 80;
    server_name qianyu.iepose.cn www.qianyu.iepose.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name qianyu.iepose.cn www.qianyu.iepose.cn;

    # SSL 证书（稍后配置）
    ssl_certificate /etc/letsencrypt/live/qianyu.iepose.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/qianyu.iepose.cn/privkey.pem;

    # 网站根目录
    root /var/www/qianyu;
    index index.html;

    # 前端路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### 步骤 4：启用配置

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/qianyu /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 步骤 5：配置 SSL 证书

```bash
# 使用 Certbot 申请证书
sudo certbot --nginx -d qianyu.iepose.cn -d www.qianyu.iepose.cn

# 按提示输入邮箱和同意条款
# Certbot 会自动配置 Nginx 并申请证书

# 测试自动续期
sudo certbot renew --dry-run
```

### 步骤 6：验证部署

```bash
# 检查 Nginx 状态
sudo systemctl status nginx

# 检查 SSL 证书
sudo certbot certificates

# 访问网站
curl https://qianyu.iepose.cn
```

---

## 🔄 更新部署

### 自动更新
```bash
# 使用 web-deployer
fishing-cli deploy update --project-path ./frontend

# 或通过飞书
/deploy web
```

### 手动更新
```bash
# 1. 本地构建
cd 千鱼千寻3.0/frontend
git pull origin main
npm run build

# 2. 备份当前版本
ssh root@服务器IP "cp -r /var/www/qianyu /var/www/qianyu.backup"

# 3. 上传新版本
rsync -avz --delete dist/ root@服务器IP:/var/www/qianyu/

# 4. 验证
curl https://qianyu.iepose.cn

# 5. 如果有问题，回滚
ssh root@服务器IP "rm -rf /var/www/qianyu && mv /var/www/qianyu.backup /var/www/qianyu"
```

---

## 🔙 回滚部署

### 自动回滚
```bash
# 回滚到上一版本
fishing-cli deploy rollback

# 回滚到指定版本
fishing-cli deploy rollback --version deploy_20260310_001
```

### 手动回滚
```bash
# 查看所有版本
ssh root@服务器IP "ls -lt /var/www/qianyu.*"

# 回滚到备份版本
ssh root@服务器IP "rm -rf /var/www/qianyu && mv /var/www/qianyu.backup /var/www/qianyu"
```

---

## 📊 监控和维护

### 1. 查看 Nginx 日志
```bash
# 访问日志
sudo tail -f /var/log/nginx/access.log

# 错误日志
sudo tail -f /var/log/nginx/error.log
```

### 2. 查看 SSL 证书状态
```bash
# 查看证书信息
sudo certbot certificates

# 手动续期
sudo certbot renew
```

### 3. 性能监控
```bash
# 安装 htop
sudo apt-get install htop

# 查看系统资源
htop

# 查看磁盘使用
df -h

# 查看网络连接
netstat -tulpn
```

### 4. 自动化监控（OpenClaw）
```
# 在飞书发送
/monitor status
/monitor nginx
/monitor ssl
```

---

## 🐛 故障排查

### 问题 1：网站无法访问

**检查步骤**：
```bash
# 1. 检查 Nginx 状态
sudo systemctl status nginx

# 2. 检查端口占用
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# 3. 检查防火墙
sudo ufw status
sudo ufw allow 80
sudo ufw allow 443

# 4. 检查文件权限
ls -la /var/www/qianyu
```

### 问题 2：SSL 证书错误

**检查步骤**：
```bash
# 1. 检查证书状态
sudo certbot certificates

# 2. 测试证书续期
sudo certbot renew --dry-run

# 3. 强制续期
sudo certbot renew --force-renewal

# 4. 检查 Nginx 配置
sudo nginx -t
```

### 问题 3：页面 404 错误

**检查步骤**：
```bash
# 1. 检查文件是否存在
ls -la /var/www/qianyu/index.html

# 2. 检查 Nginx 配置
sudo nginx -t

# 3. 查看错误日志
sudo tail -f /var/log/nginx/error.log

# 4. 检查前端路由配置
# 确保 Nginx 配置中有 try_files $uri $uri/ /index.html;
```

### 问题 4：API 请求失败

**检查步骤**：
```bash
# 1. 检查后端服务
curl http://localhost:8000/health

# 2. 检查 Nginx 代理配置
sudo nginx -t

# 3. 查看代理日志
sudo tail -f /var/log/nginx/error.log

# 4. 测试代理
curl -H "Host: qianyu.iepose.cn" http://localhost/api/v1/health
```

---

## 🔐 安全加固

### 1. SSH 安全
```bash
# 禁用密码登录，只允许密钥认证
sudo nano /etc/ssh/sshd_config

# 修改以下配置
PasswordAuthentication no
PubkeyAuthentication yes

# 重启 SSH
sudo systemctl restart sshd
```

### 2. 防火墙配置
```bash
# 启用 UFW
sudo ufw enable

# 允许必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS

# 查看状态
sudo ufw status
```

### 3. 自动更新
```bash
# 安装自动更新
sudo apt-get install unattended-upgrades

# 配置自动更新
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 4. 备份策略
```bash
# 创建备份脚本
cat > /root/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backup/qianyu_$DATE.tar.gz /var/www/qianyu
find /backup -name "qianyu_*.tar.gz" -mtime +7 -delete
EOF

# 添加执行权限
chmod +x /root/backup.sh

# 添加到 crontab（每天凌晨 2 点备份）
echo "0 2 * * * /root/backup.sh" | sudo crontab -
```

---

## 📈 性能优化

### 1. 启用 HTTP/2
```nginx
# 在 Nginx 配置中
listen 443 ssl http2;
```

### 2. 启用 Gzip 压缩
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

### 3. 配置缓存
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 4. 使用 CDN
- 将静态资源上传到 CDN
- 修改前端配置，使用 CDN 地址

---

## 🎯 总结

### 推荐部署方式

1. **开发环境**：手动部署，方便调试
2. **测试环境**：自动化部署（web-deployer）
3. **生产环境**：OpenClaw + 飞书命令

### 部署检查清单

- [ ] 服务器环境准备完成
- [ ] 域名解析配置正确
- [ ] 前端代码构建成功
- [ ] 文件上传到服务器
- [ ] Nginx 配置正确
- [ ] SSL 证书配置成功
- [ ] 网站可以正常访问
- [ ] API 代理工作正常
- [ ] 监控和告警配置完成
- [ ] 备份策略已设置

### 维护建议

- 每周检查 SSL 证书状态
- 每月检查服务器资源使用
- 定期更新系统和软件
- 保持至少 3 个版本的备份
- 使用 OpenClaw 自动化监控

---

**部署完成！祝你的网站运行顺利！** 🎉
