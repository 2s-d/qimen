# 文档引用：PROJECT_SPEC.md - 1573行
# 安全相关（JWT、密码加密）

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os

# 密码加密上下文
# 说明：原设计使用 bcrypt，但在当前运行环境下，bcrypt 后端存在兼容性问题
#（passlib 在检测 bcrypt 后端时会触发 “password cannot be longer than 72 bytes” 异常），
# 这会导致注册/登录全部失败。
# 为保证功能可用，这里改用 pbkdf2_sha256 实现密码哈希。
# TODO: 如后续环境允许，可切回 bcrypt 并重新验证。
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT配置（文档6.2节）
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24  # 文档6.2节：24小时有效期

def hash_password(password: str) -> str:
    """
    使用 PBKDF2-SHA256 加密密码
    文档引用：PROJECT_SPEC.md - 4.2.1节业务规则
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    文档引用：PROJECT_SPEC.md - 4.2.1节业务规则
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT Token
    文档引用：PROJECT_SPEC.md - 6.2节
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    验证JWT Token
    文档引用：PROJECT_SPEC.md - 6.2节
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def decode_token(token: str) -> Optional[dict]:
    """
    解码JWT Token（不验证过期）
    文档引用：PROJECT_SPEC.md - 6.2节
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except JWTError:
        return None
