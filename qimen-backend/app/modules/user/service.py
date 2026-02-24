# 文档引用：PROJECT_SPEC.md - 1550行
# 用户业务逻辑

from app.db.session import SessionLocal
from app.modules.user.models import User
from app.modules.qimen.models import QimenRecord
from app.core.security import hash_password, verify_password, create_access_token
from app.common.exceptions import BusinessException, AuthException, ValidationException, NotFoundException
from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def create_user(username: str, password: str, nickname: Optional[str] = None) -> dict:
    """
    创建用户
    文档引用：PROJECT_SPEC.md - 5.1.1节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：参数验证（已在schemas中完成）
        
        # 步骤2：检查用户名唯一性
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise BusinessException("用户名已存在", code=400)
        
        # 步骤3：密码加密
        password_hash = hash_password(password)
        
        # 步骤4：创建用户记录
        user = User(
            username=username,
            password_hash=password_hash,
            nickname=nickname or username,  # 昵称为空时使用用户名
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"用户注册成功: user_id={user.id}, username={username}")
        
        # 步骤5：返回结果
        return {
            "user_id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    except BusinessException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建用户失败: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"异常堆栈: {traceback.format_exc()}")
        raise BusinessException(f"注册失败: {str(e)}", code=500)
    finally:
        db.close()

def authenticate_user(username: str, password: str) -> dict:
    """
    验证用户（登录）
    文档引用：PROJECT_SPEC.md - 5.1.2节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：查询用户
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise AuthException("账号或密码错误", code=401)
        
        # 步骤2：验证密码
        if not verify_password(password, user.password_hash):
            raise AuthException("账号或密码错误", code=401)
        
        # 步骤3：生成JWT token
        token_data = {
            "user_id": user.id,
            "username": user.username
        }
        token = create_access_token(token_data)
        
        # 步骤4：统计起盘次数
        qipan_count = db.query(QimenRecord).filter(QimenRecord.user_id == user.id).count()
        
        logger.info(f"用户登录成功: user_id={user.id}, username={username}")
        
        # 步骤5：返回结果
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "qipan_count": qipan_count
            }
        }
    except AuthException:
        raise
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}", exc_info=True)
        raise AuthException("登录失败", code=500)
    finally:
        db.close()

def get_user_info(user: User) -> dict:
    """
    获取用户信息
    文档引用：PROJECT_SPEC.md - 5.1.3节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：获取用户基本信息（已从依赖注入获得）
        
        # 步骤2：统计起盘次数
        qipan_count = db.query(QimenRecord).filter(QimenRecord.user_id == user.id).count()
        
        # 步骤3：返回结果
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "qipan_count": qipan_count,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}", exc_info=True)
        raise BusinessException("获取用户信息失败", code=500)
    finally:
        db.close()

def update_user(user: User, nickname: str) -> dict:
    """
    更新用户信息（仅支持修改昵称）
    文档引用：PROJECT_SPEC.md - 5.1.4节业务逻辑
    """
    db = SessionLocal()
    try:
        # 步骤1：参数验证（已在schemas中完成）
        logger.info(f"开始更新用户信息: user_id={user.id}, nickname={nickname}")
        
        # 步骤2：从当前会话中重新查询用户对象（解决会话绑定问题）
        db_user = db.query(User).filter(User.id == user.id).first()
        if not db_user:
            logger.error(f"用户不存在: user_id={user.id}")
            raise NotFoundException("用户不存在", code=404)
        
        # 步骤3：更新数据库
        db_user.nickname = nickname
        # updated_at 由数据库自动更新（onupdate=func.current_timestamp()）
        # 不需要手动设置 updated_at = datetime.now()
        
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"用户信息更新成功: user_id={db_user.id}, nickname={db_user.nickname}")
        
        # 步骤4：返回结果
        return {
            "id": db_user.id,
            "username": db_user.username,
            "nickname": db_user.nickname,
            "updated_at": db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    except BusinessException:
        db.rollback()
        raise
    except NotFoundException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_detail = f"更新用户信息失败: {str(e)}\n异常类型: {type(e).__name__}\n堆栈信息: {traceback.format_exc()}"
        logger.error(error_detail, exc_info=True)
        raise BusinessException(f"更新失败: {str(e)}", code=500)
    finally:
        db.close()

def get_user_by_id(user_id: int) -> Optional[User]:
    """
    根据ID获取用户
    """
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def get_user_by_username(username: str) -> Optional[User]:
    """
    根据用户名获取用户
    """
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()
