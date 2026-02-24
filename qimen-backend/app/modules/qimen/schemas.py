# 文档引用：PROJECT_SPEC.md - 1557行
# 算命请求/响应模式

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# ========== 起盘计算接口 ==========

class QimenCalculateRequest(BaseModel):
    """起盘计算请求 - 文档5.2.1节"""
    datetime: str = Field(..., description="起盘日期时间，格式：YYYY-MM-DD HH:mm")
    gender: str = Field(..., description="性别：男/女")
    type: str = Field(..., description="起盘类型：时家奇门/日家奇门")
    calendar_type: Optional[str] = Field("公历", description="日历类型：公历/农历")
    
    @validator("gender")
    def validate_gender(cls, v):
        if v not in ["男", "女"]:
            raise ValueError("性别必须是'男'或'女'")
        return v
    
    @validator("type")
    def validate_type(cls, v):
        if v not in ["时家奇门", "日家奇门"]:
            raise ValueError("起盘类型必须是'时家奇门'或'日家奇门'")
        return v

class PalaceData(BaseModel):
    """宫位数据"""
    position: str = Field(..., description="宫位名称，如：巽4")
    direction: str = Field(..., description="方位，如：东南")
    heaven_star: str = Field(..., description="天盘（九星）")
    earth_palace: str = Field(..., description="地盘（八宫）")
    human_door: str = Field(..., description="人盘（八门）")
    god: str = Field(..., description="神盘（八神）")
    stem: str = Field(..., description="天干")
    branch: str = Field(..., description="地支")
    fortune: str = Field(..., description="吉凶：大吉/中吉/平/凶/大凶")
    description: str = Field(..., description="说明文字")

class PlateData(BaseModel):
    """盘面数据"""
    datetime: str
    gender: str
    type: str
    chief_star: str = Field(..., description="值符（九星）")
    chief_door: str = Field(..., description="值使（八门）")
    palaces: List[PalaceData] = Field(..., description="九宫数据（9个宫位）")

class FortuneItem(BaseModel):
    """单项运势"""
    score: float = Field(..., ge=1.0, le=5.0, description="评分1-5")
    text: str = Field(..., description="运势文案50-100字")

class FortuneData(BaseModel):
    """运势数据"""
    overall_score: float = Field(..., ge=1.0, le=5.0, description="总体评分")
    overall_fortune: str = Field(..., description="总体吉凶")
    fortunes: Dict[str, FortuneItem] = Field(..., description="分类运势：career/wealth/love/health")
    notices: List[str] = Field(..., description="注意事项3-5条")

class QimenCalculateResponse(BaseModel):
    """起盘计算响应 - 文档5.2.1节"""
    datetime: str
    gender: str
    type: str
    chief_star: str
    chief_door: str
    palaces: List[PalaceData]
    fortune_data: FortuneData

# ========== 保存起盘记录接口 ==========

class QimenSaveRequest(BaseModel):
    """保存起盘记录请求 - 文档5.2.2节"""
    datetime: str
    gender: str
    type: str
    plate_data: Dict[str, Any] = Field(..., description="完整盘面数据（PlateData结构）")
    fortune_data: Dict[str, Any] = Field(..., description="运势数据（FortuneData结构）")
    fortune_score: float = Field(..., ge=1.0, le=5.0, description="运势评分")

class QimenSaveResponse(BaseModel):
    """保存起盘记录响应 - 文档5.2.2节"""
    id: int
    created_at: str

# ========== 历史记录列表接口 ==========

class HistoryListItem(BaseModel):
    """历史记录列表项 - 文档5.2.3节"""
    id: int
    datetime: str
    gender: str
    type: str
    fortune_score: float
    created_at: str

class QimenHistoryListResponse(BaseModel):
    """历史记录列表响应 - 文档5.2.3节"""
    items: List[HistoryListItem]
    total: int
    page: int
    size: int
    pages: int

# ========== 历史记录详情接口 ==========

class QimenHistoryResponse(BaseModel):
    """历史记录详情响应 - 文档5.2.4节"""
    id: int
    datetime: str
    gender: str
    type: str
    plate_data: Dict[str, Any]
    fortune_data: Dict[str, Any]
    fortune_score: float
    created_at: str

# ========== 今日运势接口 ==========

class FortuneResponse(BaseModel):
    """今日运势响应 - 文档5.2.6节"""
    date: str
    overall_score: float
    overall_fortune: str
    fortunes: Dict[str, FortuneItem]
    notices: List[str]

# ========== 万年历接口 ==========

class CalendarDay(BaseModel):
    """日历日期数据 - 文档5.2.7节"""
    date: str = Field(..., description="日期YYYY-MM-DD")
    day: int = Field(..., description="日（1-31）")
    weekday: int = Field(..., description="星期几（0=周日，1=周一...6=周六）")
    lunar_date: str = Field(..., description="农历日期，如：腊月初十")
    lunar_month: str = Field(..., description="农历月份，如：腊月")
    lunar_day: str = Field(..., description="农历日，如：初十")
    solar_term: str = Field(default="", description="节气，如：小寒")
    festival: str = Field(default="", description="公历节日，如：元旦")
    lunar_festival: str = Field(default="", description="农历节日，如：春节")
    stem_branch: str = Field(..., description="天干地支，如：甲子年丙子月甲子日")
    is_today: bool = Field(..., description="是否今天")

class CalendarResponse(BaseModel):
    """万年历响应 - 文档5.2.7节"""
    year: int
    month: int
    days: List[CalendarDay]

# ========== 知识文章接口 ==========

class KnowledgeArticleResponse(BaseModel):
    """知识文章响应 - 文档5.2.8节"""
    id: int
    category: str
    title: str
    summary: str
    content: str
    order_num: int
    created_at: str
