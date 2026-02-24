#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试所有18个API接口
用于验证接口是否能正常调用和返回正确响应
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

# 添加项目路径以便导入后端模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入数据库相关模块用于验证
try:
    from app.db.session import SessionLocal
    from app.modules.user.models import User
    from app.modules.qimen.models import QimenRecord, KnowledgeArticle
    from app.modules.system.models import SystemConfig, Announcement, Feedback
    DB_VERIFICATION_ENABLED = True
except ImportError as e:
    print(f"⚠️  警告: 无法导入数据库模块，将跳过数据库验证: {e}")
    DB_VERIFICATION_ENABLED = False

# 配置
# 注意：根据后端日志，服务运行在端口 8087
BASE_URL = "http://localhost:8087"
# BASE_URL = "http://localhost:8000"  # 如果后端运行在不同端口，修改这里

# 调试模式（显示详细的请求/响应信息）
DEBUG_MODE = False  # 设置为 True 可以看到详细的请求和响应信息

# 数据库验证模式（验证接口是否真的修改了数据库）
DB_VERIFY_MODE = True  # 设置为 True 会验证数据库状态

# 测试结果统计
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

# 全局变量
token: Optional[str] = None
user_id: Optional[int] = None
record_id: Optional[int] = None
plate_data: Optional[Dict[str, Any]] = None
test_username: Optional[str] = None  # 用于数据库验证
test_nickname: Optional[str] = None  # 用于数据库验证


def print_test_header(test_name: str):
    """打印测试标题"""
    print("\n" + "=" * 60)
    print(f"测试: {test_name}")
    print("=" * 60)


def print_result(success: bool, message: str, details: str = "", db_verify: str = ""):
    """打印测试结果"""
    test_results["total"] += 1
    if success:
        test_results["passed"] += 1
        status = "✓ 通过"
    else:
        test_results["failed"] += 1
        test_results["errors"].append(f"{test_results['total']}. {message}")
        status = "✗ 失败"
    
    print(f"{status}: {message}")
    if details:
        # 如果详情很长，格式化输出
        if "\n" in details:
            print(f"  详情:\n{details}")
        else:
            print(f"  详情: {details}")
    if db_verify:
        print(f"  [数据库验证] {db_verify}")
    print()


def verify_db_user_exists(username: str, expected_nickname: Optional[str] = None) -> tuple[bool, str]:
    """验证数据库中用户是否存在"""
    if not DB_VERIFICATION_ENABLED or not DB_VERIFY_MODE:
        return True, "数据库验证已禁用"
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False, f"用户不存在: {username}"
        
        verify_info = f"用户ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}"
        
        if expected_nickname and user.nickname != expected_nickname:
            return False, f"昵称不匹配: 期望 '{expected_nickname}', 实际 '{user.nickname}'"
        
        return True, verify_info
    except Exception as e:
        return False, f"数据库查询失败: {str(e)}"
    finally:
        db.close()


def verify_db_record_exists(record_id: int, user_id: int) -> tuple[bool, str]:
    """验证数据库中记录是否存在"""
    if not DB_VERIFICATION_ENABLED or not DB_VERIFY_MODE:
        return True, "数据库验证已禁用"
    
    db = SessionLocal()
    try:
        record = db.query(QimenRecord).filter(
            QimenRecord.id == record_id,
            QimenRecord.user_id == user_id
        ).first()
        if not record:
            return False, f"记录不存在: record_id={record_id}, user_id={user_id}"
        
        return True, f"记录存在: ID={record.id}, 日期={record.datetime}, 性别={record.gender}"
    except Exception as e:
        return False, f"数据库查询失败: {str(e)}"
    finally:
        db.close()


def verify_db_record_deleted(record_id: int) -> tuple[bool, str]:
    """验证数据库中记录是否已删除"""
    if not DB_VERIFICATION_ENABLED or not DB_VERIFY_MODE:
        return True, "数据库验证已禁用"
    
    db = SessionLocal()
    try:
        record = db.query(QimenRecord).filter(QimenRecord.id == record_id).first()
        if record:
            return False, f"记录仍然存在: record_id={record_id}"
        return True, f"记录已删除: record_id={record_id}"
    except Exception as e:
        return False, f"数据库查询失败: {str(e)}"
    finally:
        db.close()


def verify_db_feedback_exists(feedback_id: int) -> tuple[bool, str]:
    """验证数据库中反馈是否存在"""
    if not DB_VERIFICATION_ENABLED or not DB_VERIFY_MODE:
        return True, "数据库验证已禁用"
    
    db = SessionLocal()
    try:
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            return False, f"反馈不存在: feedback_id={feedback_id}"
        return True, f"反馈存在: ID={feedback.id}, 内容长度={len(feedback.content)}"
    except Exception as e:
        return False, f"数据库查询失败: {str(e)}"
    finally:
        db.close()


def verify_user_count_increased(before_count: int) -> tuple[bool, str]:
    """验证用户数量是否增加"""
    if not DB_VERIFICATION_ENABLED or not DB_VERIFY_MODE:
        return True, "数据库验证已禁用"
    
    db = SessionLocal()
    try:
        current_count = db.query(User).count()
        if current_count <= before_count:
            return False, f"用户数量未增加: 之前={before_count}, 现在={current_count}"
        return True, f"用户数量已增加: 之前={before_count}, 现在={current_count}"
    except Exception as e:
        return False, f"数据库查询失败: {str(e)}"
    finally:
        db.close()


def test_api(method: str, url: str, data: Optional[Dict] = None, 
             headers: Optional[Dict] = None, expected_status: int = 200) -> Optional[Dict]:
    """通用API测试函数"""
    try:
        if headers is None:
            headers = {"Content-Type": "application/json"}
        
        # 打印请求信息（调试用）
        if DEBUG_MODE:
            print(f"  [DEBUG] 请求: {method.upper()} {url}")
            if data:
                print(f"  [DEBUG] 数据: {json.dumps(data, ensure_ascii=False)[:100]}...")
            if headers:
                print(f"  [DEBUG] 请求头: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, ensure_ascii=False)}")
        
        if method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
        
        if DEBUG_MODE:
            print(f"  [DEBUG] 响应状态码: {response.status_code}")
            try:
                print(f"  [DEBUG] 响应内容: {json.dumps(response.json(), ensure_ascii=False)[:200]}...")
            except:
                print(f"  [DEBUG] 响应内容: {response.text[:200]}...")
        
        # 检查状态码
        if response.status_code != expected_status:
            error_detail = f"状态码错误: 期望 {expected_status}, 实际 {response.status_code}"
            error_detail += f"\n  请求URL: {url}"
            if data:
                error_detail += f"\n  请求数据: {json.dumps(data, ensure_ascii=False)[:200]}"
            
            try:
                error_json = response.json()
                if "message" in error_json:
                    error_detail += f"\n  错误信息: {error_json.get('message')}"
                if "detail" in error_json:
                    error_detail += f"\n  详细信息: {error_json.get('detail')}"
                if "code" in error_json:
                    error_detail += f"\n  错误码: {error_json.get('code')}"
                # 对于500错误，显示完整响应以便调试
                if response.status_code == 500:
                    error_detail += f"\n  [500错误] 完整响应: {json.dumps(error_json, ensure_ascii=False, indent=2)}"
                # 打印完整响应（用于调试）
                elif DEBUG_MODE:
                    error_detail += f"\n  完整响应: {json.dumps(error_json, ensure_ascii=False)}"
            except:
                error_detail += f"\n  响应内容: {response.text[:500]}"
                if response.status_code == 500:
                    error_detail += f"\n  [500错误] 完整响应文本: {response.text}"
            
            return {
                "success": False,
                "error": error_detail,
                "status_code": response.status_code,
                "response": response.text[:1000]  # 增加响应长度以便查看完整错误
            }
        
        # 尝试解析JSON
        try:
            result = response.json()
        except Exception as e:
            return {
                "success": False,
                "error": f"响应不是有效的JSON: {str(e)}\n  响应内容: {response.text[:200]}",
                "status_code": response.status_code,
                "response": response.text[:500]
            }
        
        # 检查响应格式
        if "code" in result:
            if result["code"] != 200:
                return {
                    "success": False,
                    "error": f"业务错误: code={result.get('code')}, message={result.get('message', '')}",
                    "status_code": response.status_code,
                    "response": result
                }
        
        return {
            "success": True,
            "data": result.get("data") if "data" in result else result,
            "response": result
        }
    
    except requests.exceptions.Timeout as e:
        return {
            "success": False,
            "error": f"请求超时（10秒）\n  URL: {url}\n  请检查后端服务是否响应缓慢或网络连接问题"
        }
    except requests.exceptions.ConnectionError as e:
        error_msg = f"连接失败\n"
        error_msg += f"  URL: {url}\n"
        error_msg += f"  错误类型: {type(e).__name__}\n"
        error_msg += f"  错误详情: {str(e)}\n"
        error_msg += f"\n  可能的原因：\n"
        error_msg += f"  1. 后端服务未启动（检查端口 {url.split(':')[-1].split('/')[0]} 是否被占用）\n"
        error_msg += f"  2. 端口号不正确（当前使用: {BASE_URL}）\n"
        error_msg += f"  3. 防火墙阻止连接\n"
        error_msg += f"  4. 后端服务运行在不同地址\n"
        error_msg += f"\n  建议：\n"
        error_msg += f"  - 检查后端是否运行: 在浏览器访问 {BASE_URL}/api/health\n"
        error_msg += f"  - 检查后端日志: 查看后端终端输出\n"
        error_msg += f"  - 修改 BASE_URL: 如果后端运行在不同端口，编辑脚本修改 BASE_URL"
        return {
            "success": False,
            "error": error_msg
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求异常: {type(e).__name__}\n  详情: {str(e)}\n  URL: {url}"
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": f"未知异常: {type(e).__name__}\n  详情: {str(e)}\n  堆栈: {traceback.format_exc()[:300]}"
        }


# ========== 用户模块测试（4个接口） ==========

def test_user_register():
    """测试1: POST /api/user/register - 用户注册"""
    print_test_header("用户注册")
    
    global test_username, test_nickname
    
    # 获取注册前的用户数量
    before_count = 0
    if DB_VERIFICATION_ENABLED and DB_VERIFY_MODE:
        db = SessionLocal()
        try:
            before_count = db.query(User).count()
        except:
            pass
        finally:
            db.close()
    
    # 生成唯一用户名
    username = f"test_user_{int(time.time())}"
    test_username = username
    test_nickname = "测试用户"
    
    data = {
        "username": username,
        "password": "123456",
        "nickname": test_nickname
    }
    
    result = test_api("POST", f"{BASE_URL}/api/user/register", data=data)
    
    if result and result["success"]:
        # 验证返回数据
        response_data = result.get("data", {})
        verify_details = []
        
        # 验证返回数据字段
        if "user_id" not in response_data:
            verify_details.append("❌ 返回数据缺少 user_id 字段")
        if "username" not in response_data:
            verify_details.append("❌ 返回数据缺少 username 字段")
        if response_data.get("username") != username:
            verify_details.append(f"❌ 返回的用户名不匹配: 期望 {username}, 实际 {response_data.get('username')}")
        if response_data.get("nickname") != test_nickname:
            verify_details.append(f"❌ 返回的昵称不匹配: 期望 {test_nickname}, 实际 {response_data.get('nickname')}")
        
        # 验证数据库
        db_success, db_info = verify_db_user_exists(username, test_nickname)
        if not db_success:
            verify_details.append(f"❌ {db_info}")
        
        # 验证用户数量增加
        count_success, count_info = verify_user_count_increased(before_count)
        if not count_success:
            verify_details.append(f"❌ {count_info}")
        
        if verify_details:
            details = f"用户名: {username}\n" + "\n".join(verify_details)
            print_result(False, "用户注册部分成功但验证失败", details)
            return False
        else:
            details = f"用户名: {username}, 用户ID: {response_data.get('user_id')}"
            db_verify = f"✓ {db_info} | ✓ {count_info}"
            print_result(True, "用户注册成功", details, db_verify)
            return True
    else:
        print_result(False, "用户注册失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_user_login():
    """测试2: POST /api/user/login - 用户登录"""
    print_test_header("用户登录")
    
    global token, user_id, test_username
    
    # 先注册一个用户
    username = f"test_user_{int(time.time())}"
    test_username = username
    register_data = {
        "username": username,
        "password": "123456",
        "nickname": "测试用户"
    }
    
    register_result = test_api("POST", f"{BASE_URL}/api/user/register", data=register_data)
    if not register_result or not register_result["success"]:
        print_result(False, "注册失败，无法测试登录", register_result.get("error", "") if register_result else "")
        return False
    
    # 测试登录
    login_data = {
        "username": username,
        "password": "123456"
    }
    
    result = test_api("POST", f"{BASE_URL}/api/user/login", data=login_data)
    
    if result and result["success"]:
        login_response = result["response"]
        verify_details = []
        
        # 验证返回数据结构
        if "data" not in login_response:
            verify_details.append("❌ 响应缺少 data 字段")
        elif "token" not in login_response["data"]:
            verify_details.append("❌ 响应缺少 token 字段")
        elif "user" not in login_response["data"]:
            verify_details.append("❌ 响应缺少 user 字段")
        else:
            token = login_response["data"]["token"]
            user_data = login_response["data"]["user"]
            user_id = user_data.get("id")
            
            # 验证token不为空
            if not token or len(token) < 10:
                verify_details.append(f"❌ Token无效: 长度={len(token) if token else 0}")
            
            # 验证用户信息
            if user_data.get("username") != username:
                verify_details.append(f"❌ 用户信息不匹配: 期望 {username}, 实际 {user_data.get('username')}")
            if "qipan_count" not in user_data:
                verify_details.append("❌ 用户信息缺少 qipan_count 字段")
            
            # 验证数据库中的用户
            db_success, db_info = verify_db_user_exists(username)
            if not db_success:
                verify_details.append(f"❌ {db_info}")
        
        if verify_details:
            details = "\n".join(verify_details)
            print_result(False, "登录部分成功但验证失败", details)
            return False
        else:
            details = f"Token已保存，用户ID: {user_id}, Token长度: {len(token)}"
            db_verify = f"✓ {db_info} | ✓ Token有效"
            print_result(True, "用户登录成功", details, db_verify)
            return True
    else:
        print_result(False, "用户登录失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_user_info():
    """测试3: GET /api/user/info - 获取用户信息"""
    print_test_header("获取用户信息")
    
    global token
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    result = test_api("GET", f"{BASE_URL}/api/user/info", headers=headers)
    
    if result and result["success"]:
        user_info = result["data"]
        print_result(True, "获取用户信息成功", 
                    f"用户名: {user_info.get('username')}, 昵称: {user_info.get('nickname')}")
        return True
    else:
        print_result(False, "获取用户信息失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_user_update():
    """测试4: PUT /api/user/info - 修改用户信息"""
    print_test_header("修改用户信息")
    
    global token, test_username, test_nickname
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    # 获取修改前的昵称（如果存在）
    old_nickname = test_nickname if test_nickname else "未知"
    # 昵称长度限制：2-10 个字符，这里生成不超过10字符的安全昵称
    new_nickname = f"新昵称{int(time.time()) % 1000}"  # 例如: 新昵称123
    # 确保长度不超过10个字符
    new_nickname = new_nickname[:10]
    test_nickname = new_nickname
    
    data = {
        "nickname": new_nickname
    }
    
    result = test_api("PUT", f"{BASE_URL}/api/user/info", data=data, headers=headers)
    
    if result and result["success"]:
        updated_info = result["data"]
        verify_details = []
        
        # 验证返回数据
        if updated_info.get("nickname") != new_nickname:
            verify_details.append(f"❌ 返回的昵称不匹配: 期望 {new_nickname}, 实际 {updated_info.get('nickname')}")
        if "updated_at" not in updated_info:
            verify_details.append("❌ 返回数据缺少 updated_at 字段")
        if updated_info.get("id") != user_id:
            verify_details.append(f"❌ 返回的用户ID不匹配: 期望 {user_id}, 实际 {updated_info.get('id')}")
        
        # 验证数据库中的昵称是否真的更新了
        db_success, db_info = verify_db_user_exists(test_username, new_nickname)
        if not db_success:
            verify_details.append(f"❌ {db_info}")
        
        if verify_details:
            details = "\n".join(verify_details)
            print_result(False, "修改部分成功但验证失败", details)
            return False
        else:
            details = f"新昵称: {new_nickname}, 旧昵称: {old_nickname}"
            db_verify = f"✓ {db_info}"
            print_result(True, "修改用户信息成功", details, db_verify)
            return True
    else:
        print_result(False, "修改用户信息失败", result.get("error", "未知错误") if result else "无响应")
        return False


# ========== 奇门模块测试（8个接口） ==========

def test_qimen_calculate():
    """测试5: POST /api/qimen/calculate - 起盘计算"""
    print_test_header("起盘计算")
    
    global plate_data
    
    # 使用当前日期时间
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M")
    
    data = {
        "datetime": datetime_str,
        "gender": "男",
        "type": "时家奇门",
        "calendar_type": "公历"
    }
    
    result = test_api("POST", f"{BASE_URL}/api/qimen/calculate", data=data)
    
    if result and result["success"]:
        plate_data = result["data"]
        chief_star = plate_data.get("chief_star", "")
        chief_door = plate_data.get("chief_door", "")
        palaces_count = len(plate_data.get("palaces", []))
        
        print_result(True, "起盘计算成功", 
                    f"值符: {chief_star}, 值使: {chief_door}, 宫位数: {palaces_count}")
        return True
    else:
        print_result(False, "起盘计算失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_save():
    """测试6: POST /api/qimen/save - 保存起盘记录"""
    print_test_header("保存起盘记录")
    
    global token, plate_data, record_id
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    if not plate_data:
        print_result(False, "缺少盘面数据，请先计算", "")
        return False
    
    # 获取保存前的记录数量
    before_count = 0
    if DB_VERIFICATION_ENABLED and DB_VERIFY_MODE:
        db = SessionLocal()
        try:
            before_count = db.query(QimenRecord).filter(QimenRecord.user_id == user_id).count()
        except:
            pass
        finally:
            db.close()
    
    # 提取运势数据
    fortune_data = plate_data.get("fortune_data", {})
    overall_score = fortune_data.get("overall_score", 3.0)
    
    data = {
        "datetime": plate_data.get("datetime"),
        "gender": plate_data.get("gender"),
        "type": plate_data.get("type"),
        "plate_data": plate_data,
        "fortune_data": fortune_data,
        "fortune_score": overall_score
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    result = test_api("POST", f"{BASE_URL}/api/qimen/save", data=data, headers=headers)
    
    if result and result["success"]:
        saved_data = result["data"]
        record_id = saved_data.get("id")
        verify_details = []
        
        # 验证返回数据
        if not record_id:
            verify_details.append("❌ 返回数据缺少 id 字段")
        if "created_at" not in saved_data:
            verify_details.append("❌ 返回数据缺少 created_at 字段")
        
        # 验证数据库中的记录
        db_success, db_info = verify_db_record_exists(record_id, user_id)
        if not db_success:
            verify_details.append(f"❌ {db_info}")
        
        # 验证记录数量增加
        if DB_VERIFICATION_ENABLED and DB_VERIFY_MODE:
            db = SessionLocal()
            try:
                after_count = db.query(QimenRecord).filter(QimenRecord.user_id == user_id).count()
                if after_count <= before_count:
                    verify_details.append(f"❌ 记录数量未增加: 之前={before_count}, 现在={after_count}")
            except Exception as e:
                verify_details.append(f"❌ 验证记录数量失败: {str(e)}")
            finally:
                db.close()
        
        if verify_details:
            details = f"记录ID: {record_id}\n" + "\n".join(verify_details)
            print_result(False, "保存部分成功但验证失败", details)
            return False
        else:
            details = f"记录ID: {record_id}, 创建时间: {saved_data.get('created_at')}"
            db_verify = f"✓ {db_info}"
            print_result(True, "保存起盘记录成功", details, db_verify)
            return True
    else:
        print_result(False, "保存起盘记录失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_history_list():
    """测试7: GET /api/qimen/history - 获取历史记录列表"""
    print_test_header("获取历史记录列表")
    
    global token
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": 1, "size": 10}
    
    result = test_api("GET", f"{BASE_URL}/api/qimen/history", data=params, headers=headers)
    
    if result and result["success"]:
        history_data = result["data"]
        total = history_data.get("total", 0)
        items = history_data.get("items", [])
        print_result(True, "获取历史记录列表成功", 
                    f"总数: {total}, 当前页: {len(items)}条")
        return True
    else:
        print_result(False, "获取历史记录列表失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_history_detail():
    """测试8: GET /api/qimen/history/{id} - 获取历史记录详情"""
    print_test_header("获取历史记录详情")
    
    global token, record_id
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    if not record_id:
        print_result(False, "缺少记录ID，请先保存记录", "")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    result = test_api("GET", f"{BASE_URL}/api/qimen/history/{record_id}", headers=headers)
    
    if result and result["success"]:
        detail_data = result["data"]
        print_result(True, "获取历史记录详情成功", 
                    f"记录ID: {detail_data.get('id')}, 日期: {detail_data.get('datetime')}")
        return True
    else:
        print_result(False, "获取历史记录详情失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_fortune():
    """测试9: GET /api/qimen/fortune - 获取今日运势"""
    print_test_header("获取今日运势")
    
    result = test_api("GET", f"{BASE_URL}/api/qimen/fortune")
    
    if result and result["success"]:
        fortune_data = result["data"]
        overall_score = fortune_data.get("overall_score", 0)
        overall_fortune = fortune_data.get("overall_fortune", "")
        print_result(True, "获取今日运势成功", 
                    f"总体评分: {overall_score}, 吉凶: {overall_fortune}")
        return True
    else:
        print_result(False, "获取今日运势失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_calendar():
    """测试10: GET /api/qimen/tools/calendar - 获取万年历数据"""
    print_test_header("获取万年历数据")
    
    now = datetime.now()
    params = {
        "year": now.year,
        "month": now.month
    }
    
    result = test_api("GET", f"{BASE_URL}/api/qimen/tools/calendar", data=params)
    
    if result and result["success"]:
        calendar_data = result["data"]
        days_count = len(calendar_data.get("days", []))
        print_result(True, "获取万年历数据成功", 
                    f"年份: {calendar_data.get('year')}, 月份: {calendar_data.get('month')}, 天数: {days_count}")
        return True
    else:
        print_result(False, "获取万年历数据失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_qimen_knowledge():
    """测试11: GET /api/qimen/knowledge/articles - 获取知识文章"""
    print_test_header("获取知识文章")
    
    categories = ["入门", "八门", "九星", "八神", "应用"]
    success_count = 0
    
    for category in categories:
        params = {"category": category}
        result = test_api("GET", f"{BASE_URL}/api/qimen/knowledge/articles", data=params)
        
        if result and result["success"]:
            articles = result["data"]
            success_count += 1
            print(f"  ✓ {category}: {len(articles)}篇文章")
        else:
            print(f"  ✗ {category}: {result.get('error', '未知错误') if result else '无响应'}")
    
    if success_count == len(categories):
        print_result(True, "获取知识文章成功", f"所有分类({len(categories)}个)都成功")
        return True
    else:
        print_result(False, "获取知识文章部分失败", f"成功: {success_count}/{len(categories)}")
        return False


def test_qimen_delete():
    """测试12: DELETE /api/qimen/history/{id} - 删除历史记录"""
    print_test_header("删除历史记录")
    
    global token, record_id
    
    if not token:
        print_result(False, "缺少token，请先登录", "")
        return False
    
    if not record_id:
        print_result(False, "缺少记录ID，请先保存记录", "")
        return False
    
    # 先验证记录存在
    db_exists_before, _ = verify_db_record_exists(record_id, user_id)
    
    headers = {"Authorization": f"Bearer {token}"}
    result = test_api("DELETE", f"{BASE_URL}/api/qimen/history/{record_id}", headers=headers)
    
    if result and result["success"]:
        verify_details = []
        
        # 验证数据库中的记录是否真的被删除
        db_success, db_info = verify_db_record_deleted(record_id)
        if not db_success:
            verify_details.append(f"❌ {db_info}")
        
        if not db_exists_before:
            verify_details.append("⚠️  警告: 删除前记录就不存在")
        
        if verify_details:
            details = f"记录ID: {record_id}\n" + "\n".join(verify_details)
            print_result(False, "删除部分成功但验证失败", details)
            return False
        else:
            details = f"记录ID: {record_id}"
            db_verify = f"✓ {db_info}"
            print_result(True, "删除历史记录成功", details, db_verify)
            record_id = None  # 清除已删除的记录ID
            return True
    else:
        print_result(False, "删除历史记录失败", result.get("error", "未知错误") if result else "无响应")
        return False


# ========== 系统模块测试（6个接口） ==========

def test_system_config():
    """测试13: GET /api/system/config - 获取系统配置"""
    print_test_header("获取系统配置")
    
    result = test_api("GET", f"{BASE_URL}/api/system/config")
    
    if result and result["success"]:
        config_data = result["data"]
        version = config_data.get("app_version", "")
        print_result(True, "获取系统配置成功", f"版本号: {version}")
        return True
    else:
        print_result(False, "获取系统配置失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_system_help():
    """测试14: GET /api/system/help - 获取帮助文档"""
    print_test_header("获取帮助文档")
    
    result = test_api("GET", f"{BASE_URL}/api/system/help")
    
    if result and result["success"]:
        help_data = result["data"]
        questions_count = len(help_data.get("questions", []))
        print_result(True, "获取帮助文档成功", f"问题数量: {questions_count}")
        return True
    else:
        print_result(False, "获取帮助文档失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_system_feedback():
    """测试15: POST /api/system/feedback - 提交反馈"""
    print_test_header("提交反馈")
    
    feedback_content = "这是一个测试反馈，用于验证反馈接口是否正常工作。反馈内容需要至少10个字符。"
    feedback_contact = "test@example.com"
    
    data = {
        "content": feedback_content,
        "contact": feedback_contact
    }
    
    result = test_api("POST", f"{BASE_URL}/api/system/feedback", data=data)
    
    if result and result["success"]:
        feedback_data = result["data"]
        feedback_id = feedback_data.get("id")
        verify_details = []
        
        # 验证返回数据
        if not feedback_id:
            verify_details.append("❌ 返回数据缺少 id 字段")
        if "created_at" not in feedback_data:
            verify_details.append("❌ 返回数据缺少 created_at 字段")
        
        # 验证数据库中的反馈
        db_success, db_info = verify_db_feedback_exists(feedback_id)
        if not db_success:
            verify_details.append(f"❌ {db_info}")
        else:
            # 验证反馈内容
            if DB_VERIFICATION_ENABLED and DB_VERIFY_MODE:
                db = SessionLocal()
                try:
                    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
                    if feedback and feedback.content != feedback_content:
                        verify_details.append(f"❌ 反馈内容不匹配")
                    if feedback and feedback.contact != feedback_contact:
                        verify_details.append(f"❌ 联系方式不匹配")
                except Exception as e:
                    verify_details.append(f"❌ 验证反馈内容失败: {str(e)}")
                finally:
                    db.close()
        
        if verify_details:
            details = f"反馈ID: {feedback_id}\n" + "\n".join(verify_details)
            print_result(False, "提交部分成功但验证失败", details)
            return False
        else:
            details = f"反馈ID: {feedback_id}, 创建时间: {feedback_data.get('created_at')}"
            db_verify = f"✓ {db_info}"
            print_result(True, "提交反馈成功", details, db_verify)
            return True
    else:
        print_result(False, "提交反馈失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_system_announcements():
    """测试16: GET /api/system/announcements - 获取公告列表"""
    print_test_header("获取公告列表")
    
    result = test_api("GET", f"{BASE_URL}/api/system/announcements")
    
    if result and result["success"]:
        announcements = result["data"]
        print_result(True, "获取公告列表成功", f"公告数量: {len(announcements)}")
        return True
    else:
        print_result(False, "获取公告列表失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_system_statistics():
    """测试17: GET /api/system/statistics - 获取统计数据"""
    print_test_header("获取统计数据")
    
    result = test_api("GET", f"{BASE_URL}/api/system/statistics")
    
    if result and result["success"]:
        stats_data = result["data"]
        total_users = stats_data.get("total_users", 0)
        total_qipan = stats_data.get("total_qipan", 0)
        print_result(True, "获取统计数据成功", 
                    f"总用户数: {total_users}, 总起盘次数: {total_qipan}")
        return True
    else:
        print_result(False, "获取统计数据失败", result.get("error", "未知错误") if result else "无响应")
        return False


def test_system_health():
    """测试18: GET /api/system/health - 健康检查"""
    print_test_header("健康检查")
    
    result = test_api("GET", f"{BASE_URL}/api/system/health")
    
    if result and result["success"]:
        health_data = result["data"]
        status = health_data.get("status", "")
        database = health_data.get("database", "")
        print_result(True, "健康检查成功", f"服务状态: {status}, 数据库: {database}")
        return True
    else:
        print_result(False, "健康检查失败", result.get("error", "未知错误") if result else "无响应")
        return False


# ========== 主测试函数 ==========

def check_backend_health():
    """检查后端服务是否可用"""
    print("\n" + "=" * 60)
    print("检查后端服务连接...")
    print("=" * 60)
    
    try:
        # 先测试根路径
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✓ 根路径连接成功 (状态码: {response.status_code})")
        
        # 测试健康检查接口
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ 健康检查接口正常 (状态码: {response.status_code})")
            try:
                health_data = response.json()
                print(f"  响应: {json.dumps(health_data, ensure_ascii=False)}")
            except:
                print(f"  响应: {response.text[:100]}")
        else:
            print(f"⚠ 健康检查接口返回异常状态码: {response.status_code}")
            print(f"  响应: {response.text[:200]}")
        
        print("=" * 60 + "\n")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"✗ 无法连接到后端服务")
        print(f"  错误: {str(e)}")
        print(f"  尝试访问的URL: {BASE_URL}/")
        print(f"\n  请检查：")
        print(f"  1. 后端服务是否已启动？")
        print(f"  2. 端口号是否正确？（当前: {BASE_URL}）")
        print(f"  3. 防火墙是否阻止连接？")
        print(f"  4. 后端是否运行在不同地址？")
        print(f"\n  建议：")
        print(f"  - 在浏览器访问 {BASE_URL}/api/health 查看是否能访问")
        print(f"  - 检查后端终端是否有错误信息")
        print(f"  - 如果后端运行在不同端口，请修改脚本中的 BASE_URL")
        print("=" * 60 + "\n")
        return False
    except Exception as e:
        print(f"✗ 检查后端服务时出错: {str(e)}")
        print("=" * 60 + "\n")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("开始测试所有18个API接口")
    print(f"后端地址: {BASE_URL}")
    print("=" * 60)
    
    # 先检查后端服务是否可用
    if not check_backend_health():
        print("\n⚠️  后端服务连接失败，但将继续尝试测试所有接口...")
        print("   如果所有测试都失败，请先解决连接问题。\n")
    
    # 测试顺序很重要，因为有些接口依赖前面的结果
    tests = [
        # 用户模块（需要先注册登录获取token）
        ("用户注册", test_user_register),
        ("用户登录", test_user_login),
        ("获取用户信息", test_user_info),
        ("修改用户信息", test_user_update),
        
        # 奇门模块
        ("起盘计算", test_qimen_calculate),
        ("保存起盘记录", test_qimen_save),
        ("获取历史记录列表", test_qimen_history_list),
        ("获取历史记录详情", test_qimen_history_detail),
        ("获取今日运势", test_qimen_fortune),
        ("获取万年历数据", test_qimen_calendar),
        ("获取知识文章", test_qimen_knowledge),
        ("删除历史记录", test_qimen_delete),
        
        # 系统模块
        ("获取系统配置", test_system_config),
        ("获取帮助文档", test_system_help),
        ("提交反馈", test_system_feedback),
        ("获取公告列表", test_system_announcements),
        ("获取统计数据", test_system_statistics),
        ("健康检查", test_system_health),
    ]
    
    # 执行测试
    for test_name, test_func in tests:
        try:
            test_func()
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            print_result(False, f"{test_name}异常", str(e))
    
    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试数: {test_results['total']}")
    print(f"通过: {test_results['passed']} ✓")
    print(f"失败: {test_results['failed']} ✗")
    print(f"通过率: {test_results['passed'] / test_results['total'] * 100:.1f}%" if test_results['total'] > 0 else "0%")
    
    if test_results['errors']:
        print("\n失败详情:")
        for error in test_results['errors']:
            print(f"  - {error}")
    
    print("\n" + "=" * 60)
    
    # 返回退出码
    return 0 if test_results['failed'] == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
