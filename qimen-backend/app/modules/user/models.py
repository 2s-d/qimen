# 文档引用：PROJECT_SPEC.md - 1548行
# 用户数据模型（对应数据库表4.2.1 users）

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    """
    用户表模型
    文档引用：PROJECT_SPEC.md - 4.2.1节
    """
    __tablename__ = "users"
    
    # 字段定义（严格按照文档4.2.1节）
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)  # UNIQUE NOT NULL，索引idx_username
    password_hash = Column(String(255), nullable=False)  # NOT NULL，bcrypt加密
    nickname = Column(String(50), nullable=True)  # NULL，可选
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 索引（文档4.2.1节：unique=True自动创建唯一索引idx_username）
    __table_args__ = (
        {"sqlite_autoincrement": True}
    )
    
    def verify_password(self, password: str) -> bool:
        """
        验证密码
        文档引用：PROJECT_SPEC.md - 4.2.1节业务规则
        """
        from app.core.security import verify_password
        return verify_password(password, self.password_hash)
    
    def set_password(self, password: str):
        """
        设置密码（bcrypt加密）
        文档引用：PROJECT_SPEC.md - 4.2.1节业务规则
        """
        from app.core.security import hash_password
        self.password_hash = hash_password(password)
