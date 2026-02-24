# 文档引用：PROJECT_SPEC.md - 1569行
# 系统业务逻辑

import json
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.modules.system.models import SystemConfig, Announcement, Feedback
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
from app.modules.qimen.models import QimenRecord, KnowledgeArticle
from app.db.session import SessionLocal
from app.common.exceptions import ValidationException, BusinessException

logger = logging.getLogger(__name__)


def get_system_config() -> Dict[str, Any]:
    """
    获取系统配置（文档5.3.1节）
    步骤1：检查缓存（简化版，直接查询数据库）
    步骤2：查询数据库
    步骤3：合并配置
    步骤4：返回结果
    """
    db = SessionLocal()
    try:
        # 查询所有配置项
        configs = db.query(SystemConfig).all()
        
        # 构造配置字典
        config_dict = {}
        for config in configs:
            try:
                # 解析JSON value
                value = json.loads(config.value) if config.value else None
                config_dict[config.key] = value
            except json.JSONDecodeError:
                logger.warning(f"配置项 {config.key} 的value不是有效的JSON")
                config_dict[config.key] = config.value
        
        # 提取常用配置项（文档5.3.1节 - 步骤3）
        result = {
            "app_version": config_dict.get("app_version", "1.0.0"),
            "banner_images": config_dict.get("banner_images", []),
            "contact_email": config_dict.get("contact_email", "support@example.com"),
            "about_text": config_dict.get("about_text", ""),
            "disclaimer": config_dict.get("disclaimer", "")
        }
        
        return result
    finally:
        db.close()


def get_help_doc() -> HelpDocResponse:
    """
    获取帮助文档（文档5.3.2节）
    步骤1：查询配置
    步骤2：返回结果
    """
    db = SessionLocal()
    try:
        # 查询帮助文档配置
        help_config = db.query(SystemConfig).filter(
            SystemConfig.key == "help_doc"
        ).first()
        
        if help_config:
            try:
                help_data = json.loads(help_config.value)
                questions = help_data.get("questions", [])
            except json.JSONDecodeError:
                # 如果解析失败，使用默认帮助文档
                questions = get_default_help_questions()
        else:
            # 如果没有配置，使用默认帮助文档
            questions = get_default_help_questions()
        
        return HelpDocResponse(questions=questions)
    finally:
        db.close()


def get_default_help_questions() -> List[Dict[str, str]]:
    """获取默认帮助问题列表"""
    return [
        {
            "question": "如何起盘？",
            "answer": "1. 点击首页\"起盘\"按钮\n2. 输入出生日期和时辰\n3. 选择性别\n4. 点击\"开始起盘\"按钮"
        },
        {
            "question": "如何查看历史记录？",
            "answer": "1. 点击底部\"历史\"按钮\n2. 选择要查看的记录\n3. 点击\"查看详情\"查看完整信息"
        },
        {
            "question": "历史记录可以保存多少条？",
            "answer": "每个用户最多可以保存100条历史记录，超出后会自动删除最早的记录。"
        },
        {
            "question": "如何修改个人信息？",
            "answer": "1. 点击底部\"我的\"按钮\n2. 点击\"修改资料\"\n3. 修改昵称后保存"
        }
    ]


def save_feedback(
    request: FeedbackRequest,
    current_user: Optional[User] = None
) -> FeedbackResponse:
    """
    保存意见反馈（文档5.3.3节）
    步骤1：参数验证（已在schema中验证）
    步骤2：创建反馈记录
    步骤3：返回结果
    """
    db = SessionLocal()
    try:
        # 创建反馈记录
        feedback = Feedback(
            user_id=current_user.id if current_user else None,  # 匿名时为None
            content=request.content,
            contact=request.contact
            # created_at 由数据库自动设置
        )
        
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        
        return FeedbackResponse(
            id=feedback.id,
            created_at=feedback.created_at
        )
    except Exception as e:
        db.rollback()
        logger.error(f"保存反馈失败: {e}", exc_info=True)
        raise BusinessException(f"保存反馈失败: {str(e)}", code=500)
    finally:
        db.close()


def get_announcements() -> List[AnnouncementResponse]:
    """
    获取公告列表（文档5.3.4节）
    步骤1：查询公告（按priority降序、created_at降序，最多3条）
    步骤2：返回结果
    """
    db = SessionLocal()
    try:
        # 查询最新3条公告（文档5.3.4节 - 步骤1）
        announcements = db.query(Announcement).order_by(
            Announcement.priority.desc(),
            Announcement.created_at.desc()
        ).limit(3).all()
        
        # 转换为响应格式
        result = [
            AnnouncementResponse(
                id=ann.id,
                title=ann.title,
                content=ann.content,
                priority=ann.priority,
                created_at=ann.created_at
            )
            for ann in announcements
        ]
        
        return result
    except Exception as e:
        logger.error(f"获取公告列表失败: {e}", exc_info=True)
        # 如果查询失败，返回空列表而不是抛出异常
        return []
    finally:
        db.close()


def get_statistics() -> StatisticsResponse:
    """
    获取数据统计（文档5.3.5节）
    步骤1：查询总用户数
    步骤2：查询总起盘次数
    步骤3：查询今日起盘次数
    步骤4：查询知识文章数
    步骤5：返回结果
    """
    db = SessionLocal()
    try:
        # 步骤1：查询总用户数
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # 步骤2：查询总起盘次数
        total_qipan = db.query(func.count(QimenRecord.id)).scalar() or 0
        
        # 步骤3：查询今日起盘次数
        today = date.today()
        today_qipan = db.query(func.count(QimenRecord.id)).filter(
            func.date(QimenRecord.created_at) == today
        ).scalar() or 0
        
        # 步骤4：查询知识文章数
        total_articles = db.query(func.count(KnowledgeArticle.id)).scalar() or 0
        
        # 步骤5：返回结果
        return StatisticsResponse(
            total_users=total_users,
            total_qipan=total_qipan,
            today_qipan=today_qipan,
            total_articles=total_articles
        )
    finally:
        db.close()


def check_health() -> HealthResponse:
    """
    健康检查（文档5.3.6节）
    检查服务状态和数据库连接
    """
    db = SessionLocal()
    try:
        # 检查数据库连接（使用SQLAlchemy的方式）
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        database_status = "connected"
        status = "healthy"
    except Exception as e:
        logger.error(f"数据库连接失败: {e}", exc_info=True)
        database_status = "disconnected"
        status = "unhealthy"
    finally:
        db.close()
    
    return HealthResponse(
        status=status,
        database=database_status,
        timestamp=datetime.now()
    )
