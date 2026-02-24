# 文档引用：PROJECT_SPEC.md - 1588行
# 数据库初始化脚本

from app.core.database import init_db
from app.db.session import SessionLocal
from app.modules.user.models import User
from app.modules.qimen.models import QimenRecord, KnowledgeArticle
from app.modules.system.models import SystemConfig, Announcement, Feedback
from app.core.security import hash_password
import json

def create_tables():
    """
    创建所有表
    文档引用：PROJECT_SPEC.md - 4.2节
    """
    init_db()
    print("✅ 数据库表创建成功")

def init_data():
    """
    初始化基础数据
    文档引用：PROJECT_SPEC.md - 1611行
    """
    db = SessionLocal()
    try:
        # 1. 创建系统配置（文档4.2.4节）
        configs = [
            {
                "key": "app_version",
                "value": json.dumps({"version": "1.0.0", "update_time": "2024-01-01"}),
                "description": "应用版本号"
            },
            {
                "key": "banner_images",
                "value": json.dumps({
                    "images": [
                        {"url": "/static/images/banner/banner1.jpg", "link": ""},
                        {"url": "/static/images/banner/banner2.jpg", "link": ""},
                        {"url": "/static/images/banner/banner3.jpg", "link": ""}
                    ]
                }),
                "description": "首页轮播图"
            },
            {
                "key": "contact_email",
                "value": json.dumps({"email": "support@qimen.com"}),
                "description": "联系邮箱"
            },
            {
                "key": "help_doc",
                "value": json.dumps({
                    "questions": [
                        {
                            "question": "如何起盘？",
                            "answer": "在起盘页面选择日期、时辰、性别，点击起盘按钮即可。"
                        },
                        {
                            "question": "如何查看历史记录？",
                            "answer": "在历史记录页面可以查看所有保存的起盘记录。"
                        },
                        {
                            "question": "如何保存起盘记录？",
                            "answer": "在盘面展示页面点击保存记录按钮即可保存。"
                        }
                    ]
                }),
                "description": "帮助文档"
            }
        ]
        
        for config_data in configs:
            existing = db.query(SystemConfig).filter(SystemConfig.key == config_data["key"]).first()
            if not existing:
                config = SystemConfig(**config_data)
                db.add(config)
        
        # 2. 创建示例公告（文档4.2.5节）
        announcements = [
            {
                "title": "欢迎使用奇门遁甲小程序",
                "content": "本小程序提供奇门遁甲起盘、运势解读等功能，欢迎使用！",
                "priority": 1
            },
            {
                "title": "功能更新通知",
                "content": "新增万年历功能，支持公历农历转换。",
                "priority": 0
            }
        ]
        
        for ann_data in announcements:
            existing = db.query(Announcement).filter(Announcement.title == ann_data["title"]).first()
            if not existing:
                announcement = Announcement(**ann_data)
                db.add(announcement)
        
        # 3. 创建示例知识文章（文档4.2.3节）
        # TODO: 知识文章种子数据较多，先创建最少数据，完整数据见scripts/seed_knowledge.py
        articles = [
            {
                "category": "入门",
                "title": "什么是奇门遁甲",
                "summary": "奇门遁甲是中国古代术数之一，以时间、空间、人事为三大要素，通过排盘推演来预测吉凶。",
                "content": "<h2>什么是奇门遁甲</h2><p>奇门遁甲是中国古代术数之一，以时间、空间、人事为三大要素，通过排盘推演来预测吉凶。</p>",
                "order_num": 1
            }
        ]
        
        for article_data in articles:
            existing = db.query(KnowledgeArticle).filter(
                KnowledgeArticle.category == article_data["category"],
                KnowledgeArticle.title == article_data["title"]
            ).first()
            if not existing:
                article = KnowledgeArticle(**article_data)
                db.add(article)
        
        db.commit()
        print("✅ 初始数据插入成功")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 初始数据插入失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化数据库...")
    create_tables()
    init_data()
    print("✅ 数据库初始化完成")
