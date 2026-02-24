# 文档引用：PROJECT_SPEC.md - 1582行
# 分页工具（历史记录列表需要）

from app.common.response import paginated_response

def get_pagination_params(page: int = 1, size: int = 10) -> tuple[int, int]:
    """
    获取分页参数并验证
    文档引用：PROJECT_SPEC.md - 5.2.3节
    """
    # 验证page≥1，size≥1且≤100
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    if size > 100:
        size = 100
    
    return page, size

def calculate_offset(page: int, size: int) -> int:
    """
    计算分页偏移量
    """
    return (page - 1) * size
