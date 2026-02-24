# 文档引用：PROJECT_SPEC.md - 1547行
# 用户路由（4个API）

from fastapi import APIRouter, Depends
from app.modules.user import schemas, service
from app.modules.user.models import User
from app.modules.user.dependencies import get_current_user
from app.common.response import success_response
from app.common.exceptions import BusinessException

router = APIRouter()

@router.post("/register", summary="用户注册")
async def register(request: schemas.UserRegisterRequest):
    """
    用户注册接口
    文档引用：PROJECT_SPEC.md - 5.1.1节
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        result = service.create_user(
            username=request.username,
            password=request.password,
            nickname=request.nickname
        )
        return success_response(data=result, message="注册成功")
    except BusinessException as e:
        logger.error(f"用户注册业务异常: {e.message}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"用户注册未知异常: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        raise BusinessException(f"注册失败: {str(e)}", code=500)

@router.post("/login", summary="用户登录")
async def login(request: schemas.UserLoginRequest):
    """
    用户登录接口
    文档引用：PROJECT_SPEC.md - 5.1.2节
    """
    try:
        result = service.authenticate_user(
            username=request.username,
            password=request.password
        )
        return success_response(data=result, message="登录成功")
    except BusinessException as e:
        raise

@router.get("/info", summary="获取用户信息")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """
    获取用户信息接口
    文档引用：PROJECT_SPEC.md - 5.1.3节
    """
    try:
        result = service.get_user_info(current_user)
        return success_response(data=result)
    except BusinessException as e:
        raise

@router.put("/info", summary="修改用户信息")
async def update_user_info(
    request: schemas.UserUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    修改用户信息接口（仅支持修改昵称）
    文档引用：PROJECT_SPEC.md - 5.1.4节
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"收到修改用户信息请求: user_id={current_user.id}, nickname={request.nickname}")
        result = service.update_user(current_user, request.nickname)
        logger.info(f"用户信息修改成功: user_id={result.get('id')}")
        return success_response(data=result, message="修改成功")
    except BusinessException as e:
        logger.error(f"用户信息修改业务异常: user_id={current_user.id}, error={e.message}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"用户信息修改未知异常: user_id={current_user.id}, error={str(e)}", exc_info=True)
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        raise BusinessException(f"修改失败: {str(e)}", code=500)
