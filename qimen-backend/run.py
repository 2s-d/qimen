# 文档引用：PROJECT_SPEC.md - 1627行
# 快速启动脚本
# 部署架构：奇门后端本地端口8087，frp穿透到公网8087

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8087,
        reload=True,
        reload_excludes=["tests/*", "tests"],
        log_level="info"
    )
