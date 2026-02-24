项目5：奇门遁甲小程序（qimen.paku.uno）

# 奇门遁甲小程序

server {

    listen 80;

    listen 443 ssl http2;

    server_name qimen.paku.uno;

    # SSL 证书配置（Certbot 已自动配置，这里省略）

    # ssl_certificate /etc/letsencrypt/live/qimen.paku.uno/fullchain.pem;

    # ssl_certificate_key /etc/letsencrypt/live/qimen.paku.uno/privkey.pem;

    # HTTP 自动跳转 HTTPS

    if ($scheme != "https") {

        return 301 https://$server_name$request_uri;

    }

    # 前端静态站点（uni-app H5，通过 frp 暴露到本机 3008）

    location / {

        proxy_pass http://127.0.0.1:3008;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;

        # 前端静态资源缓存

        proxy_cache_valid 200 1h;

    }

    # HTTP API 代理：/api -> 本机 8087（FastAPI 后端，通过 frp 暴露）

    location /api/ {

        proxy_pass http://127.0.0.1:8087/;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;

        # API 超时设置

        proxy_read_timeout 60;

        proxy_connect_timeout 60;

    }

}

配置说明

奇门遁甲小程序（qimen.paku.uno）

/ → 127.0.0.1:3008（uni-app H5 前端）

/api/ → 127.0.0.1:8087/（FastAPI 后端）

注意事项

SSL 证书：Certbot 已自动配置，ssl_certificate 和 ssl_certificate_key 行已省略，实际文件中会有。

HTTP → HTTPS 跳转：已包含自动跳转。

API 路径：/api/ 末尾的斜杠很重要，确保路径正确转发。前端使用相对路径 `/api/xxx`，nginx 会将 `/api/` 转发到后端根路径 `/`。

前端配置：前端已配置为使用相对路径（API_BASE_URL = ''），所有 API 请求为 `/api/xxx` 格式，由 nginx 统一转发。
