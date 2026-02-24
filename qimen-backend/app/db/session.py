# 文档引用：PROJECT_SPEC.md - 1587行
# 数据库会话管理

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# 数据库文件路径（文档4.1节：data/qimen.db）
DATABASE_URL = f"sqlite:///./data/qimen.db"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite需要
    echo=False  # 开发阶段可设为True查看SQL
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话（用于依赖注入）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
