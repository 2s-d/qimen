# 文档引用：PROJECT_SPEC.md - 1566行
# 系统路由（6个API）

from fastapi import APIRouter, Depends, Header
from typing import Optional

from app.modules.system import service as system_service
from app.modules.system.schemas import (
    SystemConfigResponse,
    HelpDocResponse,
    FeedbackRequest,
    FeedbackResponse,
    AnnouncementResponse,
    StatisticsResponse,
    HealthResponse
)
from app.modules.user.models import User
from app.common.dependencies import get_current_user_optional
from app.common.response import success_response

router = APIRouter()


@router.get("/config", response_model=SystemConfigResponse)
async def get_system_config():
    """
    获取系统配置（文档5.3.1节）
    接口路径：GET /api/system/config
    认证要求：无需认证（公开接口）
    """
    config = system_service.get_system_config()
    return success_response(data=config)


@router.get("/help", response_model=HelpDocResponse)
async def get_help_doc():
    """
    获取帮助文档（文档5.3.2节）
    接口路径：GET /api/system/help
    认证要求：无需认证（公开接口）
    """
    help_doc = system_service.get_help_doc()
    return success_response(data=help_doc.dict())


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    authorization: Optional[str] = Header(None)
):
    """
    提交意见反馈（文档5.3.3节）
    接口路径：POST /api/system/feedback
    认证要求：无需认证（支持匿名反馈）
    """
    # 可选认证（支持匿名）
    current_user = await get_current_user_optional(authorization)
    
    feedback = system_service.save_feedback(request, current_user)
    return success_response(data=feedback.dict(), message="感谢您的反馈")


@router.get("/announcements", response_model=list[AnnouncementResponse])
async def get_announcements():
    """
    获取公告列表（文档5.3.4节）
    接口路径：GET /api/system/announcements
    认证要求：无需认证（公开接口）
    """
    try:
        announcements = system_service.get_announcements()
        return success_response(data=[ann.dict() for ann in announcements])
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"获取公告列表失败: {e}", exc_info=True)
        # 返回空列表而不是错误
        return success_response(data=[])


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    获取数据统计（文档5.3.5节）
    接口路径：GET /api/system/statistics
    认证要求：无需认证（公开接口）
    """
    statistics = system_service.get_statistics()
    return success_response(data=statistics.dict())


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    健康检查（文档5.3.6节）
    接口路径：GET /api/system/health
    认证要求：无需认证（公开接口）
    """
    health = system_service.check_health()
    return success_response(data=health.dict())
