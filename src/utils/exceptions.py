class StudentSystemError(Exception):
    """
    学生信息管理系统基础异常类
    所有系统自定义异常都继承自这个类
    """
    def __init__(self, message="学生信息管理系统错误", error_code=None):
        """
        初始化基础异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class DataValidationError(StudentSystemError):
    """
    数据验证错误
    当输入数据不符合验证规则时抛出
    """
    def __init__(self, message="数据验证失败", field_name=None):
        """
        初始化数据验证错误
        
        Args:
            message: 错误消息
            field_name: 出错的字段名
        """
        self.field_name = field_name
        full_message = f"{field_name}：{message}" if field_name else message
        super().__init__(full_message, error_code="VALIDATION_ERROR")

class StudentNotFoundError(StudentSystemError):
    """
    学生不存在错误
    当尝试访问不存在的学生记录时抛出
    """
    def __init__(self, student_id=None):
        """
        初始化学生不存在错误
        
        Args:
            student_id: 不存在的学生学号
        """
        if student_id:
            message = f"学号为 {student_id} 的学生不存在"
        else:
            message = "学生不存在"
        super().__init__(message, error_code="STUDENT_NOT_FOUND")

class StudentAlreadyExistsError(StudentSystemError):
    """
    学生已存在错误
    当尝试添加一个已存在的学生记录时抛出
    """
    def __init__(self, student_id):
        """
        初始化学生已存在错误
        
        Args:
            student_id: 重复的学生学号
        """
        message = f"学号为 {student_id} 的学生已存在"
        super().__init__(message, error_code="STUDENT_ALREADY_EXISTS")

class DataIOError(StudentSystemError):
    """
    数据读写错误
    当数据文件读写操作失败时抛出
    """
    def __init__(self, message="数据读写失败", file_path=None, operation=None):
        """
        初始化数据读写错误
        
        Args:
            message: 错误消息
            file_path: 操作的文件路径
            operation: 执行的操作（读取/写入/备份等）
        """
        self.file_path = file_path
        self.operation = operation
        
        full_message = message
        if operation:
            full_message = f"{operation}操作失败：{message}"
        if file_path:
            full_message += f" (文件：{file_path})"
        
        super().__init__(full_message, error_code="DATA_IO_ERROR")

class BackupRestoreError(StudentSystemError):
    """
    备份恢复错误
    当数据备份或恢复操作失败时抛出
    """
    def __init__(self, message="备份恢复操作失败", operation="备份"):
        """
        初始化备份恢复错误
        
        Args:
            message: 错误消息
            operation: 操作类型（备份/恢复）
        """
        full_message = f"{operation}失败：{message}"
        super().__init__(full_message, error_code="BACKUP_RESTORE_ERROR")

class InvalidOperationError(StudentSystemError):
    """
    无效操作错误
    当用户尝试执行无效或不允许的操作时抛出
    """
    def __init__(self, message="无效操作"):
        """
        初始化无效操作错误
        
        Args:
            message: 错误消息
        """
        super().__init__(message, error_code="INVALID_OPERATION")

class PermissionDeniedError(StudentSystemError):
    """
    权限拒绝错误
    当用户尝试执行没有权限的操作时抛出
    """
    def __init__(self, message="权限不足，无法执行此操作"):
        """
        初始化权限拒绝错误
        
        Args:
            message: 错误消息
        """
        super().__init__(message, error_code="PERMISSION_DENIED")

class EmptyDataError(StudentSystemError):
    """
    空数据错误
    当操作需要数据但没有可用数据时抛出
    """
    def __init__(self, message="没有可用数据"):
        """
        初始化空数据错误
        
        Args:
            message: 错误消息
        """
        super().__init__(message, error_code="EMPTY_DATA")

class SystemConfigError(StudentSystemError):
    """
    系统配置错误
    当系统配置不正确或缺失时抛出
    """
    def __init__(self, message="系统配置错误", config_name=None):
        """
        初始化系统配置错误
        
        Args:
            message: 错误消息
            config_name: 配置项名称
        """
        if config_name:
            message = f"配置项 '{config_name}'：{message}"
        super().__init__(message, error_code="SYSTEM_CONFIG_ERROR")

class OperationFailedError(StudentSystemError):
    """
    操作失败错误
    当业务操作执行失败时抛出
    """
    def __init__(self, message="操作执行失败", operation=None):
        """
        初始化操作失败错误
        
        Args:
            message: 错误消息
            operation: 操作名称
        """
        if operation:
            message = f"{operation}操作失败：{message}"
        super().__init__(message, error_code="OPERATION_FAILED")

# 异常处理工具函数
def handle_exception(exception, logger=None):
    """
    统一处理异常的函数
    
    Args:
        exception: 异常对象
        logger: 日志记录器实例
        
    Returns:
        str: 格式化的错误消息
    """
    # 确定错误消息
    if isinstance(exception, StudentSystemError):
        # 已知的系统异常
        error_message = str(exception)
    else:
        # 未知异常
        error_message = f"发生未知错误: {str(exception)}"
    
    # 记录日志
    if logger:
        if isinstance(exception, StudentSystemError):
            # 系统自定义异常记录为错误级别
            logger.error(error_message)
        else:
            # 未知异常记录为严重错误级别
            logger.critical(error_message, exc_info=True)
    
    return error_message

def safe_operation(logger=None):
    """
    安全操作装饰器，用于捕获并处理函数执行过程中的异常
    
    Args:
        logger: 日志记录器实例
        
    Returns:
        function: 装饰后的函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = handle_exception(e, logger)
                # 对于返回元组 (success, message) 格式的函数
                if func.__name__ in ['add_student', 'update_student', 'delete_student', 
                                   'delete_students_by_ids', 'delete_students_by_class']:
                    return False, error_message
                # 对于其他函数，可以根据需要调整返回值
                raise
        return wrapper
    return decorator