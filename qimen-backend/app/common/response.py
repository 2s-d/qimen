# 文档引用：PROJECT_SPEC.md - 1579行
# 统一响应格式

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional

def success_response(data: Any = None, message: str = "success") -> JSONResponse:
    """
    成功响应
    文档引用：PROJECT_SPEC.md - 6.1.1节
    """
    content = {"code": 200, "message": message, "data": data}
    # 使用 jsonable_encoder 处理 datetime、UUID 等不可直接序列化类型
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(content)
    )

def error_response(code: int, message: str, data: Any = None) -> JSONResponse:
    """
    错误响应
    文档引用：PROJECT_SPEC.md - 6.1.2节
    """
    content = {"code": code, "message": message, "data": data}
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(content)
    )

def paginated_response(
    data: list,
    total: int,
    page: int,
    size: int,
    message: str = "success"
) -> JSONResponse:
    """
    分页响应
    文档引用：PROJECT_SPEC.md - 1582行
    """
    content = {
        "code": 200,
        "message": message,
        "data": {
            "items": data,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size > 0 else 0
        }
    }
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(content)
    )
