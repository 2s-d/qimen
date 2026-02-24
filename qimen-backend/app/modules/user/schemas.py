# 文档引用：PROJECT_SPEC.md - 1549行
# 用户请求/响应模式

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserRegisterRequest(BaseModel):
    """
    用户注册请求
    文档引用：PROJECT_SPEC.md - 5.1.1节
    """
    username: str = Field(..., min_length=3, max_length=20, description="用户名（3-20位，字母数字下划线）")
    password: str = Field(..., min_length=6, max_length=20, description="密码（6-20位）")
    nickname: Optional[str] = Field(None, min_length=2, max_length=10, description="昵称（2-10位，可选）")
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式：3-20位，只能包含字母、数字、下划线"""
        import re
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('用户名只能包含字母、数字、下划线，长度3-20位')
        return v

class UserLoginRequest(BaseModel):
    """
    用户登录请求
    文档引用：PROJECT_SPEC.md - 5.1.2节
    """
    username: str = Field(..., description="用户名")
    password: str = Field(..., min_length=6, description="密码（≥6位）")

class UserLoginResponse(BaseModel):
    """
    用户登录响应
    文档引用：PROJECT_SPEC.md - 5.1.2节
    """
    token: str
    user: dict

class UserInfoResponse(BaseModel):
    """
    用户信息响应
    文档引用：PROJECT_SPEC.md - 5.1.3节
    """
    id: int
    username: str
    nickname: Optional[str]
    qipan_count: int
    created_at: str

class UserUpdateRequest(BaseModel):
    """
    用户更新请求（仅支持修改昵称）
    文档引用：PROJECT_SPEC.md - 5.1.4节
    """
    nickname: str = Field(..., min_length=2, max_length=10, description="昵称（2-10位）")

class UserUpdateResponse(BaseModel):
    """
    用户更新响应
    文档引用：PROJECT_SPEC.md - 5.1.4节
    """
    id: int
    username: str
    nickname: str
    updated_at: str
