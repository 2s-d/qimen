# 文档引用：PROJECT_SPEC.md - 1574行
# 数据库连接管理

from app.db.base import Base
from app.db.session import engine
import os

def init_db():
    """
    初始化数据库（创建所有表）
    文档引用：PROJECT_SPEC.md - 1588行
    """
    # 确保data目录存在
    os.makedirs("data", exist_ok=True)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)

def close_db():
    """
    关闭数据库连接
    """
    engine.dispose()
