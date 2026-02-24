#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""直接测试用户注册功能"""

import sys
import traceback
from app.modules.user import service

try:
    print("测试用户注册...")
    result = service.create_user(
        username="test_user_123",
        password="123456",
        nickname="测试用户"
    )
    print("✓ 注册成功!")
    print(f"结果: {result}")
except Exception as e:
    print(f"✗ 注册失败: {e}")
    print(f"异常类型: {type(e).__name__}")
    traceback.print_exc()
