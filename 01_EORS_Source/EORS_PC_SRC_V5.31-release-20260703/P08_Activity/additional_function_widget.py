# 导入QT模块
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QWidget

# 导入工程模块
from P07_View.Qt_Designer_ui_py.Ui_AdditionalFunctionWidget import Ui_AdditionFunctionWidget
from P06_Utils.services_bus.serial_port_manager import SerialPortManager
from P06_Utils.services_bus.services_bus import service_bus, ServiceID
from P06_Utils.services_bus.ui_manager import UIManager


# 导入其他模块
from threading import Thread
from pathlib import Path
import os


class AdditionalFunctionWidget(Ui_AdditionFunctionWidget):
    def __init__(self):
        super().__init__()

        #====================================添加变量====================================#
        self.resize_height = 150
        self.resize_width = 160
        self.__additional_function_widget = QWidget()

        self.ui_manager: UIManager = service_bus.get_service(service_id=ServiceID.UI_MANAGER)
        self.serial_port_manager: SerialPortManager = service_bus.get_service(service_id=ServiceID.SERIAL_PORT_MANAGER)
        
        #====================================设置UI====================================#
        self.setupUi(self.__additional_function_widget)
        self.sendImageProgressBar.setValue(0) #发送图片进度条和重塑数据集进度条

        #====================================添加槽函数====================================#
        self.selectDatasetButton.clicked.connect(self.btnSelectDatasetclicked)# 连接选择数据集按钮的点击信号到选择数据集的槽函数
        self.resizeDatasetButton.clicked.connect(self.btnResizeDatasetclicked) # 连接调整数据集按钮的点击信号到调整数据集的槽函数


    def get_widget(self):
        return self.__additional_function_widget

    def btnSelectDatasetclicked(self):
        """
        处理"选择数据集"按钮点击事件，打开文件夹选择对话框并设置数据集路径。
        
        功能描述：
        1. 弹出系统文件夹选择对话框，让用户选择数据集所在的目录
        2. 验证用户是否确实选择了路径（防止取消操作）
        3. 根据选择结果更新界面状态和应用程序数据
        """
        self.dataset_path = QFileDialog.getExistingDirectory(self.__additional_function_widget, "选择文件夹", "C://", )

        if self.dataset_path == "":
            self.ui_manager.show_message_box("警告", "未选择数据集", "warning")
            return
        self.importDatasetPathLabel.setText("数据集路径：" + self.dataset_path)   
        self.ui_manager.show_status_message("选择数据集路径：" + self.dataset_path)

    def btnResizeDatasetclicked(self):
        """
        处理数据集缩放按钮点击事件。
        
        参数:
            app: 应用程序实例，用于消息提示
            
        功能:
            - 检查数据集路径有效性
            - 自动识别rawdata目录
            - 创建输出目录并启动处理线程
        """
        # 检查数据集路径是否存在
        if not os.path.exists(self.dataset_path):
            self.ui_manager.show_message_box("警告", "数据集路径不存在", "warning")
            return
        
        # 识别数据源和输出路径
        parent_dir = os.path.dirname(self.dataset_path)
        if 'rawdata' in os.path.basename(self.dataset_path).lower():
            target_path = os.path.join(parent_dir, "data")
            raw_data_path = self.dataset_path
        else:
            found = False
            for item in os.listdir(self.dataset_path):
                item_path = os.path.join(self.dataset_path, item)
                if os.path.isdir(item_path) and item.lower() == 'rawdata':
                    raw_data_path = item_path
                    found = True
                    break
            if not found:
                self.ui_manager.show_message_box("警告", "数据集路径下未找到rawdata文件夹", "warning")
                return
            target_path = os.path.join(self.dataset_path, "data")
        
        # 启动处理线程
        t = Thread(target=self.process_dataset, args=(raw_data_path, target_path, (self.resize_width, self.resize_height)))
        t.start()

    """
    函数名称：resize_with_aspect_ratio
    入口参数：image_path: 图片路径，target_size: 目标尺寸
    函数返回：result: 缩放后的图像
    功能描述：根据传入的参数， 缩放图像以保持原始宽高比
    调用方法：控件cmbBaudRate选择改变后触发
    """
    def resize_with_aspect_ratio(self, image_path, target_size=(160, 150)):
        # 加载原始图像
        original = QImage(image_path)
        if original.isNull():
            raise ValueError("无法加载图像文件")

        # 计算缩放比例
        target_width, target_height = target_size
        original_width = original.width()
        original_height = original.height()
        # print(f"target_size type: {type(target_size)}, value: {target_size}")
        # 计算保持比例的缩放尺寸
        ratio = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        # 缩放图像
        scaled = original.scaled(
            new_width, new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # 创建目标尺寸画布并填充黑色
        result = QImage(target_width, target_height, QImage.Format.Format_RGB888)
        result.fill(QColor(255, 255, 255))  # 填充黑色

        # 将缩放后的图像居中绘制
        painter = QPainter(result)
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        painter.drawImage(x, y, scaled)
        painter.end()

        return result

    """
    函数名称：process_dataset
    入口参数：input_dir: 输入目录，output_dir: 输出目录，target_size: 目标尺寸
    函数返回：无
    功能描述：处理数据集，将输入目录中的图像缩放到目标尺寸，并保存到输出目录
    调用方法：不直接调用
    """
    def process_dataset(self, input_dir, output_dir, target_size=(160, 150)):
        """
        改进版：支持处理包含多层子目录的数据集，并添加进度统计
        """

        # 创建输出根目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        valid_suffixes = {'.jpg', '.jpeg', '.png', '.bmp'}

        # 先统计总文件数
        total_files = 0
        for root, _, files in os.walk(input_dir):
            for file in files:
                if Path(file).suffix.lower() in valid_suffixes:
                    total_files += 1

        # 初始化进度计数器
        processed_files = 0

        for root, dirs, files in os.walk(input_dir):
            # 计算相对于输入目录的相对路径
            rel_path = os.path.relpath(root, input_dir)

            # 处理根目录的特殊情况（rel_path 会是 "."）
            if rel_path == ".":
                output_subdir = output_dir
            else:
                output_subdir = os.path.join(output_dir, rel_path)

            # 创建输出子目录（自动创建所有父目录）
            Path(output_subdir).mkdir(parents=True, exist_ok=True)

            for file in files:
                if Path(file).suffix.lower() in valid_suffixes:
                    input_path = os.path.join(root, file)
                    output_path = os.path.join(output_subdir, file)
                    self.process_single_image(input_path, output_path, target_size)

                    # 更新进度
                    processed_files += 1
                    progress = int((processed_files / total_files) * 100)
                    self.sendImageProgressBar.setValue(progress)
        self.ui_manager.show_message_box("提示", "数据集标准化完成", "information")
        self.ui_manager.show_status_message("数据集标准化完成")

    def process_single_image(self, input_path, output_path, target_size):
        """
        处理单张图像：缩放至目标尺寸并保存为PNG格式。
        
        参数:
            input_path (str): 输入图像路径
            output_path (str): 输出图像路径
            target_size (tuple): 目标尺寸(宽, 高)
            
        异常:
            处理失败时弹出警告消息并打印错误信息
        """
        try:
            # 使用之前定义的缩放函数
            processed_img = self.resize_with_aspect_ratio(input_path, target_size)

            # 保存为PNG格式（无损压缩）
            processed_img.save(output_path, "PNG", 100)
            # print(f"已处理: {input_path} -> {output_path}")
        except Exception as e:
            self.ui_manager.show_message_box("警告", f"处理失败 {input_path}: {str(e)}", "warning")
            print(f"处理失败 {input_path}: {str(e)}")
        
        
