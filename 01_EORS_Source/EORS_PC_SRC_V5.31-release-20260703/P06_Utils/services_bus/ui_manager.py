from PySide6.QtCore import Signal, QObject, QTimer
from .base_manager import BaseManager
from .config_manager import ConfigManager
from .services_bus import service_bus, ServiceID
import os

class UIManager(BaseManager):
    """UI状态管理服务，用于管理UI相关的状态和消息"""
    # 定义信号
    status_message_changed = Signal(str)  # 状态栏消息变化信号 (消息内容, 显示时长)
    message_box_requested = Signal(str, str, str)  # 消息框请求信号 (标题, 内容, 消息类型)
    update_model_list = Signal(list)  # 模型列表变化信号 (模型列表)
    dataset_loading_update = Signal(str, object) # 专门用于readDataset线程与UI线程通信的信号,参数：更新类型, 数据
    train_info_update = Signal(str, object) # 专门用于训练线程与UI线程通信的信号,参数：更新类型, 数据
    
    def __init__(self):
        super().__init__()
        # 通过服务总线获取ConfigManager，确保使用单例实例
        self.config_manager = None
    
    def initialize(self):
        """初始化UI状态管理服务"""
        # 初始化任何必要的状态
        # 通过服务总线获取ConfigManager
        self.config_manager = service_bus.get_service(ServiceID.CONFIG_MANAGER)
        if not self.config_manager:
            print("警告: 无法获取ConfigManager服务")
            # 创建一个本地实例作为后备
            self.config_manager = ConfigManager()
            
        # 初始化模型扫描定时器
        self._model_scan_timer = QTimer()
        self._model_scan_timer.timeout.connect(self.updata_model_list_comboBox)
        self._model_scan_timer.start(1000)
        
        return super().initialize()
    
    def show_status_message(self, message: str):
        """显示状态栏消息
        
        Args:
            message: 要显示的消息内容
            timeout: 消息显示时长(毫秒)，默认为3秒
        """
        self.status_message_changed.emit(message)
    
    def show_message_box(self, title: str, message: str, message_type: str):
        """显示消息框
        
        Args:
            title: 消息框标题
            message: 消息内容
            message_type: 消息类型，0表示信息类型，1表示警告类型，2表示错误类型
        """
        self.message_box_requested.emit(title, message, message_type)   
    
    def update_training_info(self, update_type: str, data: object):
        self.train_info_update.emit(update_type, data)

    def update_dataset_loading_info(self, update_type: str, data: object):
        self.dataset_loading_update.emit(update_type, data)

    def updata_model_list_comboBox(self):
        """更新模型列表到comboBox"""
        model_list = []
        if not self.config_manager:
            print("警告: ConfigManager未初始化")
            return
            
        dataset_path = self.config_manager.get("foldersPath.datasetPath")
        if not dataset_path or not os.path.exists(dataset_path):
            model_list = []
        else:
            # 扫描数据集路径下的所有.keras和.h5文件
            import glob
            keras_files = glob.glob(os.path.join(dataset_path, "*.keras"))
            h5_files = glob.glob(os.path.join(dataset_path, "*.h5"))
            # 获取文件名（不包含路径）
            model_list = [os.path.basename(file) for file in keras_files + h5_files]

        self.update_model_list.emit(model_list)
    
    def shutdown(self):
        """关闭服务"""
        # 停止定时器
        if hasattr(self, '_model_scan_timer'):
            self._model_scan_timer.stop()
        # 清理任何资源
        return super().shutdown()