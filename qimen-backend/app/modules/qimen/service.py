# 文档引用：PROJECT_SPEC.md - 1558行
# 算命业务逻辑

from app.db.session import SessionLocal
from app.modules.qimen.models import QimenRecord, KnowledgeArticle
from app.modules.qimen import schemas
from app.modules.qimen.qimen_engine import calculate
from app.modules.qimen.calendar_utils import (
    solar_to_lunar, lunar_to_solar, get_solar_term, get_stem_branch,
    get_month_calendar, get_lunar_festival
)
from app.modules.qimen.interpretation import (
    get_overall_fortune, get_career_fortune, get_wealth_fortune,
    get_love_fortune, get_health_fortune, get_notices
)
from app.common.exceptions import (
    ValidationException, NotFoundException, PermissionException
)
from app.common.pagination import get_pagination_params, calculate_offset
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

def calculate_qimen(
    datetime_str: str,
    gender: str,
    qimen_type: str,
    calendar_type: str = "公历"
) -> Dict[str, Any]:
    """
    起盘计算
    文档引用：PROJECT_SPEC.md - 5.2.1节业务逻辑
    """
    # 步骤1：参数验证
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValidationException("日期格式错误，应为 YYYY-MM-DD HH:mm")
    
    # 验证日期范围（1900-2100年）
    if dt.year < 1900 or dt.year > 2100:
        raise ValidationException("日期范围必须在1900-2100年之间")
    
    # 验证日期不超过当前时间
    if dt > datetime.now():
        raise ValidationException("日期不能超过当前时间")
    
    # 验证性别和起盘类型
    if gender not in ["男", "女"]:
        raise ValidationException("性别必须是'男'或'女'")
    
    if qimen_type not in ["时家奇门", "日家奇门"]:
        raise ValidationException("起盘类型必须是'时家奇门'或'日家奇门'")
    
    # MVP版本只实现时家奇门
    if qimen_type != "时家奇门":
        raise ValidationException("MVP版本只支持时家奇门")
    
    # 步骤2：日历转换
    solar_date = dt.date()
    if calendar_type == "农历":
        # 如果是农历，需要转换为公历（这里简化处理）
        # TODO: 实现完整的农历转公历
        pass
    
    # 步骤3：起盘计算
    plate_data = calculate(datetime_str, gender, qimen_type)
    
    # 步骤4：生成运势解读
    overall = get_overall_fortune(plate_data)
    fortune_data = {
        "overall_score": overall["overall_score"],
        "overall_fortune": overall["overall_fortune"],
        "fortunes": {
            "career": get_career_fortune(plate_data),
            "wealth": get_wealth_fortune(plate_data),
            "love": get_love_fortune(plate_data),
            "health": get_health_fortune(plate_data)
        },
        "notices": get_notices(plate_data)
    }
    
    # 步骤5：返回结果
    result = {
        **plate_data,
        "fortune_data": fortune_data
    }
    
    return result

def save_qimen_record(
    user_id: int,
    datetime_str: str,
    gender: str,
    qimen_type: str,
    plate_data: Dict[str, Any],
    fortune_data: Dict[str, Any],
    fortune_score: float
) -> Dict[str, Any]:
    """
    保存起盘记录
    文档引用：PROJECT_SPEC.md - 5.2.2节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：检查记录数量限制
        record_count = db.query(QimenRecord).filter(
            QimenRecord.user_id == user_id
        ).count()
        
        if record_count >= 100:
            # 查询最早的记录
            oldest_record = db.query(QimenRecord).filter(
                QimenRecord.user_id == user_id
            ).order_by(QimenRecord.created_at.asc()).first()
            
            if oldest_record:
                db.delete(oldest_record)
        
        # 步骤2：创建记录
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        record = QimenRecord(
            user_id=user_id,
            datetime=dt,
            gender=gender,
            type=qimen_type,
            plate_data=json.dumps(plate_data, ensure_ascii=False),
            fortune_data=json.dumps(fortune_data, ensure_ascii=False),
            fortune_score=fortune_score
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # 步骤3：返回结果
        return {
            "id": record.id,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    finally:
        db.close()

def get_user_history(
    user_id: int,
    page: int = 1,
    size: int = 10
) -> Dict[str, Any]:
    """
    获取用户历史记录列表
    文档引用：PROJECT_SPEC.md - 5.2.3节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：参数验证
        page, size = get_pagination_params(page, size)
        
        # 步骤2：查询总数
        total = db.query(QimenRecord).filter(
            QimenRecord.user_id == user_id
        ).count()
        
        # 步骤3：分页查询
        offset = calculate_offset(page, size)
        records = db.query(QimenRecord).filter(
            QimenRecord.user_id == user_id
        ).order_by(QimenRecord.created_at.desc()).offset(offset).limit(size).all()
        
        # 步骤4：计算分页信息
        pages = (total + size - 1) // size if size > 0 else 0
        
        # 步骤5：返回结果
        items = []
        for record in records:
            items.append({
                "id": record.id,
                "datetime": record.datetime.strftime("%Y-%m-%d %H:%M"),
                "gender": record.gender,
                "type": record.type,
                "fortune_score": float(record.fortune_score),
                "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    finally:
        db.close()

def get_record_by_id(record_id: int, user_id: int) -> Dict[str, Any]:
    """
    获取历史记录详情
    文档引用：PROJECT_SPEC.md - 5.2.4节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：查询记录
        record = db.query(QimenRecord).filter(QimenRecord.id == record_id).first()
        if not record:
            raise NotFoundException("记录不存在", code=404)
        
        # 步骤2：验证所有权
        if record.user_id != user_id:
            raise PermissionException("无权访问此记录", code=403)
        
        # 步骤3：解析JSON数据
        plate_data = json.loads(record.plate_data)
        fortune_data = json.loads(record.fortune_data)
        
        # 步骤4：返回结果
        return {
            "id": record.id,
            "datetime": record.datetime.strftime("%Y-%m-%d %H:%M"),
            "gender": record.gender,
            "type": record.type,
            "plate_data": plate_data,
            "fortune_data": fortune_data,
            "fortune_score": float(record.fortune_score),
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    finally:
        db.close()

def delete_record(record_id: int, user_id: int) -> None:
    """
    删除历史记录
    文档引用：PROJECT_SPEC.md - 5.2.5节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：查询记录
        record = db.query(QimenRecord).filter(QimenRecord.id == record_id).first()
        if not record:
            raise NotFoundException("记录不存在", code=404)
        
        # 步骤2：验证所有权
        if record.user_id != user_id:
            raise PermissionException("无权删除此记录", code=403)
        
        # 步骤3：删除记录
        db.delete(record)
        db.commit()
    finally:
        db.close()

def get_daily_fortune(date_str: Optional[str] = None) -> Dict[str, Any]:
    """
    获取今日运势
    文档引用：PROJECT_SPEC.md - 5.2.6节业务逻辑
    """
    try:
        logger.info(f"get_daily_fortune 开始，date_str: {date_str}")
        
        # 步骤1：确定日期
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()
        
        logger.info(f"目标日期: {target_date}")
        
        # 步骤2：检查缓存（简化实现，暂不实现缓存）
        # TODO: 实现缓存机制，缓存到当天23:59:59
        
        # 步骤3：计算今日运势
        # 使用当天日期和子时（00:00）作为起盘时间
        datetime_str = f"{target_date.strftime('%Y-%m-%d')} 00:00"
        logger.info(f"开始计算盘面，datetime_str: {datetime_str}")
        
        plate_data = calculate(datetime_str, "男", "时家奇门")
        logger.info(f"盘面计算完成，palaces数量: {len(plate_data.get('palaces', []))}")
        
        # 生成运势解读
        logger.info("开始生成运势解读")
        overall = get_overall_fortune(plate_data)
        logger.info(f"总体运势: {overall}")
        
        fortune_data = {
            "date": target_date.strftime("%Y-%m-%d"),
            "overall_score": overall["overall_score"],
            "overall_fortune": overall["overall_fortune"],
            "fortunes": {
                "career": get_career_fortune(plate_data),
                "wealth": get_wealth_fortune(plate_data),
                "love": get_love_fortune(plate_data),
                "health": get_health_fortune(plate_data)
            },
            "notices": get_notices(plate_data)
        }
        
        logger.info(f"运势解读生成完成，overall_score: {fortune_data['overall_score']}")
        
        # 步骤4：缓存结果（简化实现，暂不实现）
        # TODO: 实现缓存机制
        
        # 步骤5：返回结果
        return fortune_data
    except Exception as e:
        logger.error(f"get_daily_fortune 异常: {e}", exc_info=True)
        raise

def get_calendar_data(year: int, month: int) -> Dict[str, Any]:
    """
    获取万年历数据
    文档引用：PROJECT_SPEC.md - 5.2.7节业务逻辑
    """
    # 步骤1：参数验证
    if year < 1900 or year > 2100:
        raise ValidationException("年份必须在1900-2100之间", code=400)
    
    if month < 1 or month > 12:
        raise ValidationException("月份必须在1-12之间", code=400)
    
    # 步骤2：生成月历数据
    days = get_month_calendar(year, month)
    
    # 步骤3：返回结果
    return {
        "year": year,
        "month": month,
        "days": days
    }

def get_knowledge_articles(category: str) -> List[Dict[str, Any]]:
    """
    获取知识文章
    文档引用：PROJECT_SPEC.md - 5.2.8节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：参数验证
        valid_categories = ["入门", "八门", "九星", "八神", "应用"]
        if category not in valid_categories:
            raise ValidationException("分类参数错误", code=400)
        
        # 步骤2：查询文章
        articles = db.query(KnowledgeArticle).filter(
            KnowledgeArticle.category == category
        ).order_by(KnowledgeArticle.order_num.asc()).all()
        
        # 步骤3：返回结果
        result = []
        for article in articles:
            result.append({
                "id": article.id,
                "category": article.category,
                "title": article.title,
                "summary": article.summary,
                "content": article.content,
                "order_num": article.order_num,
                "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return result
    finally:
        db.close()
