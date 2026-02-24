# 文档引用：PROJECT_SPEC.md - 1585行
# 数据库初始化 - 确保所有模型被导入

# 导入所有模型，确保SQLAlchemy能够识别它们
from app.modules.user.models import User
from app.modules.qimen.models import QimenRecord, KnowledgeArticle
from app.modules.system.models import SystemConfig, Announcement, Feedback

# 导入Base，供其他模块使用
from app.db.base import Base

__all__ = ["Base", "User", "QimenRecord", "KnowledgeArticle", "SystemConfig", "Announcement", "Feedback"]
