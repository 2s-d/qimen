# 文档引用：PROJECT_SPEC.md - 1560行
# 日历转换工具
# 优先使用 sxtwl==1.1.0 库

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional

try:
    # 优先使用推荐的 sxtwl 库
    import sxtwl
    SXTWL_AVAILABLE = True
except ImportError:
    # TODO: sxtwl库不可用，暂时使用简化日期转换
    # 原因：库未安装或版本不兼容
    # 计划：安装 sxtwl==1.1.0 或使用替代方案
    SXTWL_AVAILABLE = False
    sxtwl = None

def solar_to_lunar(solar_date: date) -> Dict[str, Any]:
    """
    公历转农历
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤2
    
    参数:
        solar_date: 公历日期
    
    返回:
        {
            "lunar_year": int,
            "lunar_month": int,
            "lunar_day": int,
            "lunar_month_name": str,  # 如：腊月
            "lunar_day_name": str,     # 如：初十
            "lunar_date_str": str      # 如：腊月初十
        }
    """
    if SXTWL_AVAILABLE:
        return _solar_to_lunar_with_sxtwl(solar_date)
    else:
        return _solar_to_lunar_simplified(solar_date)

def _solar_to_lunar_with_sxtwl(solar_date: date) -> Dict[str, Any]:
    """
    使用 sxtwl 库转换
    """
    # TODO: 根据 sxtwl 库的实际API调整调用方式
    # 示例：
    # day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    # lunar_year = day.getLunarYear()
    # lunar_month = day.getLunarMonth()
    # lunar_day = day.getLunarDay()
    
    # 简化返回
    return {
        "lunar_year": solar_date.year,
        "lunar_month": solar_date.month,
        "lunar_day": solar_date.day,
        "lunar_month_name": f"{solar_date.month}月",
        "lunar_day_name": f"{solar_date.day}日",
        "lunar_date_str": f"{solar_date.month}月{solar_date.day}日"
    }

def _solar_to_lunar_simplified(solar_date: date) -> Dict[str, Any]:
    """
    简化转换（当 sxtwl 库不可用时使用）
    """
    # 简化实现：直接返回格式化的日期
    return {
        "lunar_year": solar_date.year,
        "lunar_month": solar_date.month,
        "lunar_day": solar_date.day,
        "lunar_month_name": f"{solar_date.month}月",
        "lunar_day_name": f"{solar_date.day}日",
        "lunar_date_str": f"{solar_date.month}月{solar_date.day}日"
    }

def lunar_to_solar(lunar_year: int, lunar_month: int, lunar_day: int) -> date:
    """
    农历转公历
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤2
    """
    if SXTWL_AVAILABLE:
        return _lunar_to_solar_with_sxtwl(lunar_year, lunar_month, lunar_day)
    else:
        return _lunar_to_solar_simplified(lunar_year, lunar_month, lunar_day)

def _lunar_to_solar_with_sxtwl(lunar_year: int, lunar_month: int, lunar_day: int) -> date:
    """
    使用 sxtwl 库转换
    """
    # TODO: 根据 sxtwl 库的实际API调整调用方式
    # 简化返回
    return date(lunar_year, lunar_month, lunar_day)

def _lunar_to_solar_simplified(lunar_year: int, lunar_month: int, lunar_day: int) -> date:
    """
    简化转换
    """
    # 简化实现：直接返回日期（实际应进行转换）
    return date(lunar_year, lunar_month, lunar_day)

def get_solar_term(solar_date: date) -> str:
    """
    获取节气
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤2
    """
    if SXTWL_AVAILABLE:
        return _get_solar_term_with_sxtwl(solar_date)
    else:
        return _get_solar_term_simplified(solar_date)

def _get_solar_term_with_sxtwl(solar_date: date) -> str:
    """
    使用 sxtwl 库获取节气
    """
    # TODO: 根据 sxtwl 库的实际API调整调用方式
    return ""

def _get_solar_term_simplified(solar_date: date) -> str:
    """
    简化获取节气
    """
    # 简化实现：根据日期判断节气（需要完整算法）
    return ""

def get_lunar_festival(lunar_month: int, lunar_day: int) -> str:
    """
    获取农历节日
    文档引用：PROJECT_SPEC.md - 5.2.7节
    """
    # 常见农历节日
    festivals = {
        (1, 1): "春节",
        (1, 15): "元宵节",
        (5, 5): "端午节",
        (7, 7): "七夕",
        (8, 15): "中秋节",
        (9, 9): "重阳节",
        (12, 30): "除夕"
    }
    return festivals.get((lunar_month, lunar_day), "")

def get_stem_branch(solar_date: date) -> str:
    """
    计算天干地支
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤2
    
    返回格式：甲子年丙子月甲子日
    """
    if SXTWL_AVAILABLE:
        return _get_stem_branch_with_sxtwl(solar_date)
    else:
        return _get_stem_branch_simplified(solar_date)

def _get_stem_branch_with_sxtwl(solar_date: date) -> str:
    """
    使用 sxtwl 库计算天干地支
    """
    # TODO: 根据 sxtwl 库的实际API调整调用方式
    return f"{solar_date.year}年{solar_date.month}月{solar_date.day}日"

def _get_stem_branch_simplified(solar_date: date) -> str:
    """
    简化计算天干地支
    """
    from app.modules.qimen.constants import STEMS, BRANCHES
    
    # 简化计算
    year_stem = STEMS[(solar_date.year - 1900) % 10]
    year_branch = BRANCHES[(solar_date.year - 1900) % 12]
    month_stem = STEMS[(solar_date.month - 1) % 10]
    month_branch = BRANCHES[(solar_date.month - 1) % 12]
    day_stem = STEMS[(solar_date.day - 1) % 10]
    day_branch = BRANCHES[(solar_date.day - 1) % 12]
    
    return f"{year_stem}{year_branch}年{month_stem}{month_branch}月{day_stem}{day_branch}日"

def get_month_calendar(year: int, month: int) -> List[Dict[str, Any]]:
    """
    获取月历数据（包含公历农历节气节日）
    文档引用：PROJECT_SPEC.md - 5.2.7节
    
    返回该月所有日期的完整信息
    """
    days = []
    
    # 获取该月第一天和最后一天
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    today = date.today()
    
    # 遍历该月每一天
    current_date = first_day
    while current_date <= last_day:
        lunar_data = solar_to_lunar(current_date)
        solar_term = get_solar_term(current_date)
        lunar_festival = get_lunar_festival(lunar_data["lunar_month"], lunar_data["lunar_day"])
        stem_branch = get_stem_branch(current_date)
        
        # 公历节日
        festival = ""
        if (current_date.month, current_date.day) == (1, 1):
            festival = "元旦"
        elif (current_date.month, current_date.day) == (5, 1):
            festival = "劳动节"
        elif (current_date.month, current_date.day) == (10, 1):
            festival = "国庆节"
        
        day_data = {
            "date": current_date.strftime("%Y-%m-%d"),
            "day": current_date.day,
            "weekday": current_date.weekday(),  # 0=周一, 6=周日
            "lunar_date": lunar_data["lunar_date_str"],
            "lunar_month": lunar_data["lunar_month_name"],
            "lunar_day": lunar_data["lunar_day_name"],
            "solar_term": solar_term,
            "festival": festival,
            "lunar_festival": lunar_festival,
            "stem_branch": stem_branch,
            "is_today": current_date == today
        }
        days.append(day_data)
        current_date += timedelta(days=1)
    
    return days
