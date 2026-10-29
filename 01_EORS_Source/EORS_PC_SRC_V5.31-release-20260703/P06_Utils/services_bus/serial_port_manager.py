from PySide6.QtCore import Signal, QTimer
from .base_manager import BaseManager
import serial.tools.list_ports
from typing import Dict, Callable, Optional, List
from ..serial_port.serial_port import SerialPort

class SerialPortManager(BaseManager):
    """串口管理服务，用于集中管理串口资源和状态，支持多串口并发和自定义数据处理"""
    # 定义信号
    ports_updated = Signal(list)  # 可用串口列表更新信号
    
    def __init__(self):
        super().__init__()
        self._available_ports = []
        self._serial_ports: Dict[str, SerialPort] = {}  # 管理的串口实例
        self._data_handlers: Dict[str, List[Callable]] = {}  # 数据处理回调函数
        self._ports_update_handler: list[Callable[[list], None]] = []
        
        # 直接在SerialManager中实现定时器功能
        self._timer = QTimer()
        self._timer.setInterval(2000)  # 每2秒检查一次串口
        self._timer.timeout.connect(self._check_ports)
    
    def _check_ports(self):
        """定期检测可用串口"""
        current_ports = self._get_ports()
        self._available_ports = current_ports
        for handler in self._ports_update_handler:
            try:
                handler(self._available_ports)
            except Exception as e:
                print(f"可用串口列表更新回调错误: {str(e)}")
    
    def _get_ports(self):
        """获取可用串口列表"""
        try:
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
        except Exception as e:
            print(f"获取串口列表失败: {str(e)}")
            return []
    
    def _on_port_data_received(self, port_name: str, data: bytes):
        """处理串口数据接收，调用注册的回调函数"""
        if port_name in self._data_handlers:
            for handler in self._data_handlers[port_name]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"数据处理回调错误 [{port_name}]: {str(e)}")
    
    def add_ports_updated_handler(self, handler: Callable[[list], None]):
        """注册可用串口列表更新回调函数"""
        self._ports_update_handler.append(handler)

    def get_available_ports(self):
        """获取当前可用串口列表
        
        Returns:
            list: 可用串口设备路径列表
        """
        return self._available_ports
    
    def create_port(self, port_name: str, port_alias: Optional[str] = None, baud_rate: int = 115200) -> bool:
        """创建串口连接
        
        Args:
            port_name: 串口设备名称（如COM3）
            port_alias: 串口别名（如“传感器串口”）
            baud_rate: 波特率
            
        Returns:
            bool: 是否创建成功
        """
        if port_name in self._serial_ports:
            print(f"串口 {port_name} 已存在")
            return False
        
        try:
            # 创建串口实例
            serial_port = SerialPort(port_alias or port_name)
            
            # 连接信号
            serial_port.dataReceived.connect(self._on_port_data_received)
            
            # 存储串口实例
            self._serial_ports[port_name] = serial_port
            
            return True
        except Exception as e:
            print(f"创建串口 {port_name} 失败: {str(e)}")
            return False
    
    def connect_port(self, port_name: str, baud_rate: int = 115200) -> bool:
        """连接指定串口
        
        Args:
            port_name: 串口设备名称
            baud_rate: 波特率
            
        Returns:
            bool: 是否连接成功
        """
        # 如果串口不存在，先创建
        if port_name not in self._serial_ports:
            if not self.create_port(port_name, None, baud_rate):
                return False
        
        serial_port = self._serial_ports[port_name]
        success = serial_port.open(port_name, baud_rate)
        
        if not success:
            print(f"连接串口 {port_name} 失败")
        
        return success
    
    def disconnect_port(self, port_name: str) -> bool:
        """断开指定串口
        
        Args:
            port_name: 串口设备名称
            
        Returns:
            bool: 是否断开成功
        """
        if port_name not in self._serial_ports:
            return False
        
        try:
            serial_port = self._serial_ports[port_name]
            serial_port.close()
            return True
        except Exception as e:
            print(f"断开串口 {port_name} 失败: {str(e)}")
            return False
    
    def remove_port(self, port_name: str) -> bool:
        """移除串口
        
        Args:
            port_name: 串口设备名称
            
        Returns:
            bool: 是否移除成功
        """
        if port_name not in self._serial_ports:
            return False
        
        # 先断开连接
        self.disconnect_port(port_name)
        
        # 移除数据处理器
        if port_name in self._data_handlers:
            del self._data_handlers[port_name]
        
        # 移除串口实例
        del self._serial_ports[port_name]
        
        return True
    
    def is_port_connected(self, port_name: Optional[str] = None) -> bool:
        """检查串口是否已连接
        
        Args:
            port_name: 串口名称，如果为None则检查是否有任何连接
            
        Returns:
            bool: 是否已连接
        """
        if port_name is None:
            # 检查是否有任何连接
            return any(port.isOpen() for port in self._serial_ports.values())
        
        if port_name in self._serial_ports:
            return self._serial_ports[port_name].isOpen()
        return False
    
    def send_data(self, port_name: str, data) -> bool:
        """发送数据到指定串口
        
        Args:
            port_name: 串口名称
            data: 要发送的数据
            
        Returns:
            bool: 是否发送成功
        """
        if port_name not in self._serial_ports:
            return False
        
        try:
            serial_port = self._serial_ports[port_name]
            if not serial_port.isOpen():
                return False
            
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            serial_port.write(data)
            return True
        except Exception as e:
            print(f"发送数据到 {port_name} 失败: {str(e)}")
            return False
    
    def register_data_handler(self, port_name: str, handler: Callable[[bytes], None]):
        """注册数据处理回调函数
        
        Args:
            port_name: 串口名称
            handler: 回调函数，签名为 (port_name: str, data: bytes) -> None
        """
        if port_name not in self._data_handlers:
            self._data_handlers[port_name] = []
        
        if handler not in self._data_handlers[port_name]:
            self._data_handlers[port_name].append(handler)
    
    def unregister_data_handler(self, port_name: str, handler: Callable[[bytes], None]):
        """取消注册数据处理回调函数
        
        Args:
            port_name: 串口名称
            handler: 要移除的回调函数
        """
        if port_name in self._data_handlers:
            if handler in self._data_handlers[port_name]:
                self._data_handlers[port_name].remove(handler)
    
    def clear_data_handlers(self, port_name: Optional[str] = None):
        """清除数据处理回调函数
        
        Args:
            port_name: 串口名称，如果为None则清除所有
        """
        if port_name is None:
            self._data_handlers.clear()
        elif port_name in self._data_handlers:
            self._data_handlers[port_name].clear()
    
    def initialize(self):
        """初始化服务并启动定时器"""
        super().initialize()
        self._timer.start()
        # 初始扫描一次可用串口
        self._check_ports()
        return True
    
    def shutdown(self):
        """关闭服务，断开所有串口连接"""
        # 断开所有串口
        for port_name in list(self._serial_ports.keys()):
            self.disconnect_port(port_name)
            
        # 清除所有数据处理器
        self._data_handlers.clear()
        
        # 停止定时器
        if self._is_initialized:
            self._timer.stop()
        
        return super().shutdown()