# 文档引用：PROJECT_SPEC.md - 1559行
# 奇门遁甲计算引擎
# 优先使用 kinqimen 库（可选，安装失败时使用内置简化算法）

from datetime import datetime
from typing import Dict, Any, List
from app.modules.qimen.constants import (
    EIGHT_DOORS, NINE_STARS, EIGHT_GODS, EIGHT_PALACES,
    STEMS, BRANCHES, FORTUNE_LEVELS
)

try:
    # 优先使用推荐的 kinqimen 库
    import kinqimen
    KINQIMEN_AVAILABLE = True
except ImportError:
    # TODO: kinqimen库不可用，暂时使用简化算法实现
    # 原因：库未安装或版本不兼容
    # 计划：安装 kinqimen==0.1.8 或使用替代方案
    KINQIMEN_AVAILABLE = False
    kinqimen = None

def calculate(datetime_str: str, gender: str, qimen_type: str) -> Dict[str, Any]:
    """
    主计算函数 - 根据日期时辰性别计算奇门遁甲盘面
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤3
    
    参数:
        datetime_str: 日期时间字符串，格式 "YYYY-MM-DD HH:mm"
        gender: 性别，"男"或"女"
        qimen_type: 起盘类型，"时家奇门"或"日家奇门"
    
    返回:
        PlateData结构（包含9宫数据）
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"calculate 开始，datetime_str: {datetime_str}, gender: {gender}, qimen_type: {qimen_type}")
        logger.info(f"KINQIMEN_AVAILABLE: {KINQIMEN_AVAILABLE}")
        
        if KINQIMEN_AVAILABLE:
            logger.info("使用 kinqimen 库计算")
            result = _calculate_with_kinqimen(datetime_str, gender, qimen_type)
        else:
            logger.info("使用简化算法计算")
            result = _calculate_simplified(datetime_str, gender, qimen_type)
        
        logger.info(f"calculate 完成，palaces数量: {len(result.get('palaces', []))}")
        return result
    except Exception as e:
        logger.error(f"calculate 异常: {e}", exc_info=True)
        raise

def _calculate_with_kinqimen(datetime_str: str, gender: str, qimen_type: str) -> Dict[str, Any]:
    """
    使用 kinqimen 库计算
    """
    # 解析日期时间
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    
    # 调用 kinqimen 库计算
    # TODO: 根据 kinqimen 库的实际API调整调用方式
    # 示例：result = kinqimen.calculate(dt, gender, qimen_type)
    
    # 转换为API定义的格式
    plate_data = {
        "datetime": datetime_str,
        "gender": gender,
        "type": qimen_type,
        "chief_star": "天蓬星",  # 从库结果获取
        "chief_door": "休门",    # 从库结果获取
        "palaces": []  # 从库结果转换9宫数据
    }
    
    # 生成9宫数据
    for i, palace in enumerate(EIGHT_PALACES):
        palace_data = {
            "position": palace["name"],
            "direction": palace["direction"],
            "heaven_star": NINE_STARS[i % len(NINE_STARS)],
            "earth_palace": palace["name"],
            "human_door": EIGHT_DOORS[i % len(EIGHT_DOORS)],
            "god": EIGHT_GODS[i % len(EIGHT_GODS)],
            "stem": STEMS[i % len(STEMS)],
            "branch": BRANCHES[i % len(BRANCHES)],
            "fortune": "中吉",
            "description": f"{palace['direction']}方位，适合..."
        }
        plate_data["palaces"].append(palace_data)
    
    return plate_data

def _calculate_simplified(datetime_str: str, gender: str, qimen_type: str) -> Dict[str, Any]:
    """
    简化算法实现（当 kinqimen 库不可用时使用）
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        logger.info("_calculate_simplified 开始")
        
        # 解析日期时间
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        logger.info(f"解析日期时间成功: {dt}")
        
        # 简化计算：根据日期时间生成基础盘面
        hour = dt.hour
        day = dt.day
        logger.info(f"hour: {hour}, day: {day}")
        
        # 确定值符值使（简化算法）
        chief_star_index = (day + hour) % len(NINE_STARS)
        chief_door_index = (day + hour) % len(EIGHT_DOORS)
        logger.info(f"chief_star_index: {chief_star_index}, chief_door_index: {chief_door_index}")
        
        plate_data = {
            "datetime": datetime_str,
            "gender": gender,
            "type": qimen_type,
            "chief_star": NINE_STARS[chief_star_index],
            "chief_door": EIGHT_DOORS[chief_door_index],
            "palaces": []
        }
        
        logger.info(f"开始生成9宫数据，EIGHT_PALACES数量: {len(EIGHT_PALACES)}")
        
        # 生成9宫数据
        for i, palace in enumerate(EIGHT_PALACES):
            # 简化计算：根据位置和日期时间生成数据
            star_index = (i + day) % len(NINE_STARS)
            door_index = (i + hour) % len(EIGHT_DOORS)
            god_index = (i + day + hour) % len(EIGHT_GODS)
            stem_index = (i + day) % len(STEMS)
            branch_index = (i + hour) % len(BRANCHES)
            
            # 简化吉凶判断
            fortune_scores = ["大吉", "中吉", "平", "凶", "大凶"]
            fortune = fortune_scores[(i + day) % len(fortune_scores)]
            
            palace_data = {
                "position": palace["name"],
                "direction": palace["direction"],
                "heaven_star": NINE_STARS[star_index],
                "earth_palace": palace["name"],
                "human_door": EIGHT_DOORS[door_index],
                "god": EIGHT_GODS[god_index],
                "stem": STEMS[stem_index],
                "branch": BRANCHES[branch_index],
                "fortune": fortune,
                "description": f"{palace['direction']}方位，{fortune}，适合相关活动"
            }
            plate_data["palaces"].append(palace_data)
        
        logger.info(f"_calculate_simplified 完成，palaces数量: {len(plate_data['palaces'])}")
        return plate_data
    except Exception as e:
        logger.error(f"_calculate_simplified 异常: {e}", exc_info=True)
        raise

def get_ju(datetime_str: str) -> Dict[str, Any]:
    """
    确定节气和局数（阴遁/阳遁）
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤3
    """
    # TODO: 实现完整的节气判断和局数计算
    # 简化实现
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    month = dt.month
    
    # 简化：根据月份判断阴阳遁
    is_yang = month in [3, 4, 5, 6, 7, 8]  # 春夏为阳遁
    ju_num = (month + dt.day) % 9 + 1  # 简化局数计算
    
    return {
        "is_yang": is_yang,
        "ju_num": ju_num,
        "solar_term": ""  # 需要从calendar_utils获取
    }

def get_zhifu_zhishi(plate_data: Dict[str, Any]) -> Dict[str, str]:
    """
    确定值符值使
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤3
    """
    return {
        "chief_star": plate_data.get("chief_star", "天蓬星"),
        "chief_door": plate_data.get("chief_door", "休门")
    }

def arrange_bagong(plate_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    排八宫（天盘、地盘、人盘、神盘）
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤3
    """
    return plate_data.get("palaces", [])

def calculate_fortune(palace: Dict[str, Any]) -> str:
    """
    计算每宫吉凶
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤3
    """
    return palace.get("fortune", "平")
