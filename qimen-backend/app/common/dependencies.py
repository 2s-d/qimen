# 文档引用：PROJECT_SPEC.md - 1581行
# 公共依赖（认证中间件）

from fastapi import Depends, HTTPException, Header
from typing import Optional
from app.core.security import verify_token
from app.db.session import SessionLocal
from app.modules.user.models import User
from app.common.exceptions import AuthException
from app.common.response import error_response

async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """
    验证Token并返回当前用户
    文档引用：PROJECT_SPEC.md - 6.2.3节
    """
    if not authorization or not authorization.startswith('Bearer '):
        raise AuthException("未提供认证Token", code=401)
    
    token = authorization.split(' ')[1]
    payload = verify_token(token)
    if not payload:
        raise AuthException("Token无效或已过期", code=401)
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise AuthException("Token无效", code=401)
    
    # 从数据库获取用户
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthException("用户不存在", code=401)
        return user
    finally:
        db.close()

async def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[User]:
    """
    可选认证（支持匿名访问）
    文档引用：PROJECT_SPEC.md - 6.2.3节
    """
    if not authorization:
        return None
    try:
        return await get_current_user(authorization)
    except AuthException:
        return None

async def get_db_session():
    """
    获取数据库会话（用于依赖注入）
    文档引用：PROJECT_SPEC.md - 1587行
    """
    from app.db.session import get_db
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
