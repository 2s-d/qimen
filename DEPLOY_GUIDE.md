# 🚀 qimen 项目前端自动部署指南

## 📋 部署架构

```
本地开发 → Git Push → GitHub Actions
  ↓
自动编译 (npm run build:h5)
  ↓
打包 dist 目录
  ↓
SCP 上传到服务器
  ↓
SSH 解压到 /var/www/qimen
  ↓
Nginx 静态托管 ✅
```

---

## 🏗️ 服务器架构说明

### 当前服务器配置文件结构：

```
/etc/nginx/sites-available/
├── portfolio        # 个人博客前端（静态托管）
├── cms             # 个人博客后端（反向代理到 1338）
└── focus-apps      # 所有其他项目的统一配置文件
    ├── kanban.paku.uno      → 反向代理到 3007
    ├── zhuanzhu.paku.uno    → 反向代理到 8085
    ├── tea.paku.uno         → 反向代理到 8082
    ├── stea.paku.uno        → 反向代理到 8081
    ├── teagw.paku.uno       → 反向代理到 3005
    ├── cteagw.paku.uno      → 反向代理到 1337
    └── qimen.paku.uno       → 静态托管 /var/www/qimen ✅
```

### qimen 项目配置：

- **前端**：静态文件托管在 `/var/www/qimen`
- **后端 API**：反向代理到 `localhost:8087`（内网穿透）
- **域名**：`qimen.paku.uno`

---

## 🔧 一、服务器端配置（已完成）

### 1.1 目录结构

```bash
/var/www/qimen/          # 前端静态文件目录
├── index.html
├── assets/
└── ...
```

### 1.2 Nginx 配置（在 focus-apps 文件中）

```nginx
# 奇门遁甲小程序前端
server {
    server_name qimen.paku.uno;

    root /var/www/qimen;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8087;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60;
        proxy_connect_timeout 60;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/kanban.paku.uno/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kanban.paku.uno/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

---

## 🔑 二、GitHub Secrets 配置

### 2.1 进入 GitHub 仓库设置

1. 打开 https://github.com/2s-d/qimen
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**

### 2.2 添加以下 Secrets

| Secret 名称 | 说明 | 值 |
|------------|------|--------|
| `SERVER_HOST` | 服务器 IP 地址 | `108.160.131.86` |
| `SERVER_SSH_PORT` | SSH 端口 | `1234` |
| `SERVER_USER` | SSH 用户名 | `root` |
| `SERVER_SSH_KEY` | SSH 私钥 | 完整的私钥内容 |

### 2.3 生成 SSH 密钥对（如果还没有）

在**本地电脑**执行：

```bash
# 生成新的 SSH 密钥对（专门用于 GitHub Actions）
ssh-keygen -t ed25519 -C "github-actions-qimen" -f ~/.ssh/github_actions_qimen

# 查看私钥（复制整个内容到 SERVER_SSH_KEY）
cat ~/.ssh/github_actions_qimen

# 查看公钥（需要添加到服务器）
cat ~/.ssh/github_actions_qimen.pub
```

### 2.4 将公钥添加到服务器

SSH 连接到服务器，执行：

```bash
# 将公钥添加到 authorized_keys
echo "你的公钥内容" >> ~/.ssh/authorized_keys

# 设置权限
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### 2.5 测试 SSH 连接

在本地测试：

```bash
ssh -i ~/.ssh/github_actions_qimen -p 1234 root@108.160.131.86
```

如果能成功连接，说明配置正确。

---

## 🎯 三、部署流程

### 3.1 首次部署

1. **确认主分支名称**
   
   检查您的主分支是 `main` 还是 `master`：
   
   ```bash
   git branch
   ```

2. **提交并推送代码**
   
   ```bash
   # 确保代码已提交
   git add .
   git commit -m "feat: 添加前端自动部署配置"
   git push origin main
   ```

3. **查看部署进度**
   
   - 打开 GitHub 仓库
   - 点击 **Actions** 标签
   - 查看 "Deploy qimen-miniapp H5 Frontend to Server" 工作流
   - 实时查看部署日志

### 3.2 后续部署

每次修改 `qimen-miniapp/` 目录下的代码并推送到 `main` 分支时，会自动触发部署：

```bash
# 修改代码后
git add qimen-miniapp/
git commit -m "feat: 更新前端功能"
git push origin main

# GitHub Actions 会自动：
# 1. 检测到 qimen-miniapp 目录变化
# 2. 安装依赖
# 3. 编译 H5 版本
# 4. 上传到服务器 /var/www/qimen
# 5. 解压并替换旧版本
```

---

## 🔍 四、故障排查

### 4.1 部署失败

**查看 GitHub Actions 日志：**
- 进入 Actions 标签
- 点击失败的工作流
- 查看具体错误信息

**常见问题：**

1. **SSH 连接失败**
   ```
   Error: Failed to connect to server
   ```
   - 检查 `SERVER_HOST` 和 `SERVER_SSH_PORT` 是否正确
   - 检查 SSH 密钥是否正确配置
   - 确认服务器防火墙允许 SSH 端口

2. **权限问题**
   ```
   Error: Permission denied
   ```
   - 确保 `/var/www/qimen` 目录权限正确
   - 检查 SSH 用户是否有写入权限

3. **构建失败**
   ```
   Error: npm run build:h5 failed
   ```
   - 检查 `package.json` 中是否有 `build:h5` 脚本
   - 查看构建日志中的具体错误

### 4.2 网站无法访问

1. **检查 Nginx 状态**
   ```bash
   sudo systemctl status nginx
   sudo nginx -t
   ```

2. **检查文件是否部署成功**
   ```bash
   ls -la /var/www/qimen/
   # 应该能看到 index.html 等文件
   ```

3. **查看 Nginx 日志**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

4. **检查 focus-apps 配置**
   ```bash
   cat /etc/nginx/sites-available/focus-apps | grep -A 20 "奇门遁甲"
   ```

---

## 📝 五、重要说明

### 5.1 架构变更

**之前的架构：**
- 前端：内网穿透 `localhost:3008` → 服务器 `3008` → Nginx 反向代理
- 后端：内网穿透 `localhost:8087` → 服务器 `8087` → Nginx 反向代理

**现在的架构：**
- 前端：GitHub Actions 自动部署到 `/var/www/qimen` → Nginx 静态托管 ✅
- 后端：内网穿透 `localhost:8087` → 服务器 `8087` → Nginx 反向代理（不变）

### 5.2 不再需要的服务

- ❌ 不再需要本地运行 `npm run dev:h5` 在 3008 端口
- ❌ 不再需要内网穿透 3008 端口
- ✅ 后端 8087 端口的内网穿透仍然需要

### 5.3 环境变量

如果前端需要配置 API 地址等环境变量，在 `.github/workflows/deploy-frontend.yml` 的 `Build frontend H5` 步骤中添加：

```yaml
- name: Build frontend H5
  working-directory: ./qimen-miniapp
  run: npm run build:h5
  env:
    NODE_ENV: production
    VITE_API_URL: https://qimen.paku.uno/api  # 示例
```

---

## ✅ 完成检查清单

部署前请确认：

- [x] 服务器已创建 `/var/www/qimen` 目录
- [x] Nginx 配置已在 focus-apps 中修改完成
- [x] Nginx 已重启并测试通过
- [ ] GitHub Secrets 已全部配置
- [ ] SSH 密钥已添加到服务器
- [ ] 本地可以通过 SSH 连接服务器
- [ ] 确认主分支名称（main/master）
- [ ] 代码已推送到 GitHub

---

## 🎉 六、后续计划

使用相同的方法，可以依次部署其他前端项目：

| 项目 | 当前状态 | 计划 |
|------|---------|------|
| qimen-miniapp-h5 | ✅ 已完成静态托管 | - |
| zhuanzhu-kanban | 反向代理 3007 | 待部署 |
| shangnantea-web | 反向代理 8082 | 待部署 |
| shangnantea-official-frontend | 反向代理 3005 | 待部署 |
| zhuanzhu-flutter | 反向代理 8085 | 待部署 |

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看 GitHub Actions 日志
2. 检查服务器 Nginx 日志
3. 确认所有配置步骤都已完成
4. 参考个人博客项目的配置

---

**祝部署顺利！🎉**

**访问地址：** https://qimen.paku.uno
