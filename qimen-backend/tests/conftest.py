"""
测试配置和fixtures
"""
import pytest
import requests
from typing import Generator

# 测试配置
BASE_URL = "http://localhost:8087"
API_BASE_URL = f"{BASE_URL}/api"

@pytest.fixture(scope="session")
def api_base_url() -> str:
    """API基础URL"""
    return API_BASE_URL

@pytest.fixture(scope="function")
def auth_token(api_base_url: str) -> Generator[str, None, None]:
    """
    获取认证token（注册并登录测试用户）
    测试结束后清理测试用户（可选）
    """
    # 注册测试用户
    test_username = "test_auto_user"
    test_password = "test123456"
    
    register_data = {
        "username": test_username,
        "password": test_password,
        "nickname": "自动化测试用户"
    }
    
    try:
        # 尝试注册
        response = requests.post(f"{api_base_url}/user/register", json=register_data)
        # 忽略已存在的错误
    except:
        pass
    
    # 登录获取token
    login_data = {
        "username": test_username,
        "password": test_password
    }
    
    response = requests.post(f"{api_base_url}/user/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    token = data["data"]["token"]
    
    yield token
    
    # 测试结束后可选的清理逻辑
    # 注意：实际项目中可能需要删除测试用户
