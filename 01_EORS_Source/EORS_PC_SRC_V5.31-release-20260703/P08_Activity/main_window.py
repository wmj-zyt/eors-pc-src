#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块
"""
# 导入QT相关模块
from PySide6.QtWidgets import QMainWindow, QMessageBox, QButtonGroup


# 导入项目相关模块
from P06_Utils.services_bus.config_manager import ConfigManager
from .data_acuisition_widget import DataAcuisitionWidget
from P06_Utils.services_bus.services_bus import service_bus, ServiceID
from P06_Utils.services_bus.ui_manager import UIManager
from .additional_function_widget import AdditionalFunctionWidget
from .model_predict_widget import ModelPredictWidget
from .model_training_widget import ModelTrainingWidget
from .component_generate_widget import ComponentGenerateWidget
from .help_dialog import HelpDialog

import os
import sys

# 导入UI文件
from P07_View.Qt_Designer_ui_py.Ui_MainWindow import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.__main_window = QMainWindow()
        self.setupUi(self.__main_window)

        #====================================定义子对象=====================================#
        self.__data_acuisition_widget = DataAcuisitionWidget()
        # self.__additional_function_widget = AdditionalFunctionWidget()
        self.__model_training_widget = ModelTrainingWidget()
        self.__model_predict_widget = ModelPredictWidget()
        self.__component_generate_widget = ComponentGenerateWidget()
        
        self.ui_manager: UIManager = service_bus.get_service(ServiceID.UI_MANAGER)
        self.config_manager: ConfigManager = service_bus.get_service(ServiceID.CONFIG_MANAGER)
        app_desc = self.config_manager.get("appInfo.description")
        app_version = self.config_manager.get("appInfo.version")
        #====================================设置UI=====================================#
        self.appDesc.setText(app_desc + app_version)
        self.stackedWidget.addWidget(self.__data_acuisition_widget.get_widget())
        self.stackedWidget.addWidget(self.__model_training_widget.get_widget())
        self.stackedWidget.addWidget(self.__model_predict_widget.get_widget())
        self.stackedWidget.addWidget(self.__component_generate_widget.get_widget())
        
        # self.stackedWidget.addWidget(self.__additional_function_widget.get_widget())
        self.stackedWidget.setCurrentWidget(self.__data_acuisition_widget.get_widget())
        
        # 创建按钮组实现互斥选择
        self.buttonGroup = QButtonGroup(self.__main_window)
        self.buttonGroup.addButton(self.dataAcquisition)
        self.buttonGroup.addButton(self.modelTraining)
        self.buttonGroup.addButton(self.softwareHelp)
        self.buttonGroup.setExclusive(True)
        
        # 设置默认选中数据采集按钮
        self.dataAcquisition.setChecked(True)

        #====================================绑定信号与槽=====================================#
        self.ui_manager.status_message_changed.connect(self.__show_status_message)
        self.ui_manager.message_box_requested.connect(self.__show_message_box)
        
        # 使用lambda表达式简化按钮点击处理
        self.dataAcquisition.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.__data_acuisition_widget.get_widget()))
        self.modelTraining.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.__model_training_widget.get_widget()))
        # self.additionalFunction.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.__additional_function_widget.get_widget()))
        self.modelPredict.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.__model_predict_widget.get_widget()))
        self.componentGeneration.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.__component_generate_widget.get_widget()))
        # 绑定帮助按钮点击事件
        self.softwareHelp.clicked.connect(self.__show_help_dialog)


        # 清理received_images目录   [WTX添加]
        # 获取应用程序工程目录
        if hasattr(sys, '_MEIPASS'):
            self.projectRoot = sys._MEIPASS
        else:
            self.projectRoot = os.path.abspath(os.getcwd()) 
        print(f"projectRoot is {self.projectRoot}")
        self.clean_received_images_directory()

    """
    函数名称：clean_received_images_directory  [WTXt添加]
    参数说明：无
    函数返回：无
    功能概要：清理received_images目录中的所有文件
    """
    def clean_received_images_directory(self):
        import shutil
        try:
            # 构建received_images目录路径
            received_images_path = os.path.join(self.projectRoot, "received_images")
            # 检查目录是否存在
            if os.path.exists(received_images_path):
                # 删除目录中的所有文件
                for filename in os.listdir(received_images_path):
                    file_path = os.path.join(received_images_path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f'删除文件 {file_path} 失败: {e}')
        except Exception as e:
            print(f'清理received_images目录时出错: {e}')

    def show(self):
        self.__main_window.show()

    def __show_status_message(self, message: str):
        """显示状态栏消息
        
        Args:
            message: 要显示的消息内容
        """
        self.statusBar.setText(message)

    def __show_message_box(self, title: str, message: str, message_type: str):
        """显示消息框
        
        Args:
            title: 消息框标题
            message: 消息内容
            message_type: 消息类型，0表示信息类型，1表示警告类型，2表示错误类型
        """
        if message_type == "warning":
            QMessageBox.warning(self.__main_window, title, message)
        elif message_type == "critical":
            QMessageBox.critical(self.__main_window, title, message)
        elif message_type == "information":
            QMessageBox.information(self.__main_window, title, message)

    def __show_help_dialog(self):
        """显示帮助文档对话框"""
        help_dialog = HelpDialog(self.__main_window)
        help_dialog.exec()