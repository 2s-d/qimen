"""
奇门遁甲模块API自动化测试
"""
import pytest
import requests
from tests.conftest import API_BASE_URL

class TestQimenAPI:
    """奇门遁甲模块API测试"""
    
    def test_calculate_qimen(self):
        """测试起盘计算"""
        calculate_data = {
            "calendar_type": "solar",
            "year": 2024,
            "month": 1,
            "day": 1,
            "shichen": "子时",
            "gender": "male"
        }
        response = requests.post(f"{API_BASE_URL}/qimen/calculate", json=calculate_data)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "plate" in data["data"]
        assert "fortune" in data["data"]
    
    def test_save_record(self, auth_token):
        """测试保存起盘记录"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        # 先计算一个盘
        calculate_data = {
            "calendar_type": "solar",
            "year": 2024,
            "month": 1,
            "day": 1,
            "shichen": "子时",
            "gender": "male"
        }
        calc_response = requests.post(f"{API_BASE_URL}/qimen/calculate", json=calculate_data)
        calc_data = calc_response.json()
        plate_data = calc_data["data"]["plate"]
        
        # 保存记录
        save_data = {
            "plate": plate_data,
            "fortune": calc_data["data"]["fortune"]
        }
        response = requests.post(f"{API_BASE_URL}/qimen/save", json=save_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "record_id" in data["data"]
    
    def test_get_history_list(self, auth_token):
        """测试获取历史记录列表"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_BASE_URL}/qimen/history?page=1&size=10", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "records" in data["data"]
        assert "total" in data["data"]
        assert isinstance(data["data"]["records"], list)
    
    def test_get_daily_fortune(self):
        """测试获取今日运势"""
        response = requests.get(f"{API_BASE_URL}/qimen/fortune")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "score" in data["data"]
        assert "level" in data["data"]
    
    def test_get_calendar(self):
        """测试获取万年历"""
        response = requests.get(f"{API_BASE_URL}/tools/calendar?year=2024&month=1")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "solar" in data["data"]
        assert "lunar" in data["data"]
    
    def test_get_knowledge_articles(self):
        """测试获取知识文章"""
        response = requests.get(f"{API_BASE_URL}/knowledge/articles?category=入门")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert isinstance(data["data"], list)
