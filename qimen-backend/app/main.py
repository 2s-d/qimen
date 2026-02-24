# 文档引用：PROJECT_SPEC.md - 1540行
# 应用入口 - FastAPI应用主入口

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.common.exceptions import (
    BusinessException,
    ValidationException,
    AuthException,
    PermissionException,
    NotFoundException
)
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.core.database import init_db
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="奇门遁甲API",
    description="奇门遁甲算命小程序后端API",
    version="1.0.0"
)

# 配置CORS
setup_cors(app)

# 配置日志中间件
app.add_middleware(LoggingMiddleware)

# 全局异常处理器（文档6.3.2节）
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """业务异常处理器"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    """参数验证异常处理器"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    """认证异常处理器"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

@app.exception_handler(PermissionException)
async def permission_exception_handler(request: Request, exc: PermissionException):
    """权限异常处理器"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """资源不存在异常处理器"""
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message, "data": None}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误", "data": None}
    )

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("正在初始化数据库...")
    init_db()
    logger.info("数据库初始化完成")

# 根路径健康检查
@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "奇门遁甲API服务运行中", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "message": "服务正常"}

# 注册各模块路由
from app.modules.user.router import router as user_router
from app.modules.qimen import router as qimen_router, public_router as qimen_public_router
from app.modules.system import router as system_router
from app.modules.ai import router as ai_router

app.include_router(user_router, prefix="/api/user", tags=["用户模块"])
# 算命主流程接口（起盘、保存、历史、运势等），挂在 /api/qimen/...
app.include_router(qimen_router, prefix="/api/qimen", tags=["算命模块"])
# 工具类/知识类接口（万年历、基础知识），按文档要求挂在 /api/tools/...、/api/knowledge/...
app.include_router(qimen_public_router, prefix="/api", tags=["算命模块"])
app.include_router(system_router, prefix="/api/system", tags=["系统模块"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI助手"])
