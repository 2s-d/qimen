# 自动化测试说明

## 运行测试

### 前置条件
1. 确保后端服务已启动：`python run.py`（运行在 localhost:8087）
2. 安装测试依赖：`pip install pytest requests`

### 运行所有测试
```bash
cd qimen-backend
python tests/run_tests.py
```

或直接使用 pytest：
```bash
cd qimen-backend
pytest tests/ -v
```

### 运行特定测试模块
```bash
# 只测试系统模块
pytest tests/test_system_api.py -v

# 只测试用户模块
pytest tests/test_user_api.py -v

# 只测试奇门模块
pytest tests/test_qimen_api.py -v
```

## 测试覆盖

### 系统模块 (6个API)
- ✓ 健康检查
- ✓ 获取系统配置
- ✓ 获取帮助文档
- ✓ 获取公告列表
- ✓ 获取数据统计
- ✓ 提交意见反馈

### 用户模块 (4个API)
- ✓ 用户注册
- ✓ 用户登录
- ✓ 获取用户信息
- ✓ 更新用户信息

### 奇门遁甲模块 (8个API)
- ✓ 起盘计算
- ✓ 保存记录
- ✓ 获取历史列表
- ✓ 获取今日运势
- ✓ 获取万年历
- ✓ 获取知识文章

## 测试说明

- 测试会自动创建测试用户并登录获取token
- 测试使用独立的测试数据，不影响生产数据
- 所有测试都是自动化执行，无需手动操作
