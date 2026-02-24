# 文档引用：PROJECT_SPEC.md - 1568行
# 系统请求/响应模式

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class SystemConfigResponse(BaseModel):
    """系统配置响应（文档5.3.1节）"""
    app_version: str = Field(..., description="应用版本号")
    banner_images: List[str] = Field(..., description="轮播图列表")
    contact_email: str = Field(..., description="联系邮箱")
    about_text: Optional[str] = Field(None, description="应用介绍文字")
    disclaimer: Optional[str] = Field(None, description="免责声明")
    
    class Config:
        json_schema_extra = {
            "example": {
                "app_version": "1.0.0",
                "banner_images": [
                    "https://example.com/banner1.jpg",
                    "https://example.com/banner2.jpg",
                    "https://example.com/banner3.jpg"
                ],
                "contact_email": "support@example.com",
                "about_text": "奇门遁甲算命小程序...",
                "disclaimer": "本应用仅供娱乐..."
            }
        }


class HelpQuestion(BaseModel):
    """帮助问题项"""
    question: str = Field(..., description="问题")
    answer: str = Field(..., description="答案")


class HelpDocResponse(BaseModel):
    """帮助文档响应（文档5.3.2节）"""
    questions: List[HelpQuestion] = Field(..., description="帮助问题列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "questions": [
                    {
                        "question": "如何起盘？",
                        "answer": "1. 点击首页\"起盘\"按钮\n2. 输入出生日期和时辰\n3. 选择性别\n4. 点击\"开始起盘\"按钮"
                    }
                ]
            }
        }


class FeedbackRequest(BaseModel):
    """意见反馈请求（文档5.3.3节）"""
    content: str = Field(..., min_length=10, max_length=500, description="反馈内容（10-500字）")
    contact: Optional[str] = Field(None, max_length=100, description="联系方式（可选）")
    
    @validator("content")
    def validate_content(cls, v):
        if len(v) < 10:
            raise ValueError("反馈内容不能少于10字")
        if len(v) > 500:
            raise ValueError("反馈内容不能超过500字")
        return v


class FeedbackResponse(BaseModel):
    """意见反馈响应"""
    id: int = Field(..., description="反馈ID")
    created_at: datetime = Field(..., description="创建时间")


class AnnouncementResponse(BaseModel):
    """公告响应（文档5.3.4节）"""
    id: int = Field(..., description="公告ID")
    title: str = Field(..., description="公告标题")
    content: str = Field(..., description="公告内容")
    priority: int = Field(..., description="优先级")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "欢迎使用奇门遁甲小程序",
                "content": "本应用提供专业的奇门遁甲起盘和解读服务...",
                "priority": 10,
                "created_at": "2024-01-01 12:00:00"
            }
        }


class StatisticsResponse(BaseModel):
    """数据统计响应（文档5.3.5节）"""
    total_users: int = Field(..., description="总用户数")
    total_qipan: int = Field(..., description="总起盘次数")
    today_qipan: int = Field(..., description="今日起盘次数")
    total_articles: int = Field(..., description="知识文章总数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_users": 1000,
                "total_qipan": 5000,
                "today_qipan": 50,
                "total_articles": 25
            }
        }


class HealthResponse(BaseModel):
    """健康检查响应（文档5.3.6节）"""
    status: str = Field(..., description="服务状态（healthy/unhealthy）")
    database: str = Field(..., description="数据库状态（connected/disconnected）")
    timestamp: datetime = Field(..., description="检查时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2024-01-01 12:00:00"
            }
        }
