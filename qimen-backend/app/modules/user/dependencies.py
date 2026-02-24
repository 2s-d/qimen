# 文档引用：PROJECT_SPEC.md - 1551行
# 用户模块依赖

from fastapi import Depends, Header
from typing import Optional
from app.modules.user.models import User
from app.common.dependencies import get_current_user as base_get_current_user

# 用户模块的get_current_user直接使用公共依赖
get_current_user = base_get_current_user
