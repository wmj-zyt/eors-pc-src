from PySide6.QtCore import QObject


class BaseManager(QObject):
    """所有服务管理器的基础类，提供基本生命周期管理"""
    def __init__(self):
        super().__init__()
        self._is_initialized = False
    
    def initialize(self):
        """初始化服务"""
        self._is_initialized = True
        return True
    
    def shutdown(self):
        """关闭服务"""
        self._is_initialized = False
        return True
    
    @property
    def is_initialized(self):
        """检查服务是否已初始化"""
        return self._is_initialized