# 导入QT模块
from PySide6.QtWidgets import QFileDialog, QSizePolicy, QAbstractButton, QVBoxLayout, QHeaderView, QWidget, QTableWidgetItem
from PySide6.QtCore import QBuffer, QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from tensorflow.python.framework.ops import uid


# 导入工程模块
from P03_Components.customLabel import CustomLabel
from P03_Components.customCornerWidget import CustomCornerWidget
from P07_View.Qt_Designer_ui_py.Ui_ModelPredictWidget import Ui_ModelPredictWidget
from P06_Utils.services_bus.ui_manager import UIManager
from P06_Utils.services_bus.config_manager import ConfigManager
from P06_Utils.services_bus.serial_port_manager import SerialPortManager
from P06_Utils.services_bus.services_bus import service_bus, ServiceID

# 导入其他模块
import struct
from PIL import Image
import numpy as np
import h5py
from keras.models import load_model
import tensorflow as tf
from keras import backend as K
import os
import copy
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path



"""
类名：ModelValidation
基类：无
功能：模型验证类
"""
class ModelPredictWidget(Ui_ModelPredictWidget):

    """
    函数名称：__init__
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：初始化方法，设置模型验证界面的初始状态和信号连接
    """
    def __init__(self):
        super().__init__()
        #====================================添加变量====================================#
        # 控件实例
        self.__model_predict_widget = QWidget()
        self.setupUi(self.__model_predict_widget)
        # 获取管理器实例
        self.ui_manager: UIManager = service_bus.get_service(ServiceID.UI_MANAGER)
        self.config_manager: ConfigManager = service_bus.get_service(ServiceID.CONFIG_MANAGER)
        self.serial_port_manager: SerialPortManager = service_bus.get_service(ServiceID.SERIAL_PORT_MANAGER)
        # 图像数据测试集路径
        self.pictureTestData = ""
        # 图像标签
        self.dataLabels = []
        self.image_path = ""
        # 初始化当前可用串口列表为空
        self.currentSerials = []
        # 显示测试集路径的label
        self.PicTestDataPathLabel = CustomLabel(parent=self.frame_75)
        # 设置表格corner
        cornerWidget = CustomCornerWidget("类别名称\评估指标")
        # app.evaluationMetrixTable.setCornerWidget(cornerWidget)
        cornerButton = self.evaluationMetrixTable.findChild(QAbstractButton)
        lay = QVBoxLayout(cornerButton)
        # 当前串口列表
        self.serial_ports = []
        self.model_list = []
        #====================================设置UI=====================================#
        self.horizontalLayout_66.insertWidget(5, self.PicTestDataPathLabel)
        # 设置左上角（交点）可见
        self.evaluationMetrixTable.setVerticalHeaderLabels(["Header 1"])
        cell = self.evaluationMetrixTable.verticalHeaderItem(0)
        cell.setText("")
        self.evaluationMetrixTable.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        lay.addWidget(cornerWidget)

        #====================================绑定信号与槽=====================================#
        # 刷新模型列表
        self.ui_manager.update_model_list.connect(self.refreshModelList)
        # 连接导入图像按钮的点击信号到打开图像的槽函数
        self.import1Img.clicked.connect(self.openImage)

        # 连接删除图像按钮的点击信号到清除图像标签的槽函数
        # self.delete1Img.clicked.connect(self.closeImage)

        # 连接开始预测按钮的点击信号到开始预测的槽函数
        self.startPredictionBtn.clicked.connect(self.startPrediction)
        self.importBatchImg.clicked.connect(self.loadTestData)
        # 连接删除批量图片按钮的点击信号到删除测试集的槽函数
        self.deleteBatchImg.clicked.connect(self.unloadTestData)
        # 连接批量图片预测的点击信号到批量图片预测的槽函数
        self.startBatchPredictionBtn.clicked.connect(self.startBatchPredict)
        # 连接打开串口按钮的点击信号到打开串口的槽函数
        #self.openSerialButton.clicked.connect(self.btnOpenClosePortclicked)
        # 连接导入图像按钮的点击信号到导入图像的槽函数
        #self.importImageButton_3.clicked.connect(self.btnSelectImageclicked)
        # 连接发送图像按钮的点击信号到发送图像的槽函数
        #self.sendImageButton.clicked.connect(self.btnSendDataclicked)
        # 连接串口数据接收的信号到更新数据的槽函数
        # self.serial_port_manager.add_ports_updated_handler(self.update_ports)

    def get_widget(self):
        return self.__model_predict_widget

    """
    函数名称：openImage
    参数说明：无
    函数返回：无
    功能概要：导入预测图片
    修改   ： WTX2025-1127修改打开图片为bmp
    """
    def openImage(self):
        #显示状态栏消息，提示正在导入图片
        self.ui_manager.show_status_message("正在导入图片...")
        # 设置打开文件对话框的初始文件夹
        # 如果有上次选择的目录，使用上次的目录；否则使用项目根目录
        image_path = self.config_manager.get("foldersPath.imagePath")

        if not image_path or not os.path.exists(image_path):
            image_path = self.config_manager.get("foldersPath.defaultPath")

        filepath, _ = QFileDialog.getOpenFileName(self.__model_predict_widget, "选择一张图片", image_path, "Image(*.png;*.jpg;*.bmp)")
         # 如果选择了文件
        if filepath:
            self.image_path = filepath
            # 保存本次选择的文件目录，供下次使用
            self.config_manager.set("foldersPath.imagePath", os.path.dirname(filepath))
            self.config_manager.save_config()
            
            # 使用Pillow读取图片
            pil_image = Image.open(filepath) 
            # 如果图片读取失败
            if pil_image is None:
                # 显示状态栏消息，提示导入图片失败
                self.ui_manager.show_status_message("导入图片失败。")
                
                # 弹出消息框，提示导入图片路径中不能包含中文
                self.ui_manager.show_message_box("警告", "导入图片路径中不能包含中文！", "warning")
                return
            else:
                # 显示状态栏消息，提示导入图片成功
                self.ui_manager.show_status_message("导入图片成功！")
            
            # 触发加载图片的信号，将图片显示在标签上
            np_image = np.array(pil_image)
            self.showImage(np_image, self.imageLabel)
        else:
            # 显示状态栏消息，提示取消导入图片
            self.ui_manager.show_status_message("取消导入图片")

    """
    函数名称：showImage
    参数说明：img_src:待显示的图片 (numpy array) label:显示图片的QLabel对象
    函数返回：无
    功能概要：显示图片在标签上，并根据标签大小调整图片尺寸
    """
    def showImage(self, img_src, label):
        try:
            # 获取图片的高度和宽度
            ih, iw, _ = img_src.shape
            # 获取标签的margin
            # margins = label.contentsMargins()
            # 获取标签的宽度和高度
            w = label.geometry().width() - 6
            h = label.geometry().height() - 6
            # 判断图片宽度与标签宽度的比例和图片高度与标签高度的比例
            if iw/w > ih/h:
                # 如果宽度比例大于高度比例，则按宽度比例缩放
                scal = w / iw
                # 新的宽度为标签宽度
                nw = w
                # 按比例计算新的高度
                nh = int(scal * ih)
            else:
                # 如果高度比例大于宽度比例，则按高度比例缩放
                scal = h / ih
                # 按比例计算新的宽度
                nw = int(scal * iw)
                # 新的高度为标签高度
                nh = h
            pil_image = Image.fromarray(img_src)
            # 缩放图片
            resized_image = pil_image.resize((nw, nh), resample=Image.BICUBIC)
            # 设置标签内容水平垂直居中
            label.setAlignment(Qt.AlignCenter)
            
            # 将图片数据转换为QImage对象
            img = QImage(resized_image.tobytes(), resized_image.width, resized_image.height, resized_image.width * len(resized_image.mode), QImage.Format_RGB888)
            # 清空标签内容
            label.clear()
            # 在标签上显示图片
            label.setPixmap(QPixmap.fromImage(img))   
            
        except Exception as e:
            # 打印异常信息
            self.ui_manager.show_message_box("警告", str(e), "warning")
            print(repr(e))

    # def closeImage(self):
    #     self.imageLabel.clear()
    #     self.predictionResult.clear()
    #     self.confidenceLevel.clear()
    #     self.forecastProgressBar.setValue(0)
    #     pass

    """
    函数名称：refreshModelList
    参数说明：comboBox:QComboBox对象，表示要刷新的模型列表下拉框
    函数返回：无
    功能概要：刷新模型列表下拉框
    """
    def refreshModelList(self, model_list: list):
        if model_list != self.model_list:
            self.model_list = model_list
            # 清空下拉框中的选项
            self.modelListComboBox_batchpredict.clear()
            self.modelSelectComboBox.clear()
            # 获取模型文件夹中的模型列表，并按创建时间降序排序
            # 将模型列表添加到下拉框中
            self.modelListComboBox_batchpredict.addItems(model_list)
            self.modelSelectComboBox.addItems(model_list)

    def convert_to_rgb565(self, image):
        np_img = np.array(image, dtype=np.uint16)
        r = (np_img[..., 0] >> 3) << 11
        g = (np_img[..., 1] >> 2) << 5
        b = np_img[..., 2] >> 3
        rgb565 = (r | g | b).astype(np.uint16)
        # 再转回 RGB888 方便显示和保存
        r = ((rgb565 >> 11) & 0x1F) << 3
        g = ((rgb565 >> 5) & 0x3F) << 2
        b = (rgb565 & 0x1F) << 3
        rbg565_array = np.stack([r, g, b], axis=-1).astype(np.uint8)
        return Image.fromarray(rbg565_array)
    """
    函数名称：startPrediction
    参数说明：无
    函数返回：无
    功能概要：预测导入的图片
    修改   ： WTX2025-1127去掉格式RGB888-RGB555的转换
    """
    def startPrediction(self):
        # 获取选择的模型文件名
        selectedModelFile = self.modelSelectComboBox.currentText()
        if not selectedModelFile:
            self.ui_manager.show_message_box("警告", "还未选择模型文件", "warning")
            
            return
        # 检查是否有选择图像文件路径
        if not hasattr(self, 'image_path') or not self.image_path:
            self.ui_manager.show_message_box("警告", "还未上传图片！", "warning")
            return
        
        # 直接使用QImage读取原始图像文件
        original_image = QImage(self.image_path)
        if original_image.isNull():
            self.ui_manager.show_message_box("警告", "图像文件读取失败！", "warning")
            return
            
        # 转换为RGB888格式
        qimage = original_image.convertToFormat(QImage.Format.Format_RGB888)
        
        # 获取需要调整的图像尺寸
        resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
        resizeWidth = self.config_manager.get("globalSettings.imageSize.width")
        
        # 缩放图像到目标尺寸
        qimage = qimage.scaled(resizeWidth, resizeHeight, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        # 获取图像数据
        rgb888Data = qimage.constBits()
        np_img = np.frombuffer(rgb888Data, dtype=np.uint8).reshape((resizeHeight, resizeWidth, 3))
        
        # 直接使用RGB888数据，不再转换为RGB565
        pixels = np_img.astype(np.uint8)

        # # RGB565转换（保持与原始convert_to_rgb565函数相同的逻辑）
        # np_img_uint16 = np_img.astype(np.uint16)
        # r = (np_img_uint16[..., 0] >> 3) << 11
        # g = (np_img_uint16[..., 1] >> 2) << 5
        # b = np_img_uint16[..., 2] >> 3 
        # rgb565 = (r | g | b).astype(np.uint16)
        # # 转回RGB888
        # r = ((rgb565 >> 11) & 0x1F) << 3
        # g = ((rgb565 >> 5) & 0x3F) << 2
        # b = (rgb565 & 0x1F) << 3
        # pixels = np.stack([r, g, b], axis=-1).astype(np.uint8)
        
        # 保存处理后的图像数据供下位机发送使用
        self.processed_image_data = pixels.copy()
        
        # 调试信息：保存处理后的数据统计
        # print(f"[调试] 预测数据统计: shape={pixels.shape}, min={pixels.min()}, max={pixels.max()}, mean={pixels.mean():.6f}")
        # print(f"[调试] 预测数据前10个像素: {pixels.flatten()[:10]}")
        
        # 归一化像素数据
        pixels_normalized = pixels * (1/255.0) 
        # 添加批次维度，从(H, W, 3)变为(1, H, W, 3)以符合模型输入要求
        inputImg = np.expand_dims(pixels_normalized, axis=0)

        dataset_path = self.config_manager.get("foldersPath.datasetPath")

        if not dataset_path or not os.path.exists(dataset_path):
            self.ui_manager.show_message_box("警告", "数据集路径不存在！", "warning")
            return
        try:
            model_path = os.path.join(dataset_path, selectedModelFile)
            # 打开模型文件，读取额外数据
            with h5py.File(model_path, mode="r") as hdf:
                infoGroup = hdf.get("additional_data")
                if infoGroup is None:
                    self.ui_manager.show_message_box("错误", "该模型文件缺少 additional_data 元信息，请重新训练并保存模型。", "critical")
                    return
                # 获取图像类比标签
                category_data = infoGroup.get('categoryLabels')
                if category_data is None:
                    self.ui_manager.show_message_box("错误", "该模型文件缺少类别标签信息，请重新训练并保存模型。", "critical")
                    return
                category = [x.decode('utf-8') for x in list(category_data)]
            # 加载模型
            model = load_model(model_path, custom_objects={})
            
            # 进度条设置为0%
            self.forecastProgressBar.setValue(0)
            # 软件底部状态栏显示"开始预测！"
            self.ui_manager.show_status_message("开始预测！")
            # 进行图像预测
            predictResult = model.predict(inputImg)
            predictResult = predictResult.flatten().tolist()

            # 显示预测结果
            # 获取预测结果中的最大值（最高置信水平）
            confLevel = max(predictResult)
            # 根据最高置信水平的索引获取对应的图像类别
            imgType = category[predictResult.index(confLevel)]
            # 设置图像类别标签的文本为预测的图像类别
            self.predictionResult.setText(imgType)
            # 设置置信水平标签的文本为最高置信水平的百分比，并保留两位小数
            self.confidenceLevel.setText(f'{round(confLevel*100, 2)}%')   

            # 进度条设置为100%
            self.forecastProgressBar.setValue(100)
            # 软件底部状态栏显示"预测结束。"
            self.ui_manager.show_status_message("预测结束。")


        except Exception as e:
            self.ui_manager.show_message_box("错误", str(e), "critical")
            # 捕捉异常并忽略
            pass

    def loadTestData(self):
        # 显示状态栏消息，提示正在导入测试集
        self.ui_manager.show_status_message("正在导入测试集...")
        # 打开文件夹选择对话框
        dataset_path = self.config_manager.get("foldersPath.datasetPath")
        if not dataset_path or not os.path.exists(dataset_path):
            self.ui_manager.show_message_box("警告", "数据集路径不存在！", "warning")
            return
        datasetPath = QFileDialog.getExistingDirectory(self.__model_predict_widget, "导入测试集", dataset_path)
        # 如果未选择文件夹，则退出
        if not datasetPath:
            self.ui_manager.show_status_message("取消导入测试集")
            return
        # 如何选择的文件夹名称不是test，则测试数据集不符合要求，退出
        basename = os.path.basename(datasetPath)
        if basename != "test":
            self.ui_manager.show_message_box("错误", "导入数据集不符合要求！", "critical")
            self.ui_manager.show_status_message("导入数据集不符合要求！.")
            
            return
        # 如果此时已经有测试集导入，则需要把表格清空
        if self.pictureTestData != "":
            self.unloadTestData()
        # 若test文件夹下没有子文件夹，则不符合要求，退出
        labels = [dir for dir in os.listdir(datasetPath) if os.path.isdir(os.path.join(datasetPath, dir))]
        if labels == []:
            self.ui_manager.show_message_box("错误", "测试集中无数据集！", "critical")
            self.ui_manager.show_status_message("测试集中无数据集！.")
            return
        # 数据集符合要求，在界面显示测试集路径
        self.pictureTestData = datasetPath
        self.dataLabels = labels
        self.PicTestDataPathLabel.setContent(f"测试集路径：{datasetPath}")
        # 隐藏提示语及提示图标
        self.label_28.setVisible(False)
        self.label_29.setVisible(False)
        self.evaluationMetrixTable.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.ui_manager.show_status_message("导入测试集成功")
        
        # 在界面显示评估指标表格
        verticalHeader = copy.deepcopy(labels) 
        verticalHeader.extend(['宏平均（Macro-Averaged）', '准确率（Accuracy）'])
        self.initTable(len(verticalHeader), False, False, verticalHeader)
        
    def unloadTestData(self):
        self.pictureTestData = ""
        self.PicTestDataPathLabel.setContent("")
        # 删除表格数据
        self.initTable(1, False, False, [""])
        self.fillTable([["","",""]])
        # 显示提示语和提示图标
        self.label_28.setVisible(True)
        self.label_29.setVisible(True)
        self.evaluationMetrixTable.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        self.ui_manager.show_status_message("删除测试集成功")
        self.batchTestProgressBar.setValue(0)
    #整体预测
    def startBatchPredict(self):
        if self.pictureTestData == "":
            self.ui_manager.show_message_box("警告", "还未导入测试集！", "warning")
            return
        # 获取选择的模型文件名
        selectedModelFile = self.modelListComboBox_batchpredict.currentText()
        # print(f"预测选择的模型文件为：{selectedModelFile}")
        if not selectedModelFile:
            self.ui_manager.show_message_box("警告", "还未选择模型文件", "warning")
            return

        dataset_path = self.config_manager.get("foldersPath.datasetPath")
        if not dataset_path or not os.path.exists(dataset_path):
            self.ui_manager.show_message_box("警告", "数据集路径不存在！", "warning")
            return

        try:
            self.ui_manager.show_status_message("开始评估")
            # 加载模型
            model = load_model(f"{dataset_path}/{selectedModelFile}", custom_objects={})
            # 获取需要调整的图像尺寸
            resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
            resizeWidth = self.config_manager.get("globalSettings.imageSize.width")
            images = []
            true_labels = []
            img_num = 0
            for idx, class_name in enumerate(self.dataLabels):
                class_folder = os.path.join(self.pictureTestData, class_name)
                for i, img_name in enumerate(os.listdir(class_folder)) :
                    jpgFileNum = len(os.listdir(class_folder))
                    img_path = os.path.join(class_folder, img_name)
                    img = Image.open(img_path)
                    img = self.convert_to_rgb565(img)
                    img = img.resize((resizeHeight, resizeWidth), resample=Image.Resampling.BICUBIC)
                    img_array = np.array(img) / 255.0 # 归一化
                    inputImg = img_array.reshape((1, resizeHeight, resizeWidth, 3))
                    images.append(inputImg)
                    true_labels.append(idx)
                    img_num += 1
                    # 更新加载数据集进度条的值
                    self.batchTestProgressBar.setValue((100//len(self.dataLabels))*idx+round(i/jpgFileNum*(100//len(self.dataLabels))))
            images = np.array(images).reshape((img_num, resizeHeight, resizeWidth, 3))
            prediction = model.predict(images)
            pred_labels = np.argmax(prediction, axis=1).tolist()
            # 精确率 
            normal_precision = precision_score(true_labels, pred_labels, average=None, zero_division=1)
            # print("精确率：", normal_precision)
            # 召回率
            normal_recall = recall_score(true_labels, pred_labels, average=None, zero_division=1)
            # print("召回率：", normal_recall)
            # F1-score
            normal_f1_score = f1_score(true_labels, pred_labels, average=None, zero_division=1)
            # print("f1-score:", normal_f1_score)
            # 宏平均精确度
            macro_precision = precision_score(true_labels, pred_labels, average='macro', zero_division=1)
            # print("宏平均精确率：", macro_precision)
            # 宏平均召回率
            macro_recall = recall_score(true_labels, pred_labels, average='macro', zero_division=1)
            # print("宏平均召回率：", macro_recall)
            # 宏平均f1-score
            macro_f1_score = f1_score(true_labels, pred_labels, average='macro', zero_division=1)
            # print('宏平均：', macro_f1_score)
            # 准确率
            normal_accuracy = accuracy_score(true_labels, pred_labels)
            # print('准确率：', normal_accuracy)
            # 组装表格数据
            matrix = []
            for i in range(len(self.dataLabels)):
                class_matrix = []
                class_matrix.append(f"{round(float(normal_precision[i])*100, 3)}%")
                class_matrix.append(f"{round(float(normal_recall[i])*100, 3)}%")
                class_matrix.append(f"{round(float(normal_f1_score[i])*100, 3)}%")
                matrix.append(class_matrix)
            matrix.append([f"{round(macro_precision*100, 3)}%", f"{round(macro_recall*100, 3)}%", f"{round(macro_f1_score*100, 3)}%"])
            matrix.append([f"{round(normal_accuracy*100, 3)}%"])
            self.fillTable(matrix)
            self.batchTestProgressBar.setValue(100)
            self.ui_manager.show_status_message("评估结束")
            
        except Exception as e:
            self.ui_manager.show_message_box("错误", str(e), "critical")
            # 捕捉异常并忽略
            pass

    def initTable(self, rowCount:int, colCount:int, horizontalHeader:int, verticalHeader):
        if rowCount:
            self.evaluationMetrixTable.setRowCount(rowCount)
        if colCount:
            self.evaluationMetrixTable.setColumnCount(colCount)
        if horizontalHeader:
            self.evaluationMetrixTable.setHorizontalHeaderLabels(horizontalHeader)
        if verticalHeader:
            self.evaluationMetrixTable.setVerticalHeaderLabels(verticalHeader)
        self.evaluationMetrixTable.setGridStyle(Qt.PenStyle.SolidLine)

    def fillTable(self, data:list):
        for row, line in enumerate(data):
            for col, info in enumerate(line):
                item = QTableWidgetItem(info)
                item.setTextAlignment(Qt.AlignCenter)  # 居中显示
                self.evaluationMetrixTable.setItem(row, col, item)
                if len(line) == 1:
                    self.evaluationMetrixTable.setSpan(row, col, 1, self.evaluationMetrixTable.columnCount()-col-1)

    #======================================一下代码为下位机验证的代码=======================================#

    # """
    # 函数名称：update_ports
    # 参数说明：app:应用程序对象 
    # 函数返回：无
    # 功能概要：# 更新串口列表
    # """
    # def update_ports(self, ports: list):
    #     if ports != self.serial_ports:
    #         self.serial_ports = ports
    #         # 清空下拉框中的选项
    #         self.selectSerialComboBox.clear()
    #         # 将串口列表添加到下拉框中
    #         self.selectSerialComboBox.addItems(ports)        # 如果当前串口列表与之前不同
    
    """
    函数名称：btnOpenClosePortclicked
    参数说明：无
    函数返回：无
    功能概要：打开关闭串口按钮事件槽函数，单击时按钮显示"打开串口/关闭串口"切换，
             实现选中的串口号与波特率打开或关闭串口
    """
    # def btnOpenClosePortclicked(self):
    #     # 打开串口
    #     if self.openSerialButton.text()==u"打开串口":
    #         PortName=self.selectSerialComboBox.currentText()
    #         BaudRate=int(self.selectBaudrateComboBox.currentText())
    #         # 关闭当前已打开的串口 这是为了防止打开不同的串口时 前一个串口没有正确关闭
    #         self.serial_port_manager.create_port(PortName)
    #         isOpen = self.serial_port_manager.connect_port(PortName)
    #         if not isOpen:
    #             # 在状态栏显示打开失败消息
    #             self.ui_manager.show_message_box("错误", "打开串口失败", "critical")
    #             self.ui_manager.show_status_message(u"状态：打开串口" + PortName+"失败")
    #             return
    #         self.openSerialButton.setText(u"关闭串口")
    #         self.ui_manager.show_status_message(message=u"状态：打开串口" + PortName+","+str(BaudRate)+u"  无校验位,8位数据位,1位停止位")
    #     # 关闭串口
    #     else:
    #         PortName=self.selectSerialComboBox.currentText()

    #         # 关闭串口连接
    #         is_closed = self.serial_port_manager.disconnect_port(PortName)
    #         if is_closed:
    #             self.openSerialButton.setText("打开串口")
    #             # 在状态栏显示串口关闭消息
    #             self.ui_manager.show_status_message(f"串口{PortName}已关闭")
    #             self.serial_no = ""
    #         else:
    #             self.ui_manager.show_status_message(f"串口{PortName}关闭失败")

    #         self.openSerialButton.setText(u"打开串口")
            
    # """
    # 函数名称：btnSendDataclicked
    # 入口参数：无
    # 函数返回：无
    # 功能描述：通过串口发送图像数据给下位机
    # 调用方法：不直接调用
    # """
    # def btnSendDataclicked(self):
    #     try:
    #         self.ui_manager.show_status_message(u"状态：开始发送数据")
            
    #         # 检查是否有选择图像文件路径
    #         if not hasattr(self, 'image_path') or not self.image_path:
    #             self.ui_manager.show_message_box("警告", "请先选择图像文件！", "warning")
                
    #             return
            
    #         # 使用与预测完全相同的图像处理流程
    #         # 直接使用QImage读取原始图像文件
    #         original_image = QImage(self.image_path)
    #         if original_image.isNull():
    #             self.ui_manager.show_message_box("警告", "图像文件读取失败！", "warning")
    #             return
                
    #         # 转换为RGB888格式
    #         qimage = original_image.convertToFormat(QImage.Format.Format_RGB888)
            
    #         # 获取需要调整的图像尺寸（使用配置文件中的尺寸）
    #         resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
    #         resizeWidth = self.config_manager.get("globalSettings.imageSize.width")
            
    #         # 缩放图像到目标尺寸（与预测时相同的方式）
    #         qimage = qimage.scaled(resizeWidth, resizeHeight, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
    #         # 获取图像数据
    #         rgb888Data = qimage.constBits()
    #         np_img = np.frombuffer(rgb888Data, dtype=np.uint8).reshape((resizeHeight, resizeWidth, 3))
            
    #         # RGB565转换（保持与原始convert_to_rgb565函数相同的逻辑）
    #         np_img_uint16 = np_img.astype(np.uint16)
    #         r = (np_img_uint16[..., 0] >> 3) << 11
    #         g = (np_img_uint16[..., 1] >> 2) << 5
    #         b = np_img_uint16[..., 2] >> 3 
    #         rgb565 = (r | g | b).astype(np.uint16)
    #         # 转回RGB888
    #         r = ((rgb565 >> 11) & 0x1F) << 3
    #         g = ((rgb565 >> 5) & 0x3F) << 2
    #         b = (rgb565 & 0x1F) << 3
    #         pixels = np.stack([r, g, b], axis=-1).astype(np.uint8)
            
    #         # 按照每一行每一列 RGB 三色的格式添加数据
    #         byte_stream = bytearray()
            
    #         # 调试信息：对比发送数据和预测数据
    #         print(f"[调试] 发送数据统计: shape={pixels.shape}, min={pixels.min()}, max={pixels.max()}, mean={pixels.mean():.6f}")
    #         print(f"[调试] 发送数据前10个像素: {pixels.flatten()[:10]}")
            
    #         # 对比预测数据和发送数据是否一致
    #         if hasattr(self, 'processed_image_data') and self.processed_image_data is not None:
    #             data_identical = np.array_equal(pixels, self.processed_image_data)
    #             print(f"[调试] 预测数据和发送数据是否一致: {data_identical}")
    #             if not data_identical:
    #                 diff = np.abs(pixels.astype(int) - self.processed_image_data.astype(int))
    #                 print(f"[调试] 数据差异统计: maPdiff={diff.max()}, mean_diff={diff.mean():.6f}")
    #         else:
    #             print("[调试] 警告：未找到预测数据，无法对比")
    #         for i in range(resizeHeight):
    #             for j in range(resizeWidth):
    #                 r = int(pixels[i][j][0])
    #                 g = int(pixels[i][j][1])
    #                 b = int(pixels[i][j][2])
    #                 byte_stream.append(r)
    #                 byte_stream.append(g)
    #                 byte_stream.append(b)

    #         byte_stream = self._build_packet(byte_stream)
    #         # 使用串口发送数据
    #         PortName = self.selectSerialComboBox.currentText()
    #         self.serial_port_manager.send_data(PortName, byte_stream)

    #         self.ui_manager.show_status_message(u"状态：发送数据结束（使用与预测相同的处理流程）")
            
    #     except Exception as e:
    #         self.ui_manager.show_message_box("警告", "发送失败！", "warning")
    #         self.ui_manager.show_status_message(u"状态：发送数据失败-" + str(e))


    """
    函数名称：btnClearImageclicked
    入口参数：无
    函数返回：无
    功能描述：清除选中图片数据
    调用方法：不直接调用
    """
    def btnClearImageclicked(self):
        self.showImageLabel.clear()
        self.ui_manager.show_status_message(u"状态：清除图片")

    # """
    # 函数名称：btnSelectImageclicked
    # 入口参数：无
    # 函数返回：无
    # 功能描述：加载选中图片
    # 调用方法：不直接调用
    # """
    # def btnSelectImageclicked(self):
    #     try:
    #         self.ui_manager.show_status_message(u"状态：选择图片")
    #         self.image_path = QFileDialog.getOpenFileName(self.__model_predict_widget, "选择图片", "", "Image Files(*.jpg *.gif *.png *.bmp *.jpeg *.tif *.tiff)")[0]
            
    #         self.config_manager.set("foldersPath.imagePath", self.image_path)
    #         self.config_manager.save_config()
            
    #         originalImage = QImage(self.image_path)

    #         self.image_width = originalImage.width()
    #         self.image_height = originalImage.height()

    #         # 计算缩放比例
    #         target_width, target_height = self.showImageLabel.width(), self.showImageLabel.height()
            
    #         # 计算保持比例的缩放尺寸
    #         ratio = min(target_width / self.image_width, target_height / self.image_height)
    #         new_width = int(self.image_width * ratio)
    #         new_height = int(self.image_height * ratio)

    #         # 缩放图像
    #         scaled = originalImage.scaled(
    #             new_width, new_height,
    #             Qt.AspectRatioMode.KeepAspectRatio,
    #             Qt.TransformationMode.SmoothTransformation
    #         )

    #         pixmap = QPixmap(scaled)
    #         self.showImageLabel.setAlignment(Qt.AlignCenter)
    #         self.showImageLabel.setPixmap(pixmap)

    #         self.ui_manager.show_status_message(u"状态：图片" + self.image_path +"加载成功")
    #     except Exception as e:
    #         self.ui_manager.show_status_message(u"状态：选择图片失败" + str(e))
    #         self.ui_manager.show_message_box("警告", str(e), "warning")



    class PacketInfo:           # 数据帧信息
        SYNC_WORD = 0xAA55      # 同步字
        ACK = 0x06              # 应答
        NAK = 0x15              # 无应答
        DATA_LENGTH = 160*3     # 数据区长度
        SYNC_WORD_SIZE = 2      # 同步字长度
        CHECKSUM_SIZE = 1       # 校验和长度

    """
    函数名称：_build_packet
    入口参数：data: 数据帧数据
    函数返回：data: 完整帧数据
    功能描述：将数据帧打包成packet
    调用方法：将要包装的真实数据传入
    """
    def _build_packet(self, data: bytes) -> bytes:
        # 打包帧头 + 帧号
        header_sync = struct.pack('<H', self.PacketInfo.SYNC_WORD)
        # 计算校验和
        checksum = self.crc16_modbus(header_sync + data)

        return header_sync + data + struct.pack('<H', checksum)
    
    """
    函数名称：crc16_modbus
    入口参数：data: 数据帧数据
    函数返回：crc: 校验和
    功能描述：计算校验和
    调用方法：将要包装的真实数据传入
    """
    def crc16_modbus(self, data: bytes) -> int:
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                lsb = crc & 0x0001
                crc >>= 1
                if lsb:
                    crc ^= 0xA001
                crc &= 0xFFFF  # 每次循环后强制截断为16位
        return crc
    
