# 文档引用：PROJECT_SPEC.md - 1593行
# 日志中间件

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# 配置日志
import os
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件
    文档引用：PROJECT_SPEC.md - 1593行
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f"请求: {request.method} {request.url.path}")
        if request.query_params:
            logger.info(f"查询参数: {request.query_params}")
        
        # 处理请求
        response = await call_next(request)
        
        # 计算耗时
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(f"响应: {response.status_code} - 耗时: {process_time:.3f}秒")
        
        return response
