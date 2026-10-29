# utils/services_bus/service_initializer.py
"""
服务初始化模块
负责注册所有服务类到服务总线
"""

from .services_bus import service_bus, ServiceID


def initialize_services():
    """初始化所有服务类注册"""
    try:
        # 动态导入服务类以避免循环依赖
        from .serial_port_manager import SerialPortManager
        from .ui_manager import UIManager
        from .config_manager import ConfigManager
        
        # 注册服务类到服务总线
        service_bus.register_service_class(ServiceID.SERIAL_PORT_MANAGER, SerialPortManager)
        service_bus.register_service_class(ServiceID.UI_MANAGER, UIManager)
        service_bus.register_service_class(ServiceID.CONFIG_MANAGER, ConfigManager)
        
        print("服务类注册完成")
    except ImportError as e:
        print(f"导入服务类失败: {str(e)}")
    except Exception as e:
        print(f"注册服务类失败: {str(e)}")


# 在模块导入时自动初始化
initialize_services()