"""
系统模块API自动化测试
"""
import pytest
import requests
from tests.conftest import API_BASE_URL

class TestSystemAPI:
    """系统模块API测试"""
    
    def test_health_check(self):
        """测试健康检查"""
        response = requests.get(f"{API_BASE_URL}/system/health")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "status" in data["data"]
        assert data["data"]["status"] == "healthy"
    
    def test_get_system_config(self):
        """测试获取系统配置"""
        response = requests.get(f"{API_BASE_URL}/system/config")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "app_name" in data["data"]
        assert "version" in data["data"]
    
    def test_get_help_doc(self):
        """测试获取帮助文档"""
        response = requests.get(f"{API_BASE_URL}/system/help")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "content" in data["data"]
    
    def test_get_announcements(self):
        """测试获取公告列表"""
        response = requests.get(f"{API_BASE_URL}/system/announcements")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert isinstance(data["data"], list)
    
    def test_get_statistics(self):
        """测试获取数据统计"""
        response = requests.get(f"{API_BASE_URL}/system/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "total_users" in data["data"]
        assert "total_records" in data["data"]
    
    def test_submit_feedback(self):
        """测试提交意见反馈"""
        feedback_data = {
            "content": "自动化测试反馈",
            "contact": "test@example.com"
        }
        response = requests.post(f"{API_BASE_URL}/system/feedback", json=feedback_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
