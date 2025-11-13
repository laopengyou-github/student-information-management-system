import logging
import logging.handlers
import os
from datetime import datetime
import sys

class Logger:
    """
    日志记录器类，用于系统操作日志的记录
    支持不同级别的日志记录和文件轮换
    """
    
    # 日志级别映射
    LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    def __init__(self, log_dir='logs', log_level='info', max_bytes=10*1024*1024, backup_count=5):
        """
        初始化日志记录器
        
        Args:
            log_dir: 日志文件保存目录
            log_level: 日志级别
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的日志文件数量
        """
        self._log_dir = log_dir
        self._log_level = self.LEVEL_MAP.get(log_level.lower(), logging.INFO)
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        
        # 确保日志目录存在
        self._ensure_log_dir_exists()
        
        # 创建日志记录器
        self._logger = self._setup_logger()
    
    def _ensure_log_dir_exists(self):
        """
        确保日志目录存在，如果不存在则创建
        """
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)
    
    def _setup_logger(self):
        """
        设置日志记录器
        
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        logger = logging.getLogger('StudentInfoSystem')
        logger.setLevel(self._log_level)
        
        # 清除现有的处理器
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
        
        # 创建文件处理器，支持文件轮换
        log_filename = os.path.join(self._log_dir, f'student_system_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_filename,
            maxBytes=self._max_bytes,
            backupCount=self._backup_count,
            encoding='utf-8'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message):
        """
        记录调试级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.debug(message)
    
    def info(self, message):
        """
        记录信息级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.info(message)
    
    def warning(self, message):
        """
        记录警告级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.warning(message)
    
    def error(self, message):
        """
        记录错误级别日志
        
        Args:
            message: 日志消息
        """
        self._logger.error(message)
    
    def critical(self, message, **kwargs):
        """
        记录严重错误级别日志
        
        Args:
            message: 日志消息
            **kwargs: 其他参数，如exc_info等
        """
        self._logger.critical(message, **kwargs)
    
    def log_operation(self, operation_type, user_info=None, details=None):
        """
        记录操作日志
        
        Args:
            operation_type: 操作类型
            user_info: 用户信息
            details: 操作详情
        """
        log_message = f"操作类型: {operation_type}"
        if user_info:
            log_message += f", 用户: {user_info}"
        if details:
            log_message += f", 详情: {details}"
        
        self.info(log_message)
    
    def log_error(self, error_message, exception=None):
        """
        记录错误日志
        
        Args:
            error_message: 错误消息
            exception: 异常对象
        """
        if exception:
            self.error(f"{error_message}: {str(exception)}")
        else:
            self.error(error_message)
    
    def set_level(self, log_level):
        """
        设置日志级别
        
        Args:
            log_level: 新的日志级别
        """
        self._log_level = self.LEVEL_MAP.get(log_level.lower(), logging.INFO)
        self._logger.setLevel(self._log_level)
        
        # 更新所有处理器的级别
        for handler in self._logger.handlers:
            handler.setLevel(self._log_level)

# 创建全局日志记录器实例
global_logger = None

def get_logger():
    """
    获取全局日志记录器实例
    
    Returns:
        Logger: 全局日志记录器
    """
    global global_logger
    if global_logger is None:
        global_logger = Logger()
    return global_logger

# 创建并导出logger变量，方便直接导入使用
logger = get_logger()