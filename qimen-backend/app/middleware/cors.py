# 文档引用：PROJECT_SPEC.md - 1592行
# CORS跨域配置

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def setup_cors(app: FastAPI):
    """
    配置CORS中间件
    文档引用：PROJECT_SPEC.md - 1592行
    部署：支持本地开发(localhost:3008)和公网(qimen.paku.uno)
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3008", "http://127.0.0.1:3008",  # 本地开发
            "http://localhost:8080", "http://127.0.0.1:8080",  # 备用开发端口
            "https://qimen.paku.uno", "http://qimen.paku.uno"   # 公网域名
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
