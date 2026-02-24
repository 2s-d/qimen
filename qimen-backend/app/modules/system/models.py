# 文档引用：PROJECT_SPEC.md - 1567行
# 系统数据模型（对应数据库表4.2.4 system_config、4.2.5 announcements、4.2.6 feedback）

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class SystemConfig(Base):
    """
    系统配置表模型
    文档引用：PROJECT_SPEC.md - 4.2.4节
    """
    __tablename__ = "system_config"
    
    # 字段定义（严格按照文档4.2.4节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)  # UNIQUE NOT NULL，索引idx_config_key（unique=True自动创建唯一索引）
    value = Column(Text, nullable=False)  # NOT NULL，JSON格式
    description = Column(String(200), nullable=True)  # NULL
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 索引（文档4.2.4节：unique=True自动创建唯一索引idx_config_key）
    __table_args__ = (
        {"sqlite_autoincrement": True}
    )


class Announcement(Base):
    """
    公告表模型
    文档引用：PROJECT_SPEC.md - 4.2.5节
    """
    __tablename__ = "announcements"
    
    # 字段定义（严格按照文档4.2.5节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)  # NOT NULL
    content = Column(Text, nullable=False)  # NOT NULL
    priority = Column(Integer, nullable=False, default=0)  # NOT NULL DEFAULT 0，索引idx_priority_created
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())  # NOT NULL，索引idx_priority_created
    
    # 索引（文档4.2.5节）
    __table_args__ = (
        Index("idx_priority_created", "priority", "created_at"),  # 组合索引idx_priority_created
        {"sqlite_autoincrement": True}
    )


class Feedback(Base):
    """
    意见反馈表模型
    文档引用：PROJECT_SPEC.md - 4.2.6节
    """
    __tablename__ = "feedback"
    
    # 字段定义（严格按照文档4.2.6节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # NULL FOREIGN KEY，索引idx_user_id
    content = Column(Text, nullable=False)  # NOT NULL
    contact = Column(String(100), nullable=True)  # NULL
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())  # NOT NULL，索引idx_created_at
    
    # 索引（文档4.2.6节）
    __table_args__ = (
        Index("idx_user_id_feedback", "user_id"),  # 索引idx_user_id
        Index("idx_created_at_feedback", "created_at"),  # 索引idx_created_at
        {"sqlite_autoincrement": True}
    )
    
    # 关系（可选）
    user = relationship("User", backref="feedbacks")
