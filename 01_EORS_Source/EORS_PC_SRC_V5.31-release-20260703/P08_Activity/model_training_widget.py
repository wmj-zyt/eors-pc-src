# 导入QT模块
from PySide6.QtWidgets import QFileDialog, QHeaderView, QWidget, QTextEdit, QTableWidgetItem,QMessageBox
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QImage,QPixmap,QIcon,QAction,QTextCursor
from h5py._hl import dataset
from tensorflow.python.data.util.structure import NoneTensor


# 导入工程模块
from P07_View.Qt_Designer_ui_py.Ui_ModelTrainingWidget import Ui_ModelTrainingWidget
from P06_Utils.services_bus.ui_manager import UIManager
from P06_Utils.services_bus.config_manager import ConfigManager
from P06_Utils.services_bus.services_bus import service_bus, ServiceID
from P03_Components.customChart import LossAccChart
# 导入其他模块
import importlib.util
import os
from PIL import Image
from threading import Thread, Event
from keras.callbacks import ModelCheckpoint
import numpy as np
import shutil

from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from keras.losses import CategoricalCrossentropy

import tensorflow as tf
from datetime import datetime

from keras.models import load_model
import h5py
from P04_Model  import *
import importlib


#WTX自动训练新增【2025-1125】
from PySide6.QtWidgets import QDialog,QMessageBox,QSpinBox,QPushButton
from .auto_train import ParamDialog
from PySide6.QtCore import Signal,QObject
from threading import Thread
import time

class TrainSignals(QObject):
    """训练信号类"""
    update_ui_params = Signal(int, int, float)  # epochs, batchsize, learning_rate
    enable_buttons = Signal(QPushButton,bool)                # 启用/禁用按钮


"""
类名：ModelTrain
基类：无
功能：模型训练类
"""

class ModelTrainingWidget(Ui_ModelTrainingWidget):
    """
    函数名称：__init__
    参数说明：无 
    函数返回：无
    功能概要：初始化方法，设置训练界面的初始状态和信号连接
    """
    def __init__(self):
        # 调用父类的初始化方法
        super().__init__()

        #====================================添加变量====================================#
        self.__model_training_widget = QWidget()
        self.setupUi(self.__model_training_widget)
        
        # 初始化同步锁
        self.event = Event()
        # 初始化输入数据列表和名称列表
        self.inputData = list()
        self.inputDataName = list()
        # 初始化训练集图片
        self.train_images = None
        # 初始化训练集标签
        self.train_labels = None
        # 初始化验证集图片
        self.val_images = None
        # 初始化验证集标签
        self.val_labels = None
        # 初始化验证集图片
        self.test_images = None
        # 初始化验证集标签
        self.test_labels = None
        # 类型数量初始化为0
        self.typeNum = 0
        # 数据集名字初始化为空字符串,数据集名字一般为文件夹名字
        self.datasetName = ""
        # 图片类别初始化为空列表
        self.imageCategory = list()
        self.ui_manager: UIManager = service_bus.get_service(ServiceID.UI_MANAGER)
        self.config_manager: ConfigManager = service_bus.get_service(ServiceID.CONFIG_MANAGER)
        # 获取模型列表
        modelList = self.config_manager.get("globalSettings.supportedModels")
        # 初始化训练图表
        self.chart = LossAccChart("训练及验证指标")

        #====================================设置UI=====================================#
        # 隐藏加载数据集的进度条
        self.TrainLoadDatasetProgressBar.setVisible(False)
        # 隐藏数据集信息显示
        self.TrainDatasetInfo.setVisible(False)
        # 隐藏删除数据集按钮
        self.TrainDeleteDataset.setVisible(False)
        # 设置图表到训练图形视图
        self.TrainGraphicsView.setChart(self.chart)
        # 禁用鼠标交互，防止用户影响光标
        self.trainInfoText.setTextInteractionFlags(Qt.NoTextInteraction)
        # 设置训练数据集信息表格的列自动拉伸
        self.TrainDatasetInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #====================================绑定信号与槽=====================================#
        # 连接加载数据集按钮的点击事件，加载数据集
        self.TrainLoadDataset.clicked.connect(self.loadDataset)
        # 连接删除数据集按钮的点击事件，卸载数据集
        self.TrainDeleteDataset.clicked.connect(self.unloadDataset)
        # 连接训练轮数spinbox的值变化事件，更新设置的epoch值
        self.epochSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'epoch_spinbox'))
        # 连接epoch滑块的值变化事件，更新设置的epoch值
        self.epochSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'epoch_slider'))
        # 连接批量大小spinbox的值变化事件，更新设置的epoch值
        self.batchsizeSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'batchsize_spinbox'))
        # 连接批量大小滑块的值变化事件，更新设置的epoch值
        self.batchsizeSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'batchsize_slider'))
        # 连接epoch滑块的值变化事件，更新设置的epoch值
        self.epochSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'epoch_slider'))
        # 连接学习率spinbox的值变化事件，更新设置的学习率值
        self.learningRateSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'learningRate_spinbox'))
        # 连接学习率滑块的值变化事件，更新设置的学习率值
        self.learningRateSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'learningRate_slider'))
        # 连接测试数据集比例spinbox的值变化事件，更新设置的测试数据集比例值
        self.testDatasetRatioSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'testDataRatio_spinbox'))
        # 连接测试数据集比例滑块的值变化事件，更新设置的测试数据集比例值
        self.testDatasetRatioSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'testDataRatio_slider'))
        # 连接tail spinbox的值变化事件，更新设置的tail数据量值
        self.tailSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'tail_spinbox'))
        # 连接tail数据量滑块的值变化事件，更新设置的tail数据量值
        self.tailSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'tail_slider'))
        # 连接alpha spinbox的值变化事件，更新设置的alpha值
        self.alphaSpinBox.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'alpha_spinbox'))
        # 连接alpha滑块的值变化事件，更新设置的alpha值
        self.alphaSlider.valueChanged.connect(lambda x: self.settingsChangeVal(x, 'alpha_slider'))
        # 连接重置训练参数设置按钮的点击事件，重置所有设置
        self.resetTrainSettings.clicked.connect(self.settingsReset)
        # 连接开始训练按钮的点击事件，开始训练模型
        self.startTrainRunning.clicked.connect(self.trainModel)
        # 连接清空训练信息按钮的点击事件，清空训练信息显示区域
        self.clearTrainInfo.clicked.connect(self.trainInfoText.clear)
        # 发射信号以填充模型选择下拉框
        # 清空下拉框
        self.trainModelComboBox.clear()
        # 将模型文件名列表添加到组合框中
        self.trainModelComboBox.addItems(modelList)
        # 连接训练模型的选择变化信号到处理函数
        # self.trainModelComboBox.currentIndexChanged.connect(self.changeTrainModel)
        # 连接清空训练图表按钮的点击事件，清空训练图表
        self.clearTrainChart.clicked.connect(self.chart.clear)
        # 连接更新下拉框的槽函数
        # self.ui_manager.model_list_changed.connect(self.update_model_lsit)
        # 连接数据集加载信号到槽函数
        self.ui_manager.dataset_loading_update.connect(self._handle_dataset_loading_update)
        # 连接更新训练信息的信号
        self.ui_manager.train_info_update.connect(self._handle_train_ui_update)

        #WTX20251115新增
        # 连接自动训练按钮的点击事件，开始自动训练模型
        self.startAutoTrainRunning.clicked.connect(self.startAutoTrain)

        #2025年11-25为了自动训练新增
        # 初始化信号
        self.signals = TrainSignals()
        # 连接信号槽
        self.setup_signal_connections()

    #2025年11-25为了自动训练新增
    def setup_signal_connections(self):
            """设置信号槽连接"""
            self.signals.update_ui_params.connect(self.on_update_ui_params)
            self.signals.enable_buttons.connect(self.on_enable_buttons)

        # 信号槽函数
    def on_update_ui_params(self,epochs, batchsize, learning_rate):
        """更新UI参数（在主线程中执行）"""
        try:
            # 这里需要根据您的实际UI控件名称进行调整
                self.epochSpinBox.setValue(epochs)
                self.batchsizeSpinBox.setValue(batchsize)
                self.learningRateSpinBox.setValue(learning_rate)
        except Exception as e:
            print(f"UI参数更新错误: {e}")

    def on_enable_buttons(self, on_enable_buttons,enabled):
        """启用/禁用按钮"""
        try:
            on_enable_buttons.setEnabled(enabled)
        except Exception as e:
            print(f"按钮状态更新错误: {e}")

    def get_widget(self):
        return self.__model_training_widget

    """
    函数名称：list_folders
    参数说明：directory:目录 
    函数返回：目录下所有文件夹组成的列表
    功能概要：获取目录下的所有文件夹
    """
    @staticmethod
    def list_folders(directory):
        # 初始化文件夹列表为空
        folders = []
        # 遍历目录下所有项目（文件及文件夹）
        for item in os.listdir(directory):
            # 获取所有项目路径
            item_path = os.path.join(directory, item)
            # 检查每个项目是否是一个文件夹
            if os.path.isdir(item_path):
                # 如果是文件夹，则将其添加到返回的列表中
                folders.append(item)
        # 返回包含所有文件夹名称的列表
        return folders


    """
    函数名称：loadDataset
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：加载数据集
    修改    ：WTX2025-1125修改，仅支持BMP格式图片 
    """
    def loadDataset(self):
        # 打开文件夹选择对话框
        openFolder = self.config_manager.get("foldersPath.datasetPath")
        if not openFolder or not os.path.exists(openFolder):
            openFolder = os.path.join(os.path.expanduser("~"), "Desktop")
        datasetPath = QFileDialog.getExistingDirectory(self.__model_training_widget, "导入数据集", openFolder)
        self.config_manager.set("foldersPath.datasetPath", datasetPath)
        # 保存配置到文件
        self.config_manager.save_config()
        # 如果取消选择数据集文件夹，则显示取消导入数据集的状态信息，并退出方法
        if not datasetPath:
            self.ui_manager.show_status_message("取消导入数据集。")
            return
        self.datasetName = os.path.basename(datasetPath)
        if self.datasetName in ('data', 'train', 'test', 'validation'):
            self.ui_manager.show_message_box("错误", "导入数据集文件夹名称不可以叫data/train/test/validation", "critical")
            return 
        # 检查数据集文件夹下是否存在RawData文件夹和生成的Data文件夹
        dirs = [d.lower() for d in self.list_folders(datasetPath)]
        
        # 优先检查是否有Data文件夹(不区分大小写)
        has_data = any(d == 'data' for d in dirs)
        has_rawdata = any(d == 'rawdata' for d in dirs)
        
        if has_data:
            # 直接使用Data文件夹
            datasetPath = os.path.join(datasetPath, "data")
        elif has_rawdata:
            self.ui_manager.show_message_box("警告", "导入数据集不符合要求！请用辅助功能标准化数据集", "warning")
            return
        else:
            self.ui_manager.show_message_box("错误", "导入数据集不符合要求！文件夹下无Data或RawData文件夹", "critical")
            return
        
        # 检查数据文件夹下是否有分类子文件夹
        dirs = self.list_folders(datasetPath)
        typeNum = len(dirs)
        # 如果类别数量小于等于1，则显示错误提示信息并退出方法
        if typeNum <= 1:
            self.ui_manager.show_message_box("错误", "导入数据集不符合要求！Data文件夹下子文件夹数量不可≤1", "critical")
            return
        
        # 设置类别数量和类别列表
        self.typeNum = typeNum
        self.imageCategory = dirs
        

        # WT新增：在读取数据集之前，先检查所有图片是否为BMP格式
        has_non_bmp_files = False
        non_bmp_folders = []
        
        for dir in dirs:
            folder_path = os.path.join(datasetPath, dir)
            if not os.path.exists(folder_path):
                non_bmp_folders.append(f"{dir} (文件夹不存在)")
                has_non_bmp_files = True
                continue
                
            # 检查文件夹中是否有文件
            files = os.listdir(folder_path)
            if not files:
                non_bmp_folders.append(f"{dir} (空文件夹)")
                has_non_bmp_files = True
                continue
                
            # 检查是否有BMP文件
            bmp_files = [f for f in files if f.lower().endswith('.bmp')]
            if not bmp_files:
                # 检查是否有其他格式文件
                other_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif'))]
                if other_files:
                    non_bmp_folders.append(f"{dir} (包含{len(other_files)}个非BMP文件)")
                else:
                    non_bmp_folders.append(f"{dir} (没有图片文件)")
                has_non_bmp_files = True
        
        # 如果发现非BMP文件，弹出警告并停止执行
        if has_non_bmp_files:
            message = "❌ 数据集格式错误！\n\n"
            message += "检测到以下文件夹不包含BMP格式文件：\n\n"
            message += "\n".join(non_bmp_folders[:5])  # 只显示前5个
            if len(non_bmp_folders) > 5:
                message += f"\n... 还有{len(non_bmp_folders)-5}个文件夹"
            message += "\n\n请确保所有数据集文件夹都包含BMP格式的图片文件。"
            
            QMessageBox.critical(None, "BMP格式要求", message)
            # app.ms.popMessageBox.emit("critical", "BMP格式要求", message)
            self.ui_manager.show_status_message("错误：数据集必须使用BMP格式")
            # app.ms.showStatus.emit("错误：数据集必须使用BMP格式", app.statusBar)
            return
        
        # 检查是否有train、test、validation文件夹
        has_train = 'train' in dirs
        has_test = 'test' in dirs
        has_validation = 'validation' in dirs
        
        # 如果没有这些文件夹，后续会从data中划分
        if not (has_train and has_test and has_validation):
            self.ui_manager.show_status_message("请点击“开始训练”按钮进行训练")
        
            # 数据集路径已经设置为Data文件夹，无需再次处理
            # 之前已经设置过类别数量和类别列表，这里不再重复设置
            # 设置数据集信息表格的行数和列数
            self.TrainDatasetInfo.setRowCount(typeNum)
            self.TrainDatasetInfo.setColumnCount(4)
            # 设置数据集信息表格的水平表头标签
            self.TrainDatasetInfo.setHorizontalHeaderLabels(['#', 'Label', 'Shape', 'Size'])
            # 隐藏加载数据集按钮
            self.TrainLoadDataset.setVisible(False)
            # 发射信号设置加载数据集进度条的值为0
            self.TrainLoadDatasetProgressBar.setValue(0)
            # 显示加载数据集进度条和数据集信息表格
            self.TrainLoadDatasetProgressBar.setVisible(True)
            self.TrainDatasetInfo.setVisible(True)
            # 显示删除数据集按钮，并禁用
            self.TrainDeleteDataset.setVisible(True)
            self.TrainDeleteDataset.setEnabled(False)

            # 创建线程，用于读取数据集
            t = Thread(target=self.readDataset, args=(datasetPath, dirs))
            # 启动线程
            t.start()


    """
    函数名称：unloadDataset
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：卸载数据集
    """
    def unloadDataset(self):
        # 标识数据集已卸载
        self.dataset = None
        # 显示加载数据集按钮
        self.TrainLoadDataset.setVisible(True)
        # 隐藏加载数据集进度条
        self.TrainLoadDatasetProgressBar.setVisible(False)
        # 发射信号设置加载数据集进度条的值为0
        self.TrainLoadDatasetProgressBar.setValue(0)
        # 隐藏数据集信息表格
        self.TrainDatasetInfo.setVisible(False)
        # 设置数据集信息表格的行数为0
        self.TrainDatasetInfo.setRowCount(0)
        # 隐藏删除数据集按钮
        self.TrainDeleteDataset.setVisible(False)
        # 清空输入数据列表、输入数据名称列表、图像类型和类别数量
        self.inputData.clear()
        self.inputDataName.clear()
        self.datasetName = ""
        self.typeNum = 0
        # 清空图像类别列表
        self.imageCategory.clear()
        # 清空模型列表
        modelList = []
        # 填充模型选择下拉框
        # app.ms.fillComboBox.emit(modelList, app.modelSelectComboBox)
        # app.ms.fillComboBox.emit(modelList, app.modelListComboBoPbatchpredict)
        # app.ms.fillComboBox.emit(modelList, app.ComponentModelComboBox)
        
    #WTX修改删除2025-1125
    # def convert_to_rgb565(self, image):
    #     np_img = np.array(image, dtype=np.uint16)
    #     r = (np_img[..., 0] >> 3) << 11
    #     g = (np_img[..., 1] >> 2) << 5
    #     b = np_img[..., 2] >> 3
    #     rgb565 = (r | g | b).astype(np.uint16)
    #     # 再转回 RGB888 方便显示和保存
    #     r = ((rgb565 >> 11) & 0x1F) << 3
    #     g = ((rgb565 >> 5) & 0x3F) << 2
    #     b = (rgb565 & 0x1F) << 3
    #     rbg565_array = np.stack([r, g, b], axis=-1).astype(np.uint8)
    #     return Image.fromarray(rbg565_array)

    """
    函数名称：readDataset
    参数说明：datasetPath:数据集路径  dirs:数据集类别标签列表
    函数返回：无
    功能概要：读取数据集并显示数据集信息
    修改    ： WTX2025-1125修改 
    """
    def readDataset(self, datasetPath, dirs):
        # 禁用开始训练按钮
        self.ui_manager.update_dataset_loading_info("dataset_loading_started", NoneTensor)
        # 获取图片调整后的高度和宽度
        resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
        resizeWidth = self.config_manager.get("globalSettings.imageSize.width")
        # 遍历每个类别的文件夹
        for index, dir in enumerate(dirs):
            # 构建当前类别的数据集信息列表
            datasetInfo = []
            # 添加编号
            datasetInfo.append(index+1)
            # 添加类别名称
            datasetInfo.append(dir)
            # 初始化数据集大小
            datasetSize = 0
            # 构建当前类别的文件夹路径
            filedir = os.path.join(datasetPath, dir)

            # 修改：只读取BMP格式文件
            bmpFiles = [f for f in os.listdir(filedir) if f.lower().endswith('.bmp')]
            # 如果没有找到BMP文件，尝试查找其他格式并提示
            if not bmpFiles:
                otherFiles = [f for f in os.listdir(filedir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if otherFiles:
                    print(f"警告: 文件夹 {dir} 中没有BMP文件，但找到其他格式文件: {otherFiles[:3]}...")
                continue

            # # 获取文件夹中所有jpg格式的文件
            # jpgFiles = [f for f in os.listdir(filedir) if f.endswith(('.jpg', '.JPG', '.png', '.PNG'))]

            # 初始化数据集列表
            dataset = list()
            # 获取当前类别文件夹中jpg文件的数量
            bmpFileNum = len(bmpFiles)
            # 遍历当前类别的每张图片
            for i, bmpFile in enumerate(bmpFiles):
                # 将图片文件名添加到输入数据名称列表中
                self.inputDataName.append(bmpFile)
                # 构建完整的图片路径
                imagePath = os.path.join(filedir, bmpFile)
                # 统计数据集大小
                datasetSize += os.path.getsize(imagePath)

                ###WTX修改
                try:
                    # 直接读取BMP文件，保持RGB888格式
                    image = Image.open(imagePath)
                    
                    # 验证图像模式，确保是RGB
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                        print(f"转换图像模式: {bmpFile} -> RGB")
                    
                    # 调整图片大小为指定大小
                    resizedImage = image.resize((resizeWidth, resizeHeight), resample=Image.Resampling.BICUBIC)
                    
                    # 直接转换为numpy数组（RGB888格式）
                    pixels = np.array(resizedImage, dtype=np.float32)
                    
                    # 归一化处理（0-255 → 0-1）
                    pixels_normalized = pixels * (1/255.0)
                    
                    # 将处理后的像素数据添加到数据集列表中
                    dataset.append(pixels_normalized)
                    
                    # 调试信息
                    if i == 0:  # 只打印第一张图片的信息
                        print(f"[调试] 读取BMP: {bmpFile}")
                        print(f"[调试] 原始尺寸: {image.size}, 模式: {image.mode}")
                        print(f"[调试] 调整后尺寸: {resizedImage.size}")
                        print(f"[调试] 像素范围: {pixels.min()} ~ {pixels.max()}")
                        print(f"[调试] 归一化后: {pixels_normalized.min():.3f} ~ {pixels_normalized.max():.3f}")
                    
                except Exception as e:
                    print(f"错误: 无法读取图片 {bmpFile}: {e}")
                    continue

                # # 打开图片
                # image = Image.open(imagePath)
                # # 将图片转为rbg565格式
                # image = self.convert_to_rgb565(image)
                # # 调整图片大小为指定大小
                # resizedImage = image.resize((resizeWidth, resizeHeight), resample=Image.Resampling.BICUBIC)
                # 获取像素数据并进行归一化处理
                # pixels = list(resizedImage.getdata())
                # pixels = np.array(pixels, dtype=np.float32)
                # pixels_normalized = pixels * (1/255.0)
                # 将处理后的像素数据添加到数据集列表中
                # dataset.append(pixels_normalized)

                # 更新加载数据集进度条的值
                # progress = (100//len(dirs))*index+round(i/jpgFileNum*(100//len(dirs)))
                progress = (100 // len(dirs)) * index + round(i / bmpFileNum * (100 // len(dirs)))
                
                self.ui_manager.update_dataset_loading_info("progress", progress)
            # 如果当前类别的数据集不为空
            if dataset:
                # # 将数据集列表转换为numpy数组，并调整形状为（图片数量，高度，宽度，通道数）
                # dataset = np.array(dataset).reshape((jpgFileNum, resizeHeight, resizeWidth, 3))
                # # 将数据集添加到输入数据列表中
                # self.inputData.append(dataset)
                # # 添加数据集信息：数据集形状和大小
                # datasetInfo.append(dataset.shape)
                # datasetInfo.append(f'{round(datasetSize/1000)}KB')

                # 将数据集列表转换为numpy数组
                dataset_array = np.array(dataset)
                print(f"[调试] 数据集形状: {dataset_array.shape} (样本数, 高, 宽, 通道)")
                
                # 添加到输入数据列表中
                self.inputData.append(dataset_array)
                
                # 添加数据集信息：数据集形状和大小
                datasetInfo.append(dataset_array.shape)
                datasetInfo.append(f'{round(datasetSize/1000)}KB')

                # 显示数据集信息
                self.ui_manager.update_dataset_loading_info("dataset_info", (index, datasetInfo))

        self.ui_manager.update_dataset_loading_info("loading_finished", None)
         # 打印数据集统计信息
        total_samples = sum([data.shape[0] for data in self.inputData])
        print(f"[数据集统计] 总样本数: {total_samples}")
        print(f"[数据集统计] 类别数: {len(self.inputData)}")
        for i, data in enumerate(self.inputData):
            print(f"[数据集统计] 类别{i}: {data.shape[0]}个样本")




    """
    函数名称：settingsReset
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：重置训练参数为默认值
    """
    def settingsReset(self):
        # 设置epoch的默认值为20
        self.epochSpinBox.setValue(40)
        self.epochSlider.setValue(40)
        # 设置batch size的默认值为16
        self.batchsizeSpinBox.setValue(16)
        self.batchsizeSlider.setValue(16)
        # 设置学习率的默认值为0.001
        self.learningRateSpinBox.setValue(0.0005)
        self.learningRateSlider.setValue(10)
        # 设置测试数据比例的默认值为0.2
        self.testDatasetRatioSpinBox.setValue(0.28)
        self.testDatasetRatioSlider.setValue(28)
        # 设置tail的默认值为20
        self.tailSpinBox.setValue(20)
        self.tailSlider.setValue(20)
        # 设置alpha的默认值为1
        self.alphaSpinBox.setValue(1)
        self.alphaSlider.setValue(1)

    """
    函数名称：settingsChangeVal
    参数说明：app:应用程序对象 x:新的数值，根据标志(flag)的不同，表示不同的设置项的值 flag:标志，用于指示要更改的设置项类型
    函数返回：无
    功能概要：设置改变数值的方法
    """
    # @staticmethod
    def settingsChangeVal(self, x, flag):
        if flag == "epoch_spinbox":
            # 将epoch的微调框的值设置为x，并更新slider的值
            self.epochSlider.setValue(int(x))
        elif flag == "epoch_slider":
            # 将epoch的滑动条的值设置为x，并更新微调框的值
            self.epochSpinBox.setValue(int(x))
        elif flag == "batchsize_spinbox":
            # 将batch size的微调框的值设置为x，并更新slider的值
            self.batchsizeSlider.setValue(int(x)) 
        elif flag == "batchsize_slider":
            # 将batch size的滑动条的值设置为x，并更新微调框的值
            self.batchsizeSpinBox.setValue(int(x))
        elif flag == "learningRate_spinbox":
            # 将学习率的微调框的值设置为x，并更新slider的值
            self.learningRateSlider.setValue(int(x * 10000))
        elif flag == "learningRate_slider":
            # 将学习率的滑动条的值设置为x，并更新微调框的值
            self.learningRateSpinBox.setValue(x / 10000)
        elif flag == "testDataRatio_spinbox":
            # 将测试数据比例的微调框的值设置为x，并更新slider的值
            self.testDatasetRatioSlider.setValue(int(x * 1000))
        elif flag == "testDataRatio_slider":
            # 将测试数据比例的滑动条的值设置为x，并更新微调框的值
            self.testDatasetRatioSpinBox.setValue(x / 1000)
        elif flag == "tail_spinbox":
            # 将tail微调框的值设置为x，并更新slider的值
            self.tailSlider.setValue(int(x))
        elif flag == "tail_slider":
            # 将tail滑动条的值设置为x，并更新微调框的值
            self.tailSpinBox.setValue(int(x))
        elif flag == "alpha_spinbox":
            # 将alpha微调框的值设置为x，并更新slider的值
            self.alphaSlider.setValue(int(x))
        elif flag == "alpha_slider":
            # 将alpha滑动条的值设置为x，并更新微调框的值
            self.alphaSpinBox.setValue(int(x))



    """
    函数名称：changeTrainModel
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：设置不同训练模型的超参数
    """
    def changeTrainModel(self):
        # 模型名称
        module_name = self.trainModelComboBox.currentText()
        curr_dir = os.path.dirname(__file__)
        model_dir = os.path.join(curr_dir, "..", "models")
        # 模型加载路径
        module_path = os.path.join(model_dir, f"{module_name}.py")
        # 模型描述
        module_spec = importlib.util.spec_from_file_location(module_name, module_path)
        # 模型模块
        model_module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(model_module)
        # 模型超参数设置
        _custom_attrs = getattr(model_module, 'custom_attrs')

        # 设置训练轮数
        self.epochSlider.setValue(_custom_attrs['epochs'])
        # 设置批量大小
        self.batchsizeSlider.setValue(_custom_attrs['batch_size'])
        # 设置学习率
        self.learningRateSlider.setValue(_custom_attrs['learning_rate'] * 10000)

    """
    函数名称：splitData
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：将数据集按照验证集比例划分为训练集和验证集并保存到两个文件夹下
    """
    def splitData(self):
        datasetPath = self.config_manager.get("foldersPath.datasetPath")
        # 在状态栏中显示训练状态
        self.ui_manager.show_status_message("开始训练......")
        # 删除之前的拆分数据集文件夹，避免重复创建
        data_path = os.path.join(datasetPath, 'data')
        if os.path.exists(os.path.join(data_path, 'train')):
            shutil.rmtree(os.path.join(data_path, 'train'))
        if os.path.exists(os.path.join(data_path, 'validation')):
            shutil.rmtree(os.path.join(data_path, 'validation'))
        if os.path.exists(os.path.join(data_path, 'test')):
            shutil.rmtree(os.path.join(data_path, 'test'))
        # 获取界面上的测试集比例超参数    
        testRatio = self.testDatasetRatioSpinBox.value()
        # 将数据集分为训练集和测试集
        self.ui_manager.update_training_info("train_info", ("开始将数据集划分为训练集、验证集和测试集...\n\n", False))
        # 计算每个数据类别的标签
        labels = []
        for i in range(self.typeNum):
            data = self.inputData[i]
            # 生成标签数组
            label = np.full(len(data), i)
            labels.append(label)
        # 合并所有图像和标签
        images = np.vstack(self.inputData) 
        labels = np.hstack(labels) 
        images_name = self.inputDataName
        
        # 初始化变量
        train_val_index = np.array([], dtype=int)
        test_index = np.array([], dtype=int)
        train_val_images = np.array([])
        train_val_labels = np.array([])
        train_index = np.array([], dtype=int)
        val_index = np.array([], dtype=int)
        
        # 使用分层抽样将数据集分为训练集+验证集和测试集
        ss = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=0)
        for train_val_idx, test_idx in ss.split(images, labels):
            train_val_index = train_val_idx
            test_index = test_idx
            train_val_images, train_val_labels = images[train_val_index], labels[train_val_index] # 训练集+验证集图片
            self.test_images, self.test_labels = images[test_index], labels[test_index] # 测试集图片
        # train_names, test_names, train_labels, test_labels = train_test_split(images_name, labels, test_size=testRatio, stratify=labels)
        train_val_names = [images_name[i] for i in train_val_index]
        test_names =[images_name[i] for i in test_index]

        ss_train_val = StratifiedShuffleSplit(n_splits=1, test_size=testRatio, random_state=0)
        for train_idx, val_idx in ss_train_val.split(train_val_images, train_val_labels):
            train_index = train_idx
            val_index = val_idx
            self.train_images, self.train_labels = train_val_images[train_index], train_val_labels[train_index]
            self.val_images, self.val_labels = train_val_images[val_index], train_val_labels[val_index]
        
        train_names = [train_val_names[i] for i in train_index]
        val_names = [train_val_names[i] for i in val_index]
        # 将训练集图像复制到相应文件夹中
        idx = 1
        trainImgNum = len(self.train_images) if self.train_images is not None and hasattr(self.train_images, '__len__') else 0
        if (self.train_images is not None and hasattr(self.train_images, '__len__') and 
            self.train_labels is not None and hasattr(self.train_labels, '__len__') and
            len(self.train_images) > 0 and len(self.train_labels) > 0):
            for name, label in zip(train_names, self.train_labels):
                train_path = f'{datasetPath}/data/{self.imageCategory[label]}/{name}'
                target_train_path = f'{datasetPath}/train/{self.imageCategory[label]}'

                os.makedirs(target_train_path, exist_ok=True)
                shutil.copyfile(train_path, os.path.join(target_train_path, name))
                self.ui_manager.update_training_info("train_info", (f'正在拷贝训练集：{idx}/{trainImgNum}\n', True))
                idx += 1
        self.ui_manager.update_training_info("train_info", ("Done.\n", False))
        # 将验证集图像复制到相应文件夹中
        idx = 1
        valImgNum = len(self.val_images) if self.val_images is not None and hasattr(self.val_images, '__len__') else 0
        if (self.val_images is not None and hasattr(self.val_images, '__len__') and 
            self.val_labels is not None and hasattr(self.val_labels, '__len__') and
            len(self.val_images) > 0 and len(self.val_labels) > 0):
            for name, label in zip(val_names, self.val_labels):
                val_path = f'{datasetPath}/data/{self.imageCategory[label]}/{name}'
                target_val_path = f'{datasetPath}/validation/{self.imageCategory[label]}'
                os.makedirs(target_val_path, exist_ok=True)
                shutil.copyfile(val_path, os.path.join(target_val_path, name))
                self.ui_manager.update_training_info("train_info", (f'正在拷贝验证集：{idx}/{valImgNum}\n', True))
                idx += 1
        self.ui_manager.update_training_info("train_info", ("Done.\n", False))
        # 将测试集图像复制到相应文件夹中
        idx = 1
        testImgNum = len(self.test_images) if self.test_images is not None and hasattr(self.test_images, '__len__') else 0
        if (self.test_images is not None and hasattr(self.test_images, '__len__') and 
            self.test_labels is not None and hasattr(self.test_labels, '__len__') and
            len(self.test_images) > 0 and len(self.test_labels) > 0):
            for name, label in zip(test_names, self.test_labels):
                test_path = f'{datasetPath}/data/{self.imageCategory[label]}/{name}'
                target_test_path = f'{datasetPath}/test/{self.imageCategory[label]}'
                os.makedirs(target_test_path, exist_ok=True)
                shutil.copyfile(test_path, os.path.join(target_test_path, name))
                self.ui_manager.update_training_info("train_info", (f'正在拷贝测试集：{idx}/{testImgNum}\n', True))
                idx += 1
        # 在界面中显示训练集和测试集信息
        self.ui_manager.update_training_info("train_info", ("Done.\n", False))
        if self.train_images is not None and hasattr(self.train_images, 'shape'):
            self.ui_manager.update_training_info("train_info", (f"训练集数据Shape:{self.train_images.shape}\n", False))
        if self.val_images is not None and hasattr(self.val_images, 'shape'):
            self.ui_manager.update_training_info("train_info", (f"验证集数据Shape:{self.val_images.shape}\n", False))
        if self.train_images is not None and hasattr(self.train_images, 'shape'):
            self.ui_manager.update_training_info("train_info", (f"训练集数据Shape:{self.train_images.shape}\n", False))
        self.event.set()

    """
    函数名称：trainModel
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：训练模型
    """
    def trainModel(self):
        # 检查是否导入了数据集
        if not self.inputData:
            self.ui_manager.show_message_box("警告", "请先导入数据集！", "warning")
            return
        # 禁用训练按钮，避免重复点击
        self.startTrainRunning.setEnabled(False)
        # 启动分离训练集和验证集数据的线程
        t_splitData = Thread(target=self.splitData)
        # 启动训练模型的线程
        t_train = Thread(target=self.trainModelThread)
        # 启动线程
        t_splitData.start()
        t_train.start()

    """
    函数名称：trainModelThread
    参数说明：train_images:训练集图片 train_labels:训练集标签 test_images:测试集图片 test_labels:测试集标签
    函数返回：无
    功能概要：训练模型
    """
    def trainModelThread(self):
        self.event.wait()
        train_images = self.train_images
        train_labels = self.train_labels
        val_images = self.val_images
        val_labels = self.val_labels
        # 获取界面上关于训练的超参数
        epochs = self.epochSpinBox.value() # 训练轮数 20 <class 'int'>
        batchsize = self.batchsizeSpinBox.value() # 批量大小
        learningRate = self.learningRateSpinBox.value() # 学习率 0.1 <class 'float'>
        tail = self.tailSpinBox.value() # 20 <class 'int'>
        alpha = self.alphaSpinBox.value() # 0 <class 'int'>
        # 设置折线图坐标轴
        if not self.chart.empty:
            self.ui_manager.update_training_info("set_lossAcc_chart", ("clear", None))
        self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['x', (1, epochs), '轮数', 5, None]))
        self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['y', (0, 1), '损失', 11, 'l']))
        self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['y', (0, 1), '精确度', 11, 'r']))
        self.ui_manager.update_training_info("set_lossAcc_chart", ("setSeries", None))
        # 获取图像的高度和宽度以及选定的模型
        imHeight = self.config_manager.get("globalSettings.imageSize.height")
        imWidth = self.config_manager.get("globalSettings.imageSize.width")
        selectedModel = self.trainModelComboBox.currentText()
        # 根据选定的模型创建模型实例
        if selectedModel == "MobileNetv2":
            model = MobileNetv2((imHeight, imWidth, 3), k=self.typeNum)
        elif selectedModel == "NCP":
            model = NCP((imHeight, imWidth, 3), k=self.typeNum)
        else:
            # 若选择不是MobileNetv2，弹出消息框提示：xx模型还未实现
            self.ui_manager.show_message_box("提示", f"{selectedModel}模型还未实现。", "information")
            return
        # model.summary()
        # 配置模型的优化器、损失函数和评估指标
        adam = tf.keras.optimizers.Adam(learning_rate=learningRate, beta_1=0.9, beta_2=0.999,
                                            epsilon=1e-08)
        model.compile(optimizer=adam, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        # 定义自定义回调函数
        customCallback = CustomCallback(self.chart)
        # 获取当前时间
        trainTime = datetime.now()
        # 模型文件名
        modelFileName = f'{self.datasetName}_{selectedModel}_{trainTime.strftime("%y%m%d-%H%M")}.keras'
        datasetPath = self.config_manager.get("foldersPath.datasetPath")
        # 模型保存路径
        modelSavePath = f'{datasetPath}/{modelFileName}'
        # 定义模型检查点回调函数
        checkpoint = ModelCheckpoint(
            filepath=modelSavePath,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        )

        try:
            # 训练模型
            model.fit(train_images, train_labels, batch_size=batchsize, epochs=epochs,validation_data=(val_images, val_labels), callbacks=[customCallback, checkpoint])
        except Exception as e:
            # 捕获训练过程中异常并打印异常信息
            self.ui_manager.update_training_info("train_info", (f"训练过程中异常：{e}\n", False))
            self.ui_manager.show_message_box("WTX错误", str(e), "critical")
            return
            
        # 在测试集上评估模型性能
        try:
            test_loss, test_acc = model.evaluate(val_images, val_labels)
        except Exception as e:
            self.ui_manager.update_training_info("train_info", (f"评估模型时异常：{e}\n", False))
            self.ui_manager.show_message_box("错误", f"评估模型时异常：{e}", "critical")
            return
            
        # 重新加载最优模型
        best_model = None
        try:
            loaded_model = load_model(modelSavePath)
            # 确保加载的模型是Keras模型类型
            if isinstance(loaded_model, tf.keras.Model):
                best_model = loaded_model
        except Exception as e:
            self.ui_manager.update_training_info("train_info", (f"加载最优模型时异常：{e}\n", False))
            self.ui_manager.show_message_box("错误", f"加载最优模型时异常：{e}", "critical")
            return

        # 用最优模型评估
        test_loss, test_acc = best_model.evaluate(val_images, val_labels)
        # 在界面中显示测试损失和准确度信息
        self.ui_manager.update_training_info("train_info", (f"最优模型测试损失: {test_loss}\n", False))
        self.ui_manager.update_training_info("train_info", (f"最优模型测试精确度: {test_acc}\n", False))

        # 在界面中显示保存模型路径
        self.ui_manager.update_training_info("train_info", (f"保存最优模型到路径：{os.path.abspath(modelSavePath)}\n", False))
        # 将额外的信息存储到模型文件中
        try:
            with h5py.File(modelSavePath, "a") as f:
                # 检查additional_data组是否已存在，如果存在则删除
                if 'additional_data' in f:
                    del f['additional_data']
                # 创建一个组来存储额外的信息
                info_group = f.create_group('additional_data')
                # 存储额外的数据
                info_group.attrs['model'] = selectedModel if selectedModel is not None else ""
                # 确保self.imageCategory不为None
                category_data = self.imageCategory if self.imageCategory is not None else []
                info_group.create_dataset('categoryLabels', data=category_data)
                info_group.create_dataset('performance', data=[test_loss, test_acc])
        except Exception as e:
            self.ui_manager.update_training_info("train_info", (f"保存模型额外信息时异常：{e}\n", False))
            self.ui_manager.show_message_box("错误", f"保存模型额外信息时异常：{e}", "critical")
            
        # 在界面中显示保存成功
        self.ui_manager.update_training_info("train_info", ("保存成功\n", False))
        # 在状态栏中显示训练结束
        self.ui_manager.show_status_message("训练完成")
        # 启用训练按钮
        self.ui_manager.update_training_info("training_finished", True)
        self.event.clear()

    """
    函数名称：showTrainInfo
    参数说明：info:字符串，表示要显示的训练信息 cover:布尔值，表示是否覆盖原有文本内容，默认为False
    函数返回：无
    功能概要：在文本编辑框中显示训练信息
    """
    def show_train_info(self, info: str, cover: bool = False):
        # 获取文本光标
        cursor = self.trainInfoText.textCursor()
        # 如果覆盖原有内容，则选中文本并删除
        if cover:
            cursor.movePosition(QTextCursor.MoveOperation.Up, QTextCursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
        # 在光标位置插入文本
        cursor.insertText(info)
        # 确保光标可见
        self.trainInfoText.ensureCursorVisible()

    """
    函数名称：setLossAccChart
    参数说明：command:字符串，命令类型："clear"表示清空图表，"setAxis"表示设置轴，"setSeries"表示设置折线图  chart:LossAccChart对象，表示要设置的图表  axisInfo: 包含轴信息的列表
    函数返回：无
    功能概要：设置损失和准确率图表
    """
    def set_lossAcc_chart(self, command, axisInfo):
        if command == "clear":
            # 清空图表
            self.chart.clear()
        elif command == "setAxis":
            # 设置轴
            type, range, title, tickCount, position = axisInfo
            self.chart.setAxis(type, range, title, tickCount, position)
        elif command == "setSeries":
            # 设置折线图
            self.chart.setSeries()

    """
    函数名称：showDatasetInfo
    参数说明：row:整数值，表示要显示信息的行索引 info:包含数据集信息的列表 table:QTableWidget对象，用于显示数据集信息的表格
    函数返回：无
    功能概要：显示数据集信息
    """
    def show_dataset_info(self, row, infos:list):
        for index, info in enumerate(infos):
            # 将信息转换为字符串格式
            info = str(info)
            # 创建表格项
            item = QTableWidgetItem(info)
            # 设置文本对齐方式为居中
            item.setTextAlignment(Qt.AlignCenter)
            # 在表格指定位置设置表格项
            self.TrainDatasetInfo.setItem(row, index, item)

    def update_model_lsit(self, model_list: str):
        self.trainModelComboBox.clear()
        self.trainModelComboBox.addItems(model_list)

    def _handle_dataset_loading_update(self, update_type: str, data: object):
        """处理数据集加载更新信号"""
        if update_type == 'dataset_loading_started':
            # 数据集加载开始后的处理
            # 禁用删除数据集按钮
            self.TrainDeleteDataset.setEnabled(False)
            # 禁用开始训练按钮
            self.startTrainRunning.setEnabled(False)
        if update_type == 'progress':
            # 更新进度条
            self.TrainLoadDatasetProgressBar.setValue(data)
        elif update_type == 'dataset_info':
            # 显示数据集信息
            index, dataset_info = data
            self.show_dataset_info(index, dataset_info)
        elif update_type == 'loading_finished':
            # 加载完成后的处理
            # 更新进度条到100%
            self.TrainLoadDatasetProgressBar.setValue(100)
            # 启用删除数据集按钮
            self.TrainDeleteDataset.setEnabled(True)
            # 更新模型列表
            dataset_path = self.config_manager.get("foldersPath.datasetPath")
            if dataset_path and os.path.exists(dataset_path):
                # 扫描数据集路径下的所有.keras和.h5文件
                import glob
                keras_files = glob.glob(os.path.join(dataset_path, "*.keras"))
                h5_files = glob.glob(os.path.join(dataset_path, "*.h5"))
                # 获取文件名（不包含路径）并合并列表
                model_list = [os.path.basename(file) for file in keras_files + h5_files]
                # 通过信号发送更新模型列表
                # self.ui_manager.model_list_changed.emit(model_list)
            # 启用开始训练按钮
            self.startTrainRunning.setEnabled(True)

    def _handle_train_ui_update(self, update_type, data):
        """处理训练过程中的UI更新信号"""
        if update_type == 'train_info':
            # 显示训练信息
            info, cover = data
            self.show_train_info(info, cover)
        elif update_type == 'set_lossAcc_chart':
            command, axisInfo = data
            self.set_lossAcc_chart(command, axisInfo)
        elif update_type == "progress":
            self.trainModelProgressBar.setValue(data)
        elif update_type == 'training_finished':
            # 启用训练按钮
            self.startTrainRunning.setEnabled(data)

    """
    函数名称：startAutoTrain
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：自动训练模型，尝试不同的参数组合并保存结果到txt文件
    修改    ：WTX新增
    """
    def startAutoTrain(self):
        # 检查是否导入了数据集
        if not self.inputData:
            self.ui_manager.show_message_box("警告", "请先导入数据集！", "warning")
            return
        
        # 弹出参数设置对话框
        param_combinations = self.showParamDialog()
        if not param_combinations:
            return  # 用户取消
        print("获取参数成功")
        
        print("开始设置按键")
        # 禁用按钮避免重复点击
        self.startAutoTrainRunning.setEnabled(False)
        self.startTrainRunning.setEnabled(False)
        print("按键设置正常")
        # 创建结果保存文件
        result_file = os.path.join(self.config_manager.get("foldersPath.datasetPath"), f"auto_train_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        print("创建文件正常")

        # 启动自动训练线程
        t = Thread(target=self.autoTrainSimple, args=(result_file, param_combinations))
        print("设置自动训练线程完毕")
        t.daemon = True
        print("将要启动自动动训练线程")
        t.start()
        print("启动自动动训练线程")

    """
    函数名称：showParamDialog
    参数说明：app:应用程序对象
    函数返回：参数组合列表
    功能概要：显示参数设置对话框
    """
    def showParamDialog(self):
        """显示参数设置对话框"""
        dialog = ParamDialog()  # 创建自定义对话框
        if dialog.exec() == QDialog.Accepted:
            # 获取用户设置的参数组合
            param_combinations = dialog.get_params()
                    # 🔴 在这里打印参数组合
            print("=== 参数组合 ===")
            for i, (epochs, batchsize, lr) in enumerate(param_combinations):
                print(f"组合{i+1}: 轮数={epochs}, 批量={batchsize}, 学习率={lr}")
            print(f"总共有 {len(param_combinations)} 组参数")
            print("================")
            return param_combinations
        return 
    """
    函数名称：autoTrainSimple
    参数说明：result_file:结果文件路径, param_combinations:参数组合列表
    函数返回：无
    功能概要：简化的自动训练实现
    """
    def autoTrainSimple(self, result_file, param_combinations):
        try:

            # 保存原始参数
            original_epochs = self.epochSpinBox.value()
            original_batchsize = self.batchsizeSpinBox.value()
            original_learning_rate = self.learningRateSpinBox.value()
            
            # 使用传入的参数组合
            # param_combinations 现在是从对话框获取的
            
            # 禁用按钮
            self.signals.enable_buttons.emit(self.startAutoTrainRunning,False)
            self.signals.enable_buttons.emit(self.startTrainRunning,False)
            # 创建结果文件并写入表头
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write("自动训练结果报告\n")
                f.write("=" * 60 + "\n")
                f.write(f"训练时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"数据集: {self.datasetName}\n")
                f.write(f"模型: {self.trainModelComboBox.currentText()}\n")
                f.write(f"类别数: {self.typeNum}\n")
                f.write(f"参数组合数: {len(param_combinations)}\n")
                f.write("=" * 60 + "\n")
                f.write("参数组合\t测试准确率\t测试损失\t模型文件\n")
                f.write("-" * 60 + "\n")
            
            results = []
            
            # 遍历所有参数组合
            for i, (epochs, batchsize, learning_rate) in enumerate(param_combinations):
                print("开始更新UI")
                # ✅ 使用信号安全更新UI参数
                self.signals.update_ui_params.emit(epochs, batchsize, learning_rate)

                # 显示当前训练信息
                current_info = f"自动训练进度: {i+1}/{len(param_combinations)}\n"
                current_info += f"参数: 轮数={epochs}, 批量={batchsize}, 学习率={learning_rate}\n"
                #app.ms.showTrainInfo.emit(current_info, self.trainInfoText, False)
                self.ui_manager.update_training_info("train_info", (current_info, False))
                # 短暂延迟确保UI更新
                time.sleep(0.1)

                try:
                    # 等待数据分割完成
                    self.event.clear()
                    t_split = Thread(target=self.splitData)
                    t_split.start()
                    self.event.wait()
                    
                    # 获取数据
                    train_images = self.train_images
                    train_labels = self.train_labels
                    val_images = self.val_images
                    val_labels = self.val_labels

                    # 设置折线图坐标轴
                    if not self.chart.empty:
                        self.ui_manager.update_training_info("set_lossAcc_chart", ("clear", None))
                    self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['x', (1, epochs), '轮数', 5, None]))
                    self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['y', (0, 1), '损失', 11, 'l']))
                    self.ui_manager.update_training_info("set_lossAcc_chart", ("setAxis", ['y', (0, 1), '精确度', 11, 'r']))
                    self.ui_manager.update_training_info("set_lossAcc_chart", ("setSeries", None))
                    # 获取图像的高度和宽度以及选定的模型
                    imHeight = self.config_manager.get("globalSettings.imageSize.height")
                    imWidth = self.config_manager.get("globalSettings.imageSize.width")
                    selectedModel = self.trainModelComboBox.currentText()
                    
                    if selectedModel == "MobileNetv2":
                        model = MobileNetv2((imHeight, imWidth, 3), k=self.typeNum)
                    elif selectedModel == "NCP":
                        model = NCP((imHeight, imWidth, 3), k=self.typeNum)
                    else:
                        # 若选择不是MobileNetv2，弹出消息框提示：xx模型还未实现
                        self.ui_manager.show_message_box("提示", f"{selectedModel}模型还未实现。", "information")
                        continue
                    
                    # 编译模型
                    model.compile(
                        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy']
                    )
                    
                    # 定义自定义回调函数
                    customCallback = CustomCallback(self.chart)
                    
                    # 获取当前时间
                    trainTime = datetime.now()
                    
                    # 生成模型文件名
                    # modelFileName = f'{self.datasetName}_{selectedModel}_auto{i+1}_{trainTime.strftime("%y%m%d-%H%M")}.keras'
                    modelFileName = f'{self.datasetName}_{selectedModel}_{trainTime.strftime("%y%m%d-%H%M")}.keras'
                    datasetPath = self.config_manager.get("foldersPath.datasetPath")
                    # 模型保存路径
                    modelSavePath = f'{datasetPath}/{modelFileName}'
                    
                    # 设置模型检查点
                    checkpoint = ModelCheckpoint(
                        filepath=modelSavePath,
                        monitor='val_accuracy',
                        save_best_only=True,
                        mode='max',
                        verbose=1
                    )
                    
                    try:
                        # 训练模型
                        model.fit(train_images, train_labels, batch_size=batchsize, epochs=epochs,
                                validation_data=(val_images, val_labels), callbacks=[customCallback, checkpoint])
                    except Exception as e:
                        self.ui_manager.update_training_info("train_info", (f"训练过程中异常：{e}\n", False))
                        # self.ui_manager.show_message_box("错误", str(e), "critical")
                        continue
                    
                    # 在测试集上评估模型性能
                    test_loss, test_acc = model.evaluate(val_images, val_labels)

                    # 重新加载最优模型
                    best_model = load_model(modelSavePath)
                    test_loss, test_acc = best_model.evaluate(val_images, val_labels, verbose=0)

                    # 在界面中显示测试损失和准确度信息
                    self.ui_manager.update_training_info("train_info", (f"最优模型测试损失: {test_loss}\n", False))
                    self.ui_manager.update_training_info("train_info", (f"最优模型测试精确度: {test_acc}\n", False))

                    # 在界面中显示保存模型路径
                    self.ui_manager.update_training_info("train_info", (f"保存最优模型到路径：{os.path.abspath(modelSavePath)}\n", False))                 
                    
                    # 保存额外信息到模型文件
                    # try:
                    #     with h5py.File(modelSavePath, "a") as f:
                    #         # 检查additional_data组是否已存在，如果存在则删除
                    #         if 'additional_data' in f:
                    #             del f['additional_data']
                    #         # 创建一个组来存储额外的信息
                    #         info_group = f.create_group('additional_data')
                    #         # 存储额外的数据
                    #         info_group.attrs['model'] = selectedModel if selectedModel is not None else ""
                    #         # 确保self.imageCategory不为None
                    #         category_data = self.imageCategory if self.imageCategory is not None else []
                    #         info_group.create_dataset('categoryLabels', data=category_data)
                    #         info_group.create_dataset('performance', data=[test_loss, test_acc])
                    # except Exception as e:
                    #     self.ui_manager.update_training_info("train_info", (f"保存模型额外信息时异常：{e}\n", False))
                    #     # self.ui_manager.show_message_box("错误", f"保存模型额外信息时异常：{e}", "critical")
                    

                    try:
                        with h5py.File(modelSavePath, "a") as f:
                            # 检查additional_data组是否已存在，如果存在则删除
                            if 'additional_data' in f:
                                del f['additional_data']
                            # 创建一个组来存储额外的信息
                            info_group = f.create_group('additional_data')
                            # 存储额外的数据
                            info_group.attrs['model'] = selectedModel if selectedModel is not None else ""
                            # 确保self.imageCategory不为None
                            category_data = self.imageCategory if self.imageCategory is not None else []
                            info_group.create_dataset('categoryLabels', data=category_data)
                            info_group.create_dataset('performance', data=[test_loss, test_acc])
                    except Exception as e:
                        self.ui_manager.update_training_info("train_info", (f"保存模型额外信息时异常：{e}\n", False))
                        self.ui_manager.show_message_box("错误", f"保存模型额外信息时异常：{e}", "critical")
                        
                    # 记录结果
                    result = {
                        'epochs': epochs,
                        'batchsize': batchsize,
                        'learning_rate': learning_rate,
                        'test_acc': test_acc,
                        'test_loss': test_loss,
                        'model_file': modelFileName
                    }
                    results.append(result)
                    
                    # 写入结果到文件
                    with open(result_file, 'a', encoding='utf-8') as f:
                        f.write(f"轮数{epochs}-批量{batchsize}-学习率{learning_rate}\t")
                        f.write(f"{test_acc:.4f}\t{test_loss:.4f}\t{modelFileName}\n")
                    
                    # 显示当前结果
                    result_info = f"结果: 准确率={test_acc:.4f}, 损失={test_loss:.4f}\n"
                    result_info += "-" * 40 + "\n"
                    self.ui_manager.update_training_info("train_info", (result_info, False))
                    
                    # 清理内存
                    del model
                    del best_model
                    tf.keras.backend.clear_session()
                    
                except Exception as e:
                    error_msg = f"参数组合 {i+1} 训练失败: {str(e)}\n"
                    # app.ms.showTrainInfo.emit(error_msg, app.trainInfoText, False)
                    self.ui_manager.update_training_info("train_info", (error_msg, False))
                    
                    # 记录失败信息
                    with open(result_file, 'a', encoding='utf-8') as f:
                        f.write(f"轮数{epochs}-批量{batchsize}-学习率{learning_rate}\t")
                        f.write(f"训练失败\t{str(e)[:50]}...\n")
                    continue
                
            # 生成最终报告
            self.generateFinalReport(results, result_file)
            
            # 恢复原始参数
            self.signals.update_ui_params.emit(original_epochs, original_batchsize, original_learning_rate)
            
            # 启用按钮
            self.signals.enable_buttons.emit(self.startAutoTrainRunning,True)
            self.signals.enable_buttons.emit(self.startTrainRunning,True)
            
            # 显示完成信息

            self.ui_manager.show_status_message("自动训练完成！")

            # app.ms.showStatus.emit("自动训练完成！", app.statusBar)
            #app.ms.showTrainInfo.emit(f"\n自动训练完成！结果保存至: {result_file}\n", app.trainInfoText, False)
            self.ui_manager.update_training_info("train_info", f"\n自动训练完成！结果保存至: {result_file}\n", False)
        except Exception as e:
            error_msg = f"自动训练异常: {str(e)}\n"
            self.ui_manager.update_training_info("train_info", (error_msg, False))
            # app.ms.showTrainInfo.emit(error_msg, app.trainInfoText, False)
            
            # 恢复按钮状态
            self.signals.enable_buttons.emit(self.startAutoTrainRunning,True)
            self.signals.enable_buttons.emit(self.startTrainRunning,True)

    """
    函数名称：generateFinalReport
    参数说明：results:结果列表, result_file:结果文件路径
    函数返回：无
    功能概要：生成最终训练报告
    """
    def generateFinalReport(self, results, result_file):
        if not results:
            return
        
        # 按测试准确率排序
        results.sort(key=lambda x: x['test_acc'], reverse=True)
        
        # 追加最终报告到文件
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write("最终训练报告\n")
            f.write("=" * 60 + "\n")
            f.write("性能排名:\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"{i}. 准确率: {result['test_acc']:.4f}, 损失: {result['test_loss']:.4f}\n")
                f.write(f"   参数: 轮数={result['epochs']}, 批量={result['batchsize']}, 学习率={result['learning_rate']}\n")
                f.write(f"   模型: {result['model_file']}\n\n")
            
            # 最佳结果
            best = results[0]
            f.write("最佳参数组合:\n")
            f.write(f"准确率: {best['test_acc']:.4f}\n")
            f.write(f"损失: {best['test_loss']:.4f}\n")
            f.write(f"轮数: {best['epochs']}, 批量: {best['batchsize']}, 学习率: {best['learning_rate']}\n")
            f.write(f"模型文件: {best['model_file']}\n")
            
            # 统计信息
            f.write(f"\n统计信息:\n")
            f.write(f"总尝试次数: {len(results)}\n")
            f.write(f"最佳准确率: {best['test_acc']:.4f}\n")
            f.write(f"平均准确率: {sum(r['test_acc'] for r in results) / len(results):.4f}\n")
            f.write(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 在界面显示最佳结果
        best_result = results[0]
        best_info = f"\n🎉 自动训练完成！最佳结果:\n"
        best_info += f"准确率: {best_result['test_acc']:.4f}\n"
        best_info += f"参数: 轮数={best_result['epochs']}, 批量={best_result['batchsize']}, 学习率={best_result['learning_rate']}\n"
        best_info += f"详细结果保存至: {result_file}\n"
        
        # app.ms.showTrainInfo.emit(best_info, app.trainInfoText, False)
        self.ui_manager.update_training_info("train_info", (best_info, False))
        
