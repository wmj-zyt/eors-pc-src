# utils/service_ids.py
from enum import Enum, auto
from .base_manager import BaseManager
from typing import Dict, Type, Optional

class ServiceID(Enum):
    """服务ID枚举类，用于替代字符串硬编码"""
    # 系统服务
    SERIAL_PORT_MANAGER = auto()
    UI_MANAGER = auto()
    CONFIG_MANAGER = auto()
    
    # 可根据需要添加更多服务ID
    
    def __str__(self):
        # 返回枚举的名称而非数值
        return self.name

class ServiceBus:
    """服务总线类，采用单例模式，用于管理所有服务"""
    _instance = None
    _services: Dict[ServiceID, BaseManager] = {}
    _service_classes: Dict[ServiceID, Type[BaseManager]] = {}
    
    def __new__(cls):
        """确保只创建一个ServiceBus实例"""
        if cls._instance is None:
            cls._instance = super(ServiceBus, cls).__new__(cls)
            cls._instance._services = {}
            # 初始化服务类映射表
            cls._instance._service_classes = {}
        return cls._instance
    
    
    def register_service_class(self, service_id: ServiceID, service_class: Type[BaseManager]):
        """注册服务类到服务总线
        
        Args:
            service_id: 服务ID
            service_class: 服务类
        """
        self._service_classes[service_id] = service_class
    
    def get_service(self, service_id: ServiceID) -> BaseManager:
        """获取服务，如果服务未注册则自动创建并初始化
        
        Args:
            service_id: 服务ID枚举值
        
        Returns:
            服务实例，如果未注册且无法自动创建则返回None
        """
        # 检查服务是否已注册
        if service_id in self._services:
            service = self._services[service_id]
            # 检查服务是否已初始化，如果没有则初始化
            if not service.is_initialized:
                print(f"服务 {service_id} 未初始化，正在初始化...")
                service.initialize()
            return service
        
        # 尝试自动创建服务
        if service_id in self._service_classes:
            try:
                # 创建服务实例
                service_class = self._service_classes[service_id]
                service_instance = service_class()
                
                # 注册服务
                self._services[service_id] = service_instance
                
                # 初始化服务
                if not service_instance.is_initialized:
                    print(f"正在初始化服务: {service_id}")
                    service_instance.initialize()
                
                return service_instance
            except Exception as e:
                print(f"自动创建服务 {service_id} 失败: {str(e)}")
                return None
        
        return None
    
    def shutdown_all_services(self):
        """关闭所有服务"""
        print("正在关闭所有服务...")
        for service_id, service in self._services.items():
            if service.is_initialized:
                print(f"关闭服务: {service_id}")
                service.shutdown()
        self._services.clear()


# 创建服务总线实例
service_bus = ServiceBus()