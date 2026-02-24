"""
用户模块API自动化测试
"""
import pytest
import requests
from tests.conftest import API_BASE_URL

class TestUserAPI:
    """用户模块API测试"""
    
    def test_register_user(self):
        """测试用户注册"""
        import random
        username = f"test_user_{random.randint(10000, 99999)}"
        register_data = {
            "username": username,
            "password": "123456",
            "nickname": "测试用户"
        }
        response = requests.post(f"{API_BASE_URL}/user/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_register_duplicate_user(self):
        """测试注册重复用户名"""
        register_data = {
            "username": "duplicate_test",
            "password": "123456"
        }
        # 第一次注册
        requests.post(f"{API_BASE_URL}/user/register", json=register_data)
        # 第二次注册应该失败
        response = requests.post(f"{API_BASE_URL}/user/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] != 200  # 应该返回错误
    
    def test_login_success(self, auth_token):
        """测试登录成功"""
        # auth_token fixture 已经登录，这里验证token有效
        assert auth_token is not None
        assert len(auth_token) > 0
    
    def test_login_failed(self):
        """测试登录失败"""
        login_data = {
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
        response = requests.post(f"{API_BASE_URL}/user/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] != 200  # 应该返回错误
    
    def test_get_user_info(self, auth_token):
        """测试获取用户信息"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_BASE_URL}/user/info", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "username" in data["data"]
        assert "nickname" in data["data"]
    
    def test_update_user_info(self, auth_token):
        """测试更新用户信息"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        update_data = {
            "nickname": "更新后的昵称"
        }
        response = requests.put(f"{API_BASE_URL}/user/info", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
