# 文档引用：PROJECT_SPEC.md - 1556行
# 算命数据模型（对应数据库表4.2.2 qimen_records和4.2.3 knowledge_articles）

from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, ForeignKey, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class QimenRecord(Base):
    """
    起盘记录表模型
    文档引用：PROJECT_SPEC.md - 4.2.2节
    """
    __tablename__ = "qimen_records"
    
    # 字段定义（严格按照文档4.2.2节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # FOREIGN KEY，索引idx_user_id
    datetime = Column(DateTime, nullable=False)  # NOT NULL，起盘日期时间
    gender = Column(String(10), nullable=False)  # NOT NULL CHECK(gender IN ('男','女'))
    type = Column(String(20), nullable=False)  # NOT NULL CHECK(type IN ('时家奇门','日家奇门'))
    plate_data = Column(Text, nullable=False)  # NOT NULL，JSON格式盘面数据
    fortune_data = Column(Text, nullable=False)  # NOT NULL，JSON格式运势数据
    fortune_score = Column(DECIMAL(2, 1), nullable=False)  # NOT NULL CHECK(fortune_score >= 1.0 AND fortune_score <= 5.0)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())  # NOT NULL，索引idx_created_at
    
    # CHECK约束和索引（文档4.2.2节）
    __table_args__ = (
        CheckConstraint("gender IN ('男','女')", name="check_gender"),
        CheckConstraint("type IN ('时家奇门','日家奇门')", name="check_type"),
        CheckConstraint("fortune_score >= 1.0 AND fortune_score <= 5.0", name="check_fortune_score"),
        Index("idx_user_id", "user_id"),  # 索引idx_user_id
        Index("idx_created_at", "created_at"),  # 索引idx_created_at
        Index("idx_user_created", "user_id", "created_at"),  # 组合索引idx_user_created
        {"sqlite_autoincrement": True}
    )
    
    # 关系（可选，用于ORM查询）
    user = relationship("User", backref="qimen_records")


class KnowledgeArticle(Base):
    """
    知识文章表模型
    文档引用：PROJECT_SPEC.md - 4.2.3节
    """
    __tablename__ = "knowledge_articles"
    
    # 字段定义（严格按照文档4.2.3节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(20), nullable=False, index=True)  # NOT NULL CHECK(category IN ('入门','八门','九星','八神','应用'))
    title = Column(String(100), nullable=False)  # NOT NULL
    summary = Column(Text, nullable=False)  # NOT NULL，100字以内
    content = Column(Text, nullable=False)  # NOT NULL，支持富文本
    order_num = Column(Integer, nullable=False, default=0, index=True)  # NOT NULL DEFAULT 0，索引idx_category_order
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    
    # CHECK约束和索引（文档4.2.3节）
    __table_args__ = (
        CheckConstraint("category IN ('入门','八门','九星','八神','应用')", name="check_category"),
        Index("idx_category_order", "category", "order_num"),  # 组合索引idx_category_order
        {"sqlite_autoincrement": True}
    )
