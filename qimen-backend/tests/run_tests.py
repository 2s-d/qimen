#!/usr/bin/env python3
"""
自动化测试运行脚本
"""
import subprocess
import sys
import os

def run_tests():
    """运行所有测试"""
    # 切换到后端目录
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    print("=" * 60)
    print("奇门遁甲小程序 - 自动化测试")
    print("=" * 60)
    print()
    
    # 检查后端服务是否运行
    import requests
    try:
        response = requests.get("http://localhost:8087/api/system/health", timeout=2)
        if response.status_code == 200:
            print("✓ 后端服务运行正常")
        else:
            print("✗ 后端服务响应异常")
            sys.exit(1)
    except Exception as e:
        print(f"✗ 后端服务未运行或无法访问: {e}")
        print("  请先启动后端服务: python run.py")
        sys.exit(1)
    
    print()
    print("开始运行测试...")
    print()
    
    # 运行pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # 详细输出
        "--tb=short",  # 简短错误信息
        "-x"  # 遇到第一个失败就停止（可选，注释掉可运行全部测试）
    ])
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    run_tests()
