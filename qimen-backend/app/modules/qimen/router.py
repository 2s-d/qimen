# 文档引用：PROJECT_SPEC.md - 1555行
# 算命路由（8个API）

from fastapi import APIRouter, Depends, Query
from app.modules.qimen import schemas, service
from app.modules.user.models import User
from app.modules.user.dependencies import get_current_user
from app.common.response import success_response, paginated_response
from app.common.exceptions import BusinessException

router = APIRouter()

# 说明：
# 本文件中有两类路由：
# 1）/api/qimen/... 下的算命主流程接口（calculate/save/history/...）
# 2）/api/tools/...、/api/knowledge/... 这样的“工具类/知识类”接口
#    为了严格符合文档中的路径设计（不带 /qimen 前缀），
#    这里单独定义一个 public_router，在 main.py 中以 prefix="/api" 注册。
public_router = APIRouter()

@router.post("/calculate", summary="起盘计算")
async def calculate_qimen(request: schemas.QimenCalculateRequest):
    """
    起盘计算接口
    文档引用：PROJECT_SPEC.md - 5.2.1节
    """
    try:
        result = service.calculate_qimen(
            datetime_str=request.datetime,
            gender=request.gender,
            qimen_type=request.type,
            calendar_type=request.calendar_type or "公历"
        )
        return success_response(data=result, message="起盘成功")
    except BusinessException as e:
        raise

@router.post("/save", summary="保存起盘记录")
async def save_qimen_record(
    request: schemas.QimenSaveRequest,
    current_user: User = Depends(get_current_user)
):
    """
    保存起盘记录接口
    文档引用：PROJECT_SPEC.md - 5.2.2节
    """
    try:
        result = service.save_qimen_record(
            user_id=current_user.id,
            datetime_str=request.datetime,
            gender=request.gender,
            qimen_type=request.type,
            plate_data=request.plate_data,
            fortune_data=request.fortune_data,
            fortune_score=request.fortune_score
        )
        return success_response(data=result, message="保存成功")
    except BusinessException as e:
        raise

@router.get("/history", summary="获取历史记录列表")
async def get_history_list(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user)
):
    """
    获取历史记录列表接口（支持分页）
    文档引用：PROJECT_SPEC.md - 5.2.3节
    """
    try:
        result = service.get_user_history(
            user_id=current_user.id,
            page=page,
            size=size
        )
        return paginated_response(
            data=result["items"],
            total=result["total"],
            page=result["page"],
            size=result["size"]
        )
    except BusinessException as e:
        raise

@router.get("/history/{id}", summary="获取历史记录详情")
async def get_history_detail(
    id: int,
    current_user: User = Depends(get_current_user)
):
    """
    获取历史记录详情接口
    文档引用：PROJECT_SPEC.md - 5.2.4节
    """
    try:
        result = service.get_record_by_id(id, current_user.id)
        return success_response(data=result)
    except BusinessException as e:
        raise

@router.delete("/history/{id}", summary="删除历史记录")
async def delete_history_record(
    id: int,
    current_user: User = Depends(get_current_user)
):
    """
    删除历史记录接口
    文档引用：PROJECT_SPEC.md - 5.2.5节
    """
    try:
        service.delete_record(id, current_user.id)
        return success_response(data=None, message="删除成功")
    except BusinessException as e:
        raise

@router.get("/fortune", summary="获取今日运势")
def get_daily_fortune(
    date: str = Query(None, description="日期（YYYY-MM-DD），默认当天")
):
    """
    获取今日运势接口
    文档引用：PROJECT_SPEC.md - 5.2.6节
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"开始获取今日运势，日期参数: {date}")
        result = service.get_daily_fortune(date)
        logger.info(f"获取今日运势成功，结果: {result.get('overall_score', 'N/A')}")
        return success_response(data=result)
    except BusinessException as e:
        logger.error(f"业务异常: {e.message}")
        raise
    except Exception as e:
        # 捕获所有其他异常，记录日志并抛出业务异常
        import traceback
        logger.error(f"获取今日运势失败: {e}", exc_info=True)
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        raise BusinessException(code=500, message=f"获取今日运势失败: {str(e)}")

@public_router.get("/tools/calendar", summary="获取万年历数据")
async def get_calendar(
    year: int = Query(..., ge=1900, le=2100, description="年份"),
    month: int = Query(..., ge=1, le=12, description="月份")
):
    """
    获取万年历数据接口
    文档引用：PROJECT_SPEC.md - 5.2.7节
    """
    try:
        result = service.get_calendar_data(year, month)
        return success_response(data=result)
    except BusinessException as e:
        raise

@public_router.get("/knowledge/articles", summary="获取知识文章")
async def get_knowledge_articles(
    category: str = Query(..., description="文章分类：入门/八门/九星/八神/应用")
):
    """
    获取知识文章接口
    文档引用：PROJECT_SPEC.md - 5.2.8节
    """
    try:
        result = service.get_knowledge_articles(category)
        return success_response(data=result)
    except BusinessException as e:
        raise
