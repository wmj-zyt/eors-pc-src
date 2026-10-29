# 导入QT模块
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox, QLabel
from PySide6.QtCore import QTimer, Qt, QByteArray
from PySide6.QtGui import QPixmap, QImage

from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

# 导入工程模块
from P06_Utils.services_bus.serial_port_manager import SerialPortManager
from P06_Utils.services_bus.config_manager import ConfigManager
from P07_View.Qt_Designer_ui_py.Ui_DataAcuisitionWidget import Ui_DataAcuisitionWidget
from P03_Components.customVideoPlayer import VideoPlayer
from P03_Components.customGridWidget import CustomGridLayout
from P06_Utils.services_bus.services_bus import service_bus, ServiceID
from P06_Utils.services_bus.ui_manager import UIManager

# 导入其他所需模块
import numpy as np
from datetime import datetime
import os
from functools import partial
import cv2
from PIL import Image

import struct
from keras.models import load_model
import h5py
"""
类名：DataAcuisitionWidget
基类：Ui_DataAcuisitionWidget
功能：数据采集页面
"""
class DataAcuisitionWidget(Ui_DataAcuisitionWidget):
    def __init__(self):
        super().__init__()

        #====================================添加变量====================================#
        # 创建界面对象
        self.__data_acuisition_widget = QWidget()
        # 获取配置服务
        self.config_manager: ConfigManager = service_bus.get_service(ServiceID.CONFIG_MANAGER)
        # 采集图像大小
        self.img_width = self.config_manager.get("globalSettings.imageSize.width")
        self.img_height = self.config_manager.get("globalSettings.imageSize.height")
        # 初始化采集图片名称列表
        self.image_path = []
        # 获取采集图像的宽度和高度
        colletImgWidth = self.img_width
        colletImgHeight = self.img_height
        # 创建另一个 QTimer 实例，关联到app应用程序对象
        self.timer_img = QTimer()
        # 初始化一个bytearray对象用于存储图片像素
        self.pixels = bytearray()
        # 初始化图片采集过程状态为False
        self.recording = False
        # 初始化当前可用串口列表为空
        self.currentSerials = []
        # 初始化正在采集图片状态为False
        self.isCollecting = False 
        # 初始化图片保存路径为空
        self.ImgSavePath = ""
        # 初始化串口列表
        self.serial_ports = []
        # 创建自定义的网格布局
        self.showImgGridWiget = CustomGridLayout(colletImgWidth, colletImgHeight)
        # 设置网格布局对象名称
        self.showImgGridWiget.setObjectName(u"gridLayout")
        # 获取UI管理器，用于交互主线程控件
        self.ui_manager: UIManager = service_bus.get_service(service_id=ServiceID.UI_MANAGER)
        # 获取串口管理器，用于和串口交互
        self.serial_port_manager: SerialPortManager = service_bus.get_service(service_id=ServiceID.SERIAL_PORT_MANAGER)
        # 打开的串口号
        self.serial_no = ""

        self.serial = QSerialPort()
        self.serial.readyRead.connect(self.on_ready_read)

        self.scan_timer = QTimer()
        self.scan_timer.setSingleShot(True)
        self.scan_timer.timeout.connect(self.on_scan_timeout)

        self.scan_ports = []
        self.scan_index = -1
        self.scan_buffer = bytearray()
        self.found_port = None

        # 你要发送的探测命令、期望匹配的回包（按你的协议改）
        self.probe_data = b"$!are you user?\r\n"
        self.expected_keyword1 = b"yes,I am uart Test"   # 例如回包里包含 OK 就算命中
        self.expected_keyword2 = b"yes,I am img collect"   # 例如回包里包含 OK 就算命中

        #====================================设置UI====================================#
        self.setupUi(self.__data_acuisition_widget)

        # # 设置采集下一张按钮初始化状态为不可点击
        # self.collectNextImgButton.setEnabled(False)

        # 播放按钮默认禁止点击，导入视频后才可以点击
        self.playVideoButton.setEnabled(False) 
        # 设置逐帧分解视频按钮默认为不可点击
        self.decomposeVideoButton.setEnabled(False)
        # 设置删除视频按钮默认不可见
        self.deleteVideoButton.setVisible(False)
        # 将网格布局添加到水平布局中
        self.showImgHorizontalLayout.addWidget(self.showImgGridWiget)
        # 设置图片管理区滚动条自动滚动到最底部
        self.savedImgsArea.verticalScrollBar().rangeChanged.connect(
            lambda: self.savedImgsArea.verticalScrollBar().setValue(
                self.savedImgsArea.verticalScrollBar().maximum()
            )
        )
        #关闭图像发送相关的
        self.selectPicBtn.setEnabled(False)
        self.sendPicBtn.setEnabled(False)
        #====================================添加槽函数====================================#
        # 连接按钮的点击信号到处理函数
        self.serialButton.clicked.connect(self.openCloseSerial)
        

        # 将超时信号(timeout)连接到lambda表达式，该表达式调用self.showImgState(app)函数，显示当前图片管理器图片数量
        self.timer_img.timeout.connect(self.showImgState)
        # 启动计时器，以 1000 毫秒(1秒)的间隔触发一次超时事件
        self.timer_img.start(1000)
        # 连接采集下一张图像按钮的点击信号到处理函数
        # self.collectNextImgButton.clicked.connect(self.colloectContinute)


        # 连接全选/取消全选图像复选框的状态改变事件，触发时调用 self.selectAllImg(app) 函数
        self.selectAllImgCheckBox.stateChanged.connect(self.selectAllImg)
        # 连接批量删除按钮的点击信号到处理函数
        self.batchDeleteButton.clicked.connect(self.deleteBatchImg)
        # 连接导入视频按钮的点击信号到处理函数
        self.loadVideoButton.clicked.connect(self.loadVideo)
        # 创建视频播放器
        self.player = VideoPlayer(self.sliderEvent, self.durationEvent, self.videoFrame)
        # 将视频播放器添加到垂直布局中
        self.videoHorizontalLayout.addWidget(self.player)
        # 连接播放视频按钮的点击信号到处理函数
        self.playVideoButton.clicked.connect(lambda: self.player.play_video(self.playVideoButton))
        # 为播放视频按钮安装事件过滤器
        self.playVideoButton.installEventFilter(self.player)
        # 连接视频进度条的滑动事件，触发时调用 app.player.set_position 函数
        self.videoSlider.sliderMoved.connect(self.player.set_position)
        # 连接逐帧分解视频按钮的点击事件，触发时调用 self.decomposeVideo(app) 函数
        self.decomposeVideoButton.clicked.connect(self.decomposeVideo)
        # 连接批量保存图片按钮的点击事件，触发时调用 self.saveBatchImg(app) 函数
        self.batchSaveButton.clicked.connect(self.saveBatchImg)
        # 连接清空图像管理区域按钮的点击事件，触发时调用 self.clearGridWidget(app) 函数
        self.clearImgManageAreaButton.clicked.connect(self.clearGridWidget)

        # 连接清空采集图像按钮的点击事件，清空采集图像
        # self.delCollectedImgButton.clicked.connect(self.collectImageLabel.clear)
        # 为清空采集图像按钮安装事件过滤器
        # self.delCollectedImgButton.installEventFilter(self)
        # 连接清空串口数据按钮的点击事件，清空串口接收数据
        self.clearSerialDataButton.clicked.connect(self.clearAllData)
        # 连接删除视频按钮的点击事件，清空视频
        self.deleteVideoButton.clicked.connect(self.deleteVideo)
        # 连接刷新串口列表的槽函数
        self.serial_port_manager.add_ports_updated_handler(self.update_ports)



        ####################################WTX添加####################################
        self.image_path = ""
        self.model_list = []
        # 初始化图片名称与BMP文件路径的映射字典
        self.image_bmp_paths = {}

        # 连接导入图像按钮的点击信号到导入图像的槽函数
        self.selectPicBtn.clicked.connect(self.btnSelectImageclicked)
        # 连接发送图像按钮的点击信号到发送图像的槽函数
        self.sendPicBtn.clicked.connect(self.btnSendDataclicked)
        self.ui_manager.update_model_list.connect(self.refreshModelList)

    # 定义槽函数
    def clearAllData(self):
        # 清空串口数据
        self.serialData.clear()
        # 清空图片标签
        self.collectImageLabel.clear() 
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
            self.selectModelComboBox.clear()
            # 获取模型文件夹中的模型列表，并按创建时间降序排序
            # 将模型列表添加到下拉框中
            self.selectModelComboBox.addItems(model_list)

    """
    函数名称：btnSendDataclicked
    入口参数：无
    函数返回：无
    功能描述：通过串口发送图像数据给下位机
    调用方法：不直接调用
    """
    def btnSendDataclicked(self):
        try:
            # app.statusBar.setText(u"状态：开始发送数据")
            self.ui_manager.show_status_message(u"状态：开始发送数据")
            
            # 检查是否有选择图像文件路径
            if not hasattr(self, 'image_path') or not self.image_path:
                self.ui_manager.show_message_box("警告", "请先选择图像文件！","warning")
                # app.ms.popMessageBox.emit("warning", "警告", "请先选择图像文件！")
                return
            
            # 使用与预测完全相同的图像处理流程
            # 直接使用QImage读取原始图像文件
            original_image = QImage(self.image_path)
            if original_image.isNull():
                self.ui_manager.show_message_box("警告", "图像文件读取失败！","warning")
                return
                
            # 转换为RGB888格式
            qimage = original_image.convertToFormat(QImage.Format.Format_RGB888)
            
            # 获取需要调整的图像尺寸（使用配置文件中的尺寸）
            # resizeHeight = self..settings['ImageSize']['Height']
            # resizeWidth = app.settings['ImageSize']['Width']
            resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
            resizeWidth = self.config_manager.get("globalSettings.imageSize.width")


            
            # 缩放图像到目标尺寸（与预测时相同的方式）
            qimage = qimage.scaled(resizeWidth, resizeHeight, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # 获取图像数据
            rgb888Data = qimage.constBits()
            np_img = np.frombuffer(rgb888Data, dtype=np.uint8).reshape((resizeHeight, resizeWidth, 3))
            

            # 直接使用RGB888数据，不再转换为RGB565
            pixels = np_img.astype(np.uint8)

            # 保存处理后的图像数据供下位机发送使用
            self.processed_image_data = pixels.copy()
            # 按照每一行每一列 RGB 三色的格式添加数据
            byte_stream = bytearray()
            
            # 调试信息：对比发送数据和预测数据
            print(f"[调试] 发送数据统计: shape={pixels.shape}, min={pixels.min()}, max={pixels.max()}, mean={pixels.mean():.6f}")
            print(f"[调试] 发送数据前10个像素: {pixels.flatten()[:10]}")
            
            # 对比预测数据和发送数据是否一致
            if hasattr(self, 'processed_image_data') and self.processed_image_data is not None:
                data_identical = np.array_equal(pixels, self.processed_image_data)
                print(f"[调试] 预测数据和发送数据是否一致: {data_identical}")
                if not data_identical:
                    diff = np.abs(pixels.astype(int) - self.processed_image_data.astype(int))
                    print(f"[调试] 数据差异统计: maPdiff={diff.max()}, mean_diff={diff.mean():.6f}")
            else:
                print("[调试] 警告：未找到预测数据，无法对比")
            for i in range(resizeHeight):
                for j in range(resizeWidth):
                    r = int(pixels[i][j][0])
                    g = int(pixels[i][j][1])
                    b = int(pixels[i][j][2])
                    byte_stream.append(r)
                    byte_stream.append(g)
                    byte_stream.append(b)

            byte_stream = self._build_packet(byte_stream)
            # 使用串口发送数据
            # self.serial.write(byte_stream)
            # PortName = self.serialComboBox.currentText()
            # self.serial_port_manager.send_data(PortName, byte_stream)
            self.serial.write(byte_stream)
            self.ui_manager.show_status_message(u"状态：发送数据结束（使用与预测相同的处理流程）")
        except Exception as e:
            # app.ms.popMessageBox.emit("warning", "警告", "发送失败！")
            self.ui_manager.show_message_box("警告", "发送失败！","warning")
            self.ui_manager.show_status_message(u"状态：发送数据失败-" + str(e))


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
    

    """
    函数名称：btnSelectImageclicked
    入口参数：无
    函数返回：无
    功能描述：加载选中图片
    调用方法：不直接调用
    """
    def btnSelectImageclicked(self):
        try:
            self.ui_manager.show_status_message(u"状态：选择图片")
            self.image_path = QFileDialog.getOpenFileName(self.__data_acuisition_widget, "选择图片", "", "Image Files(*.jpg *.gif *.png *.bmp *.jpeg *.tif *.tiff)")[0]
            #self.image_path = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files(*.jpg *.gif *.png *.bmp *.jpeg *.tif *.tiff)")[0]
            if(self.image_path):
                self.ui_manager.show_status_message(u"状态：图片" + self.image_path +"加载成功")

            
        except Exception as e:
            self.ui_manager.show_status_message(u"状态：选择图片失败" + str(e))
            # app.ms.popMessageBox.emit("warning", "警告", str(e))
            self.ui_manager.show_message_box("警告", str(e),"warning")

    def get_widget(self):
        return self.__data_acuisition_widget

    """
    函数名称：update_ports
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：# 更新串口列表
    """
    def update_ports(self, ports):
        if ports != self.serial_ports:
            self.serial_ports = ports
            # # 清空下拉框中的选项
            # self.serialComboBox.clear()
            # # 将串口列表添加到下拉框中
            # self.serialComboBox.addItems(ports)


    # """
    # 函数名称：openCloseSerial
    # 参数说明：app:应用程序对象 
    # 函数返回：无
    # 功能概要：打开/关闭串口
    # """
    # def openCloseSerial(self):
    #     self.pixels.clear()  
    #     # 获取当前选择的串口
    #     serialNo = self.serialComboBox.currentText()
    #     # 如果串口按钮文本为"打开串口"
    #     if self.serialButton.text() ==u"打开串口":
    #         try: 
    #             # 尝试打开串口，返回打开状态和消息
    #             # 尝试创建串口实例
    #             self.serial_port_manager.create_port(serialNo)
    #             is_open = self.serial_port_manager.connect_port(serialNo)

    #             # 如果打开失败
    #             if not is_open:
    #                 # 在状态栏显示打开失败消息
    #                 self.ui_manager.show_message_box("错误", "打开串口失败", "critical")
    #                 self.ui_manager.show_status_message(f"串口{serialNo}打开失败")
    #                 return
    #             # 如果打开成功，修改串口按钮文本为"关闭串口"
    #             self.serialButton.setText("关闭串口")
    #             # 在状态栏显示串口已打开消息
    #             self.ui_manager.show_status_message(f"串口{serialNo}已打开")

    #             self.serial_no = serialNo

    #             img_height = self.config_manager.get("globalSettings.imageSize.height")
    #             img_width = self.config_manager.get("globalSettings.imageSize.width")

    #             # 连接串口的数据接收信号到处理函数
    #             # self.serial_port_manager.register_data_handler(self.serial_no, self.SCIUpdateRevtxtbox)
    #             self.serial_port_manager.register_data_handler(self.serial_no, lambda data: self.SCIUpdateRevtxtbox(data, img_height, img_width))

    #         except Exception as e:
    #             # 如果打开过程中发生异常，在状态栏显示串口打开失败消息
    #             self.ui_manager.show_status_message(str(e))
    #     else:
    #         if self.isCollecting:
    #             self.ui_manager.show_message_box("警告", "请先停止采集！", "warning")
    #             return
    #         # 如果串口按钮文本为"关闭串口"，修改按钮文本为"打开串口"
    #         self.serialButton.setText("打开串口")
    #         # 关闭串口连接
    #         is_closed = self.serial_port_manager.disconnect_port(serialNo)
    #         if is_closed:
    #             # 在状态栏显示串口关闭消息
    #             self.ui_manager.show_status_message(f"串口{serialNo}已关闭")
    #             self.serial_port_manager.unregister_data_handler(self.serial_no, self.SCIUpdateRevtxtbox)
    #             self.serial_no = ""
    #         else:
    #             self.ui_manager.show_status_message(f"串口{serialNo}关闭失败")
    
    # def openCloseSerial(self):
    #     if getattr(self, "handshake_ok", False):
    #         self.handshake_ok= False
    #         return
    #     # 🔴 第一步：判断串口当前是否已打开
    #     if self.serial.isOpen():
    #         # 串口已打开 → 执行关闭逻辑
    #         self.serial.close()
    #         self.ui_manager.show_status_message("串口已关闭")
    #         self.uartStateLabel.setText(f"GEC:{self.found_port}已关闭")
    #         self.serialButton.setText("连接GEC")
    #         return
        
    #     #关闭图像发送相关按钮
    #     self.selectPicBtn.setEnabled(False)
    #     self.sendPicBtn.setEnabled(False)
    #     print(self.serial_ports)  # ["COM3","COM8", ...]

    #     if not self.serial_ports:
    #         self.ui_manager.show_status_message("没有可用串口")
    #         self.uartStateLabel.setText("没有可用串口")
    #         return
        
    #     self.serial.readyRead.connect(self.on_ready_read)

    #     self.scan_ports = list(self.serial_ports)
    #     self.scan_index = -1
    #     self.scan_buffer = bytearray()
    #     self.found_port = None

    #     self.ui_manager.show_status_message("开始扫描串口...")
    #     self.scan_next_port()

    def openCloseSerial(self):
        # 1) 如果已经打开，就关闭（这是用户点击“断开连接”的预期行为）
        if self.serial.isOpen():
            self.scan_timer.stop() if hasattr(self, "scan_timer") else None

            try:
                self.serial.readyRead.disconnect()  # 断开所有 readyRead 槽，防止残留
            except Exception:
                pass

            self.serial.close()
            self.ui_manager.show_status_message("串口已关闭")
            self.uartStateLabel.setText(f"GEC:{getattr(self, 'found_port', '')}已关闭")
            self.serialButton.setText("连接GEC")

            # 清状态
            self.handshake_ok = False
            if hasattr(self, "pixels"):
                self.pixels.clear()
            if hasattr(self, "scan_buffer"):
                self.scan_buffer.clear()
            #失能图片相关按钮
            self.selectPicBtn.setEnabled(False)
            self.sendPicBtn.setEnabled(False)
            return

        # 2) 走扫描打开
        self.handshake_ok = False

        self.selectPicBtn.setEnabled(False)
        self.sendPicBtn.setEnabled(False)

        if not self.serial_ports:
            self.ui_manager.show_status_message("没有可用串口")
            self.uartStateLabel.setText("没有可用串口")
            return

        # ✅ 防止重复 connect
        try:
            self.serial.readyRead.disconnect()
        except Exception:
            pass
        self.serial.readyRead.connect(self.on_ready_read)

        self.scan_ports = list(self.serial_ports)
        self.scan_index = -1
        self.scan_buffer = bytearray()
        self.found_port = None

        self.ui_manager.show_status_message("开始扫描串口...")
        self.scan_next_port()

    def scan_next_port(self):
        # 先停掉上一个串口
        if self.serial.isOpen():
            self.serial.close()

        self.scan_index += 1
        self.scan_buffer.clear()

        if self.scan_index >= len(self.scan_ports):
            self.ui_manager.show_status_message("扫描完成：未找到匹配设备")
            self.uartStateLabel.setText("扫描完成：未找到匹配设备")
            return

        port_name = self.scan_ports[self.scan_index]
        self.ui_manager.show_status_message(f"正在尝试 {port_name} ...")

        # 配置串口参数（按你设备需要改）
        self.serial.setPortName(port_name)
        self.serial.setBaudRate(115200)
        self.serial.setDataBits(QSerialPort.Data8)
        self.serial.setParity(QSerialPort.NoParity)
        self.serial.setStopBits(QSerialPort.OneStop)
        self.serial.setFlowControl(QSerialPort.NoFlowControl)

        if not self.serial.open(QSerialPort.ReadWrite):
            # 打不开就下一个
            self.ui_manager.show_status_message(f"{port_name} 打开失败，尝试下一个")
            self.scan_next_port()
            return

        # 打开成功：发送探测数据
        self.serial.write(self.probe_data)

        # 启动超时计时（比如 300ms~1000ms 看设备响应速度）
        self.scan_timer.start(2000)
    # def on_ready_read(self):
    #     data = self.serial.readAll().data()
    #     if not data:
    #         return

    #     self.scan_buffer.extend(data)

    #     # 任意一个关键字命中就算找到
    #     hit1 = self.expected_keyword1 in self.scan_buffer
    #     hit2 = self.expected_keyword2 in self.scan_buffer

    #     if hit1 or hit2:
    #         self.scan_timer.stop()
    #         self.found_port = self.serial.portName()
    #         self.serial_no = self.found_port

    #         img_height = self.config_manager.get("globalSettings.imageSize.height")
    #         img_width = self.config_manager.get("globalSettings.imageSize.width")
    #         self.serialButton.setText("断开连接")
    #         # 可选：记录是哪一种
    #         if hit1:
    #             self.found_type = "uart_test"
    #             self.selectPicBtn.setEnabled(True)
    #             self.sendPicBtn.setEnabled(True)
    #             self.ui_manager.show_status_message(f"已找到设备串口：{self.found_port} ({self.found_type})")
    #             self.uartStateLabel.setText(f"GEC:{self.found_port}连接成功")
    #         elif hit2:
    #             self.found_type = "img_collect"
    #             self.selectPicBtn.setEnabled(False)
    #             self.sendPicBtn.setEnabled(False)
    #             self.ui_manager.show_status_message(f"已找到设备串口：{self.found_port} ({self.found_type})")
    #             self.uartStateLabel.setText(f"GEC:{self.found_port}连接成功")
    #         else:
    #             self.uartStateLabel.setText(f"匹配失败")

    #         # ✅ 切换时建议清空缓冲，避免把握手残留当成图像帧的一部分
    #         if hasattr(self, "pixels"):
    #             self.pixels.clear()

    #         # 扫描缓冲也可以清
    #         self.scan_buffer.clear()
    #         # ✅ 关键：切换 readyRead 回调
    #         try:
    #             self.serial.readyRead.disconnect(self.on_ready_read)
    #             print("切换成功")
    #         except Exception:
    #             print("切换失败")
    #             pass
    #         self.serial.readyRead.connect(self.on_ready_read_img)


    #         return
        
    #     else:
    #         self.uartStateLabel.setText(f"握手失败")


    def on_ready_read(self):
        # 如果已经握手成功，就不要再跑扫描逻辑，避免覆盖UI
        if getattr(self, "handshake_ok", False):
            return

        data = bytes(self.serial.readAll())
        if not data:
            return

        self.scan_buffer.extend(data)

        hit1 = self.expected_keyword1 in self.scan_buffer
        hit2 = self.expected_keyword2 in self.scan_buffer
        hit3 = len(data)>0x40
        if hit1 or hit2 or hit3:
            self.handshake_ok = True   # ✅ 关键：锁定状态，后续不再走失败分支

            self.scan_timer.stop()
            self.found_port = self.serial.portName()
            self.serial_no = self.found_port

            self.serialButton.setText("断开连接")

            if hit1:
                self.found_type = "uart_test"
                self.selectPicBtn.setEnabled(True)
                self.sendPicBtn.setEnabled(True)
            elif hit2 :
                self.found_type = "img_collect"
                self.selectPicBtn.setEnabled(False)
                self.sendPicBtn.setEnabled(False)
            else:
                self.found_type = "img_collect"
                self.selectPicBtn.setEnabled(False)
                self.sendPicBtn.setEnabled(False) 
                print(f"hit3 {len(data)}") 

            self.ui_manager.show_status_message(f"已找到设备串口：{self.found_port} ({self.found_type})")
            self.uartStateLabel.setText(f"GEC:{self.found_port}连接成功")

            # 清缓冲，避免握手残留污染图像解析
            if hasattr(self, "pixels"):
                self.pixels.clear()
            self.scan_buffer.clear()

            # 切换 readyRead 回调
            try:
                self.serial.readyRead.disconnect(self.on_ready_read)
            except Exception:
                pass
            self.serial.readyRead.connect(self.on_ready_read_img)

            return

        # ❌ 不要在这里每次都写“握手失败”
        # 因为握手回包可能分段，未命中只是“还没收全”
        # 握手失败应该放在 scan_timer 超时里处理

            
    def on_scan_timeout(self):
        # 超时说明当前口没匹配到
        port_name = self.serial.portName()
        self.ui_manager.show_status_message(f"{port_name} 无响应/不匹配，尝试下一个")
        self.scan_next_port()

    def on_ready_read_img(self):
        data = self.serial.readAll()   # QByteArray
        if data.isEmpty():
            return
        self.SCIUpdateRevtxtbox(data, self.img_height, self.img_width)

    """
    函数名称：SCIUpdateRevtxtbox
    参数说明：data:串口接收的数据  img_height:采集图片高度  img_width:采集图片宽度 
    函数返回：无
    功能概要：串口接收数据信号的处理函数，主要用于从串口接收 ​​RGB565 格式的图像数据​​，并转换为 ​​RGB888 格式​​ 的图像进行显示
    """
    def SCIUpdateRevtxtbox(self, data: QByteArray, img_height, img_width):
        """
        解析新帧结构：[0x55 0xAA][长度4字节][RGB888数据][CRC16]
        注意：帧长度字段已从2字节扩展为4字节
        """
        # 1. 转换为原始字节
        try:
            # 使用QByteArray的正确方法获取字节数据
            if hasattr(data, 'data'):
                raw_data = data.data()
            else:
                # 使用QByteArray的其他方法
                try:
                    # 尝试使用QByteArray的正确方法
                    buffer = data.data() if hasattr(data, 'data') else None
                    if buffer:
                        raw_data = buffer
                    else:
                        # 最后使用默认方法
                        raw_data = data
                except:
                    raw_data = data
        except:
            # 如果上述方法失败，使用默认方法
            raw_data = data
        # 确保raw_data是bytes类型
        if not isinstance(raw_data, bytes):
            try:
                # 使用QByteArray的正确转换方法
                # 对于QByteArray，我们需要特殊处理
                if hasattr(raw_data, 'size') and hasattr(raw_data, 'at'):
                    # 逐字节读取QByteArray
                    byte_list = []
                    for i in range(raw_data.size()):
                        byte_list.append(raw_data.at(i))
                    raw_data = bytes(byte_list)
                else:
                    # 尝试其他转换方法
                    raw_data = raw_data.data() if hasattr(raw_data, 'data') else b""
            except:
                # 如果所有方法都失败，使用默认值
                raw_data = b""
        self.pixels.extend(raw_data)
        
        # 2. 调试信息
        display_data = ''.join([chr(b) if 32 <= b < 127 else '.' for b in raw_data[:50]])
        # app.ms.showStatus.emit(display_data, app.serialData)
        self.serialData.setText(display_data)
        # self.ui_manager.show_status_message("图片保留在右侧图片管理区")

        # 3. 查找帧头
        while True:
            start_idx = self.pixels.find(b'\x55\xAA')
            if start_idx == -1:
                return  # 未找到完整帧头
            
            # 4. 检查是否收到完整帧头+长度
            if len(self.pixels) < start_idx + 6:  # 帧头2 + 长度4
                return  # 数据不足
                
            # 5. 解析32位长度（大端序）
            data_len = (self.pixels[start_idx + 2] << 24) | \
                    (self.pixels[start_idx + 3] << 16) | \
                    (self.pixels[start_idx + 4] << 8) | \
                    self.pixels[start_idx + 5]
            
            # 6. 检查完整帧是否接收完毕
            frame_size = 6 + data_len + 2  # 帧头2 + 长度4 + 数据 + CRC2
            if len(self.pixels) < start_idx + frame_size:
                return  # 数据不完整
                
            # 7. 提取完整帧
            frame = self.pixels[start_idx : start_idx + frame_size]
            self.pixels = self.pixels[start_idx + frame_size : ]  # 移除已处理数据
            
            # 8. 分解帧数据
            header = frame[:2]        # 0x55 0xAA
            length = frame[2:6]       # 4字节长度
            image_data = frame[6:-2]  # RGB565数据
            received_crc = frame[-2:] # CRC校验
            
            # 9. CRC校验（仅对数据部分）
            calculated_crc = self.crc16(image_data)
            if int.from_bytes(received_crc, 'big') != calculated_crc:
                # app.ms.showStatus.emit(f"CRC错误: {hex(int.from_bytes(received_crc, 'big'))} != {hex(calculated_crc)}", app.statusBar)
                self.ui_manager.show_status_message(f"CRC错误: {hex(int.from_bytes(received_crc, 'big'))} != {hex(calculated_crc)}")
                self.pixels.clear()
                continue  # 继续处理下一帧
                
            try:
                # 10. 直接解析RGB888数据（不再需要RGB565转换）
                # 计算期望的数据长度（RGB888每个像素3字节）
                expected_size = img_height * img_width * 3
                if len(image_data) != expected_size:
                    raise ValueError(f"数据长度不符: 需要{expected_size}字节, 收到{len(image_data)}")
                 # 直接解析为RGB888格式
                 #chw
                rgb888 = np.frombuffer(image_data, dtype=np.uint8).reshape(3,img_height, img_width)
                #chw
                # 11. 转换为下位机期望的CHW格式
                rgb888 = np.transpose(rgb888, (1, 2, 0))  # chw -> hwc
                # 11. 直接无损保存为BMP
                bmp_path = self.save_as_bmp_lossless(rgb888)
                
                # 调试信息
                print(f"[调试] 接收RGB888数据: shape={rgb888.shape}, min={rgb888.min()}, max={rgb888.max()}")
                print(f"[调试] 首个像素: R={rgb888[0,0,0]}, G={rgb888[0,0,1]}, B={rgb888[0,0,2]}")
            
                # 12. 更新UI
                self.recording = False
                # app.ms.loadImage.emit(rgb888, app.collectImageLabel)
                self.showImage(rgb888, self.collectImageLabel)
                # app.ms.showStatus.emit("采集成功", app.statusBar)
                self.ui_manager.show_status_message("采集成功")
                # 使用新的方法保存图片，建立映射关系
                if bmp_path:
                    self.holdImgWithBmpPath( bmp_path)

                 # 归一化像素数据
                pixels_normalized = rgb888 * (1/255.0) 
                # 添加批次维度，从(H, W, 3)变为(1, H, W, 3)以符合模型输入要求
                inputImg = np.expand_dims(pixels_normalized, axis=0)

                # 获取选择的模型文件名
                selectedModelFile = self.selectModelComboBox.currentText()
                if not selectedModelFile:
                    # app.ms.popMessageBox.emit("warning", "警告", "还未选择模型文件")
                    return
        
                try:
                    dataset_path = self.config_manager.get("foldersPath.datasetPath")
                    #selectedModelFile = "G:/suda_MCU/EORS-20250817-/EORS-251012/EORS-251012/ABCD-StepByStep-251016/2-train/ABCD/new_data_MobileNetv2_251026-0813.keras"
                    # model = load_model(f"{dataset_path}/{selectedModelFile}", custom_objects={})
                    

                    # 打开模型文件，读取额外数据
                    with h5py.File(f"{dataset_path}/{selectedModelFile}", mode="r") as hdf:
                        infoGroup = hdf.get("additional_data")
                        category = []
                        if infoGroup is not None:
                            try:
                                # 使用异常处理来安全访问categoryLabels
                                try:
                                    # 尝试直接访问categoryLabels
                                    category_data = infoGroup['categoryLabels']
                                    # 检查category_data是否为None
                                    if category_data is not None:
                                        # 尝试转换为列表
                                        try:
                                            # 对于h5py对象，使用特殊方法读取
                                            if hasattr(category_data, '__len__') and hasattr(category_data, '__getitem__'):
                                                # 这可能是一个数组或列表
                                                category_list = []
                                                for i in range(len(category_data)):
                                                    category_list.append(category_data[i])
                                            elif hasattr(category_data, '__iter__'):
                                                # 可迭代对象
                                                category_list = list(category_data)
                                            else:
                                                # 其他情况
                                                category_list = []
                                            # 解码字节字符串
                                            category = [x.decode('utf-8') if isinstance(x, bytes) else str(x) for x in category_list]
                                        except:
                                            # 如果转换失败，设置为空列表
                                            category = []
                                except (KeyError, TypeError):
                                    # categoryLabels不存在或无法访问
                                    category = []
                            except Exception as e:
                                print(f"获取分类标签时出错: {e}")
                                category = []
                    # 加载模型
                    model = load_model(f"{dataset_path}/{selectedModelFile}", custom_objects={})
                    
                    # 创建自定义回调
                    # 进行图像预测
                    predictResult = model.predict(inputImg)
                    predictResult = predictResult.flatten().tolist()
                    print(f"predictResult is {predictResult}")

                    # 显示预测结果
                    # 显示预测结果
                    # 获取预测结果中的最大值（最高置信水平）
                    confLevel = max(predictResult)
                    # 根据最高置信水平的索引获取对应的图像类别
                    imgType = category[predictResult.index(confLevel)]
                    # app.ms.showImgPredictionResult.emit(predictResult, category, app.uart_preLeibie, app.uart_preData)
                    self.uart_preLeibie.setText(imgType)
                    self.uart_preData.setText(f'{round(confLevel*100, 2)}%')   
                    # 显示预测结果
                    # app.ms.showImgPredictionResult.emit(predictResult, category, app.predictionResult, app.confidenceLevel)
                except Exception as e:
                    # app.ms.popMessageBox.emit("critical", "错误", str(e))
                    self.ui_manager.show_message_box("错误", str(e),"critical")
                    # 捕捉异常并忽略
                    pass
                break

            except Exception as e:
                self.recording = False
                print(f"解析异常: {e}\n原始数据: {frame.hex()}")
                # app.ms.showStatus.emit(f"解析错误: {str(e)}", app.statusBar)
                self.ui_manager.show_status_message(f"解析错误: {str(e)}")



    def crc16(self, data: bytes) -> int:  # 实例方法
        """与C语言一致的CRC16实现"""
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                lsb = crc & 0x0001
                crc >>= 1
                if lsb:
                    crc ^= 0xA001
        return crc

    def save_as_bmp_lossless(self, rgb888_array):
        """无损保存为BMP格式"""
        try:
            from PIL import Image
            import os
            from datetime import datetime
            
            # 创建保存目录
            save_dir = "received_images"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 生成文件名（带时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"received_{timestamp}.bmp"
            filepath = os.path.join(save_dir, filename)
            
            # 转换为PIL图像并保存为BMP
            image = Image.fromarray(rgb888_array)
            image.save(filepath, "BMP")
            
            # 验证保存的图片与原数据是否一致
            self.verify_bmp_integrity(rgb888_array, filepath)
            
            print(f"[BMP保存] 图片已无损保存: {filepath}")
            # app.ms.showStatus.emit(f"BMP保存成功: {filename}", app.statusBar)
            self.ui_manager.show_status_message(f"BMP保存成功: {filename}")
            
            # 返回保存的文件路径
            return filepath
        except Exception as e:
            print(f"[BMP保存] 错误: {e}")
            # app.ms.showStatus.emit(f"BMP保存失败: {str(e)}", app.statusBar)
            self.ui_manager.show_status_message(f"BMP保存失败: {str(e)}")
            return None

    def verify_bmp_integrity(self, original_array, bmp_path):
        """验证BMP保存的完整性"""
        try:
            from PIL import Image
            
            # 重新加载BMP
            reloaded_image = Image.open(bmp_path)
            reloaded_array = np.array(reloaded_image)
            
            # 比较差异
            diff = np.abs(original_array.astype(int) - reloaded_array.astype(int))
            maPdiff = diff.max()
            mean_diff = diff.mean()
            
            if maPdiff == 0:
                print(f"[完整性验证] ✅ BMP保存完全无损")
            else:
                print(f"[完整性验证] ⚠️ BMP存在差异: maPdiff={maPdiff}, mean_diff={mean_diff:.6f}")
                print(f"[完整性验证] 差异像素数: {np.sum(diff > 0)}/{diff.size}")
                
        except Exception as e:
            print(f"[完整性验证] 错误: {e}")
    """
    函数名称：holdImgWithBmpPath
    参数说明：app:应用程序对象  bmp_path:原始BMP文件路径
    函数返回：无
    功能概要：保留拍摄的图片到图片管理区，并建立图片名称与BMP文件路径的映射关系
    """
    def holdImgWithBmpPath(self, bmp_path):
        # 获取当前显示的图片
        # pixmap = app.collectImageLabel.pixmap() #获取当前显示的 QPixmap
        pixmap = self.collectImageLabel.pixmap()
        if pixmap:
            # 获取当前时间作为图片名称
            saveTime = datetime.now()
            imageName = saveTime.strftime(r"%Y%m%d_%H%M%S")
            # 如果图片名称不在已保存的图片路径中，则添加图片到右侧图片管理区
            if imageName not in self.image_path:
                self.showImgGridWiget.add_image(imageName, pixmap)
                # app.ms.addImageLabel.emit(imageName, pixmap, app.gridLayout)
                # 建立图片名称与BMP文件路径的映射关系
                self.image_bmp_paths[imageName] = bmp_path
            
                # app.collectImageLabel.clear()
                # 在状态栏显示图片保留在右侧图片管理区消息
                # app.ms.showStatus.emit("图片保留在右侧图片管理区", app.statusBar)
                self.ui_manager.show_status_message("图片保留在右侧图片管理区")
        else:
            # 如果没有图片可以保留，弹出警告消息框
            # app.ms.popMessageBox.emit("warning", "警告", "没有图片可以保留")
            self.ui_manager.show_message_box("警告", "没有图片可以保留", "warning")


    # """
    # 函数名称：colloectContinute
    # 参数说明：app:应用程序对象 
    # 函数返回：无
    # 功能概要：采集下一张按钮点击事件
    # """
    # def colloectContinute(self):
    #     # 如果当前不在采集状态，弹出警告消息框
    #     if self.isCollecting is False:
    #         # 弹出警告消息框
    #         self.ui_manager.show_message_box("警告", "请先点击\"开始采集\"按钮", "warning")
    #         return   
    #     # 在状态栏显示采集下一张图片消息
    #     self.ui_manager.show_status_message("采集下一张图片，请稍后")
    #     # 设置继续采集标志为True
    #     self.recording = True


    """
    函数名称：holdImg
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：保留拍摄的图片到图片管理区
    """
    def holdImg(self):
        # 获取当前显示的图片
        pixmap = self.collectImageLabel.pixmap()
        if pixmap:
            # 获取当前时间作为图片名称
            saveTime = datetime.now()
            imageName = saveTime.strftime(r"%Y%m%d_%H%M%S")
            # 如果图片名称不在已保存的图片路径中，则添加图片到右侧图片管理区
            if imageName not in self.image_path:
                self.showImgGridWiget.add_image(imageName, pixmap)
                # app.ms.addImageLabel.emit(imageName, pixmap, app.gridLayout)
                self.collectImageLabel.clear()
                # 在状态栏显示图片保留在右侧图片管理区消息
                self.ui_manager.show_status_message("图片保留在右侧图片管理区")
                # app.ms.showStatus.emit("图片保留在右侧图片管理区", app.statusBar)
        else:
            # 如果没有图片可以保留，弹出警告消息框
            self.ui_manager.show_message_box("警告", "没有图片可以保留", "warning")
            # app.ms.popMessageBox.emit("warning", "警告", "没有图片可以保留")


    """
    函数名称：selectAllImg
    参数说明：app:应用程序对象  state:全选/取消全选复选框状态
    函数返回：无
    功能概要：全选/取消全选图片管理区所有图片
    """
    def selectAllImg(self, state):
        # 如果状态为选中，则执行全选操作
        if state == Qt.CheckState.Checked.value:
            self.showImgGridWiget.selectAllImg()
        # 如果状态为未选中，则执行取消全选操作
        else:
            self.showImgGridWiget.cancelSelectAllImg()


    """
    函数名称：deleteBatchImg
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：毗连删除图片管理区所有选中的图片
    """
    def deleteBatchImg(self):
        # 获取图片管理区所有选中的图片
        selectdImgs = self.showImgGridWiget.get_selected_images()
        # 获取当前图像数量
        currentImgNum = len(self.showImgGridWiget.images)
        # 遍历要删除的图像列表
        for image,_ in selectdImgs:
            self.showImgGridWiget.del_image(image)
        # 更新网格布局
        self.showImgGridWiget.update(currentImgNum)

        # 发送信号删除图片管理区所有选中的图片
        # app.ms.delBatchImage.emit(selectdImgs, self.gridLayout)


    """
    函数名称：showImgState
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：显示图片管理器信息，格式为：已选中...张图片，共有...张图片
    """
    def showImgState(self):
        # 获取图片管理区所有选中的图片
        selectedImg = self.showImgGridWiget.get_selected_images()
        # 获取图片管理区图片数量
        totalImg = self.showImgGridWiget.images
        # 发送信号，在界面中显示图片管理区图片信息
        # self.ui_manager.show_status_message(f"已选中{len(selectedImg)}张图片,共有{len(totalImg)}张图片")
        self.imgNum.setText(f"已选中{len(selectedImg)}张图片,共有{len(totalImg)}张图片")
        # app.ms.showStatus.emit(f"已选中{len(selectedImg)}张图片,共有{len(totalImg)}张图片", app.ImgNum)


    """
    函数名称：loadVideo
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：导入视频文件并在视频播放器中显示
    """
    def loadVideo(self):
        # 在状态栏显示导入视频的提示信息
        self.ui_manager.show_status_message("导入视频")
        # 获取用户选择的视频文件路径
        fileName, _ = QFileDialog.getOpenFileName(self.__data_acuisition_widget, "导入视频", filter="视频文件 (*.mp4 *.avi *.mov *.mkv)")
        # 如果未选择文件，则在状态栏显示取消导入视频的提示信息，并返回
        if not fileName:
            # 在状态栏显示取消导入视频的提示信息，并返回
            self.ui_manager.show_status_message("取消导入视频")
            return
        # 获取视频文件的文件名
        file = os.path.basename(fileName)
        # 在界面上显示视频文件的文件名
        self.videoName.setText(file)
        # 设置删除视频的按钮为可见
        self.deleteVideoButton.setVisible(True)
        # 设置视频播放器的视频源为所选择的视频文件
        self.player.mediaPlayer.setSource(fileName)
        # 启用播放视频按钮
        self.playVideoButton.setEnabled(True)
        # 在视频播放器中显示视频封面
        self.player.show_video_cover(fileName)
        # 设置逐帧分解视频按钮为可点击状态
        self.decomposeVideoButton.setEnabled(True)


    """
    函数名称：format_time
    参数说明：ms:时间，单位是毫秒
    函数返回：无
    功能概要：格式化毫秒表示的时间为时:分:秒
    """
    def format_time(self, ms):
        # 计算秒数、分钟数和小时数
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        hours = (ms // (1000 * 60 * 60)) % 24
        # 如果小时数大于0，则返回格式化后的时间字符串，包括小时、分钟和秒
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        # 否则，返回格式化后的时间字符串，不包括小时，只有分钟和秒
        else:
            return f"{minutes:02}:{seconds:02}"


    """
    函数名称：sliderEvent
    参数说明：app:应用程序对象  position:视频播放器滑块位置
    函数返回：无
    功能概要：处理视频播放器滑块事件
    """
    def sliderEvent(self, position):
        # 设置视频滑块的当前值
        self.videoSlider.setValue(position)
        # 格式化并显示视频播放的开始时间
        self.videoStartTime.setText(self.format_time(position))


    """
    函数名称：durationEvent
    参数说明：app:应用程序对象  duration:视频播放时长
    函数返回：无
    功能概要：处理视频播放器持续时间事件
    """
    def durationEvent(self, duration):
        # 设置视频滑块的范围为视频持续时间
        self.videoSlider.setRange(0, duration)
        # 格式化并显示视频播放的结束时间
        self.videoEndTime.setText(self.format_time(duration))


    """
    函数名称：decomposeVideo
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：逐帧分解视频
    """
    def decomposeVideo(self):
        # 在状态栏显示提示信息
        self.ui_manager.show_status_message("正在逐帧分解视频，请稍后")
        # app.ms.showStatus.emit("正在逐帧分解视频，请稍后", app.statusBar)
        # 获取视频路径
        video_path = self.player.video_path
        # 检查视频路径是否为空
        if not video_path:
            self.ui_manager.show_message_box("错误", "没有视频可以解析，请先导入一个视频。", "critical")
            # app.ms.popMessageBox.emit("critical", "错误", "没有视频可以解析，请先导入一个视频。")
            return
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        # 获取视频文件名（不包含扩展名）
        videoName = os.path.splitext(os.path.basename(video_path))[0]
        # 检查视频是否成功打开
        if not cap.isOpened():
            self.ui_manager.show_message_box("错误", "无法打开视频文件。", "critical")
            # app.ms.popMessageBox.emit("critical", "错误", "无法打开视频文件。")
            return
        # 获取视频总帧数和帧率
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = int(cap.get(cv2.CAP_PROP_FPS))
        frames = []
        frame_index = 0
        idx = 0
        # 逐帧读取视频，并每隔一定帧率保存一帧图片
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_index % frame_interval == 0:
                # 将帧转换为QImage格式
                height, width, _ = frame.shape
                bytes_per_line = 3 * width
                cv_img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qImage = QImage(cv_img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qImage)
                # 发射信号以在UI上添加图片标签
                self.showImgGridWiget.add_image(f"{videoName}_{idx}", pixmap)
                # app.ms.addImageLabel.emit(f"{videoName}_{idx}", pixmap, app.gridLayout)
                idx += 1
                frames.append(frame)
            frame_index += 1
        # 释放视频对象
        cap.release()
        # 在状态栏显示分解视频成功的信息
        self.ui_manager.show_status_message("逐帧分解视频成功")
        # app.ms.showStatus.emit("逐帧分解视频成功", app.statusBar)


    """
    函数名称：saveBatchImg
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：批量保存图片
    修改   ： WTX修改jpg为bmp,保存图片为映射后的图片
    """
    def saveBatchImg(self):
        import shutil
        # 获取图片保存路径
        self.ImgSavePath = QFileDialog.getExistingDirectory(self.__data_acuisition_widget, caption="选择图片保存路径")
        if not self.ImgSavePath:
            return
        
        # 在UI上设置图片保存路径
        self.imgPath.setText(f"保存路径：{self.ImgSavePath}")
        # 获取选中的图片列表
        selectdImgs = self.showImgGridWiget.get_selected_images()
        idx = 0
        totalImgNum = len(selectdImgs)
        # # 遍历选中的图片列表，保存每张图片到指定路径
        # for image, pixmap in selectdImgs:
        #     # imagePath = f"{self.ImgSavePath}/{image}.jpg"
        #     imagePath = f"{self.ImgSavePath}/{image}.bmp"
        #     pixmap.save(imagePath)
        #     idx += 1
        #     # 在状态栏显示保存进度信息
        #     self.ui_manager.show_status_message(f"正在保存第{idx}/{totalImgNum}张图片")
        #     # app.ms.showStatus.emit(f"正在保存第{idx}/{totalImgNum}张图片", app.statusBar)
        # # 在状态栏显示批量保存成功的信息
        # self.ui_manager.show_status_message(f"批量保存成功!")
        # self.ui_manager.show_message_box("提示", f"批量保存成功!", "info")
        # # app.ms.showStatus.emit(f"批量保存成功!", app.statusBar)
        # # 弹出提示框，显示保存图片数量信息
        # self.ui_manager.show_message_box("提示", f"成功保存{totalImgNum}张图片！", "information")
        # # app.ms.popMessageBox.emit("information", "提示", f"成功保存{totalImgNum}张图片！")
        
        #wtx修改
        # 遍历选中的图片列表，保存每张图片到指定路径
        for image, pixmap in selectdImgs:
            # 检查是否有对应的原始BMP文件路径
            if image in self.image_bmp_paths:
                # 从原始BMP文件复制到目标路径
                source_path = self.image_bmp_paths[image]
                target_path = f"{self.ImgSavePath}/{image}.bmp"
                try:
                    shutil.copy2(source_path, target_path)
                    idx += 1
                    # 在状态栏显示保存进度信息
                    self.ui_manager.show_status_message(f"正在保存第{idx}/{totalImgNum}张图片")
                    #app.ms.showStatus.emit(f"正在保存第{idx}/{totalImgNum}张图片", app.statusBar)
                except Exception as e:
                    print(f"复制文件失败: {e}")
                    self.ui_manager.show_status_message(f"保存图片失败: {str(e)}")
                    #app.ms.showStatus.emit(f"保存图片失败: {str(e)}", app.statusBar)
            else:
                # 如果没有对应的原始BMP文件，则保存Pixmap
                imagePath = f"{self.ImgSavePath}/{image}.bmp"  # 改为.bmp格式
                pixmap.save(imagePath, "BMP")  # 指定保存为BMP格式
                idx += 1
                # 在状态栏显示保存进度信息
                self.ui_manager.show_status_message(f"正在保存第{idx}/{totalImgNum}张图片")
                # app.ms.showStatus.emit(f"正在保存第{idx}/{totalImgNum}张图片", app.statusBar)
        # # 在状态栏显示批量保存成功的信息
        # app.ms.showStatus.emit(f"批量保存成功!", app.statusBar)
        # # 弹出提示框，显示保存图片数量信息
        # app.ms.popMessageBox.emit("information", "提示", f"成功保存{totalImgNum}张BMP图片！")
        self.ui_manager.show_status_message(f"批量保存成功!")
        self.ui_manager.show_message_box("提示", f"成功保存{totalImgNum}张图片！", "information")


    """
    函数名称：clearGridWidget
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：清空图片管理区
    """
    def clearGridWidget(self):
        # 获取当前图像数量
        currentImgNum = len(self.showImgGridWiget.images)
        # 删除所有图像标签
        self.showImgGridWiget.del_all_image()
        # 更新网格布局
        self.showImgGridWiget.update(currentImgNum)
        # 发射信号以清空图片管理区域
        # app.ms.clearImgManageArea.emit(app.gridLayout)
        # 在状态栏显示清空图片管理区成功的信息
        self.ui_manager.show_status_message("清空图片管理区成功")
        # app.ms.showStatus.emit(f"清空图片管理区成功", app.statusBar)

    """
    函数名称：deleteVideo
    参数说明：app:应用程序对象
    函数返回：无
    功能概要：清空视频
    """
    def deleteVideo(self):
        # 清空视频
        self.player.clear_video()
        # 设置删除视频按钮不可见
        self.deleteVideoButton.setVisible(False)
        # 清空视频名称
        self.videoName.clear()
        # 设置逐帧分解按钮为可不点击状态
        self.decomposeVideoButton.setEnabled(False)
        # 设置播放按钮可点击
        self.playVideoButton.setEnabled(False) 



    def showImage(self, img_src, label: QLabel):
        """
        函数名称：showImage
        参数说明：img_src:待显示的图片 (numpy array) label:显示图片的QLabel对象
        函数返回：无
        功能概要：显示图片在标签上，并根据标签大小调整图片尺寸
        """
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
            QMessageBox.warning(None, "警告", str(e))
            print(repr(e))