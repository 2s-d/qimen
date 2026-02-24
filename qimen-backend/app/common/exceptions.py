# 文档引用：PROJECT_SPEC.md - 1580行
# 自定义异常

class BusinessException(Exception):
    """
    业务异常（通用）
    文档引用：PROJECT_SPEC.md - 6.3.2节
    """
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationException(BusinessException):
    """
    参数验证异常
    文档引用：PROJECT_SPEC.md - 6.3.2节
    """
    def __init__(self, message: str = "参数验证失败", code: int = 400):
        super().__init__(message, code)

class AuthException(BusinessException):
    """
    认证异常
    文档引用：PROJECT_SPEC.md - 6.3.2节
    """
    def __init__(self, message: str = "未认证", code: int = 401):
        super().__init__(message, code)

class PermissionException(BusinessException):
    """
    权限异常
    文档引用：PROJECT_SPEC.md - 6.3.2节
    """
    def __init__(self, message: str = "无权限", code: int = 403):
        super().__init__(message, code)

class NotFoundException(BusinessException):
    """
    资源不存在异常
    文档引用：PROJECT_SPEC.md - 6.3.2节
    """
    def __init__(self, message: str = "资源不存在", code: int = 404):
        super().__init__(message, code)
