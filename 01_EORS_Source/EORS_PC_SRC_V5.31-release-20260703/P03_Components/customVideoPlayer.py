from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QPushButton
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QIcon, QPixmap, QImage, QResizeEvent, QShowEvent
from PySide6.QtCore import QTimer, Qt
import cv2

"""
类名：CoverWidget
基类：QLabel:Qt标签控件类
功能：自定义视频封面组件
"""
class CoverWidget(QLabel):

    """
    函数名称：__init__
    参数说明：无
    函数返回：无
    功能概要：初始化自定义视频封面组件
    """
    def __init__(self):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__()
        # 设置标签内容居中显示
        self.setAlignment(Qt.AlignCenter)
        # 设置标签的背景颜色为黑色
        self.setStyleSheet("background-color: black;")
        # 设置标签初始时不可见
        self.setVisible(False)
        # 存储标签初始化时的宽度和高度
        self.old_width = self.width()
        self.old_height = self.height()


    """
    函数名称：set_cover_image
    参数说明：pixmap:视频封面图片
    函数返回：无
    功能概要：设置封面图片
    """
    def set_cover_image(self, pixmap):
        # 将输入的封面图片按照当前标签的大小进行缩放，保持长宽比并使用平滑的转换方式
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # 设置标签的图片为缩放后的封面图片
        self.setPixmap(scaled_pixmap)
        # 设置标签可见
        self.setVisible(True)


    """
    函数名称：resizeEvent
    参数说明：event:窗口大小改变事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理窗口大小改变事件
    """
    def resizeEvent(self, event: QResizeEvent):
        # 获取标签新的宽度和高度
        new_width = self.width()
        new_height = self.height()
        # 如果标签有图片
        if self.pixmap():
            # 如果标签有存储原始尺寸的属性
            if hasattr(self, 'normalHeight'):
                # 如果新的高度或宽度小于原始尺寸
                if new_height < self.old_height or new_width < self.old_width :
                    # 使用原始尺寸进行缩放
                    scaled_pixmap = self.pixmap().scaled(self.normalSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                else:
                    # 使用新的尺寸进行缩放
                    scaled_pixmap = self.pixmap().scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                # 使用新的尺寸进行缩放
                scaled_pixmap = self.pixmap().scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # 设置标签的图片为缩放后的图片
            self.setPixmap(scaled_pixmap)
        # 更新存储的宽度和高度
        self.old_width = new_width
        self.old_height = new_height
        # 调用父类的 resizeEvent 方法处理事件
        super().resizeEvent(event)


    """
    函数名称：showEvent
    参数说明：event:显示事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理标签显示时的事件
    """
    def showEvent(self, event: QShowEvent):
        # 存储标签的原始宽度、高度和大小
        self.normalWidth = self.width()
        self.normalHeight = self.height()
        self.normalSize = self.size()
        # 调用父类的 showEvent 方法处理事件
        super().showEvent(event)


"""
类名：VideoPlayer
基类：QWidget:Qt部件类
功能：自定义视频播放器
"""
class VideoPlayer(QWidget):

    """
    函数名称：__init__
    参数说明：slider_callback:滑块回调函数 duration_callback:持续时间回调函数 parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义视频播放器
    """
    def __init__(self, slider_callback=None, duration_callback=None, parent=None):
        # 调用父类的构造方法，初始化父类的属性和方法
        super().__init__(parent)
        # 存储视频路径和回调函数
        self.video_path = ""
        # 滑块回调函数，用于更新视频播放进度
        self.slider_callback = slider_callback
        # 持续时间回调函数，用于更新视频总时长
        self.duration_callback = duration_callback
        # 创建一个媒体播放器对象
        self.mediaPlayer = QMediaPlayer()
        # 创建一个视频显示部件
        self.videoWidget = QVideoWidget()
        # 设置视频显示部件尺寸策略
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建一个封面显示部件
        self.coverWidget = CoverWidget()
        # 设置封面显示部件尺寸策略
        self.coverWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建垂直布局
        self.layout = QVBoxLayout()
        # 将封面显示部件添加到布局中
        self.layout.addWidget(self.coverWidget)
        # 将视频显示部件添加到布局中
        self.layout.addWidget(self.videoWidget)
        # 设置布局
        self.setLayout(self.layout)
        # 将视频输出连接到视频小部件
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # 当媒体状态发生变化时触发该信号，用于处理媒体状态的变化，比如播放、暂停、停止等
        self.mediaPlayer.mediaStatusChanged.connect(self.handle_media_status_change)
        # 当媒体播放位置发生变化时触发该信号，用于更新当前播放位置，以便更新滑块的位置
        self.mediaPlayer.positionChanged.connect(self.update_position)
        # 当媒体总时长发生变化时触发该信号，用于更新媒体的总时长，以便显示在用户界面上
        self.mediaPlayer.durationChanged.connect(self.update_duration)


    """
    函数名称：play_video
    参数说明：btn：控制播放/暂停的按钮
    函数返回：无
    功能概要：控制视频的播放和暂停，根据当前的播放状态执行相应的操作
    """
    def play_video(self, btn):
        # 显示视频播放部件
        self.videoWidget.setVisible(True)
        # 如果媒体播放器正在播放
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlayingState:
            # 设置按钮图标
            btn.setIcon(QIcon('./02-Image/begin.png'))
            # 设置按钮提示文本
            btn.setToolTip("开始播放")
            # 暂停媒体播放
            self.mediaPlayer.pause()
        else:
            # 隐藏封面小部件
            # self.coverWidget.setVisible(False)
            # 设置按钮图标
            btn.setIcon(QIcon('./02-Image/stop.png'))
            # 设置按钮提示文本
            btn.setToolTip("暂停播放")
            # 开始播放视频
            self.mediaPlayer.play()


    """
    函数名称：set_position
    参数说明：position:视频播放的位置
    函数返回：无
    功能概要：设置视频播放的位置，以便用户能够跳转到视频的特定时间点进行播放
    """
    def set_position(self, position):
        # 设置媒体播放器的位置
        self.mediaPlayer.setPosition(position)


    """
    函数名称：show_video_cover
    参数说明：file_path:视频文件路径
    函数返回：无
    功能概要：显示视频封面
    """
    def show_video_cover(self, file_path):
        # 将视频文件路径保存起来
        self.video_path = file_path
        # 隐藏视频小部件
        self.videoWidget.setVisible(False)
        # 使用 OpenCV 打开视频文件
        cap = cv2.VideoCapture(file_path)
        # 读取第一帧的图像数据
        ret, frame = cap.read()
        if ret:
            # 将图像从BGR格式转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 获取帧高度和宽度
            height, width, _ = frame.shape
            # 计算每行的字节数
            bytes_per_line = 3 * width
            # 创建QImage对象
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # 从QImage创建QPixmap对象
            pixmap = QPixmap.fromImage(image)
            # 在封面小部件中设置封面图片
            self.coverWidget.set_cover_image(pixmap)
        # 释放视频捕获对象
        cap.release()


    """
    函数名称：handle_media_status_change
    参数说明：status: 媒体状态
    函数返回：无
    功能概要：处理媒体播放状态的变化
    """
    def handle_media_status_change(self, status):
        # 如果媒体状态变为 EndOfMedia，即播放到视频的末尾
        if status == QMediaPlayer.EndOfMedia:
            # 延迟 100 毫秒后调用 show_last_frame 方法
            QTimer.singleShot(100, self.show_last_frame)


    """
    函数名称：show_last_frame
    参数说明：无
    函数返回：无
    功能概要：显示视频最后一帧图像
    """
    def show_last_frame(self):
        # 使用 OpenCV 打开视频文件
        cap = cv2.VideoCapture(self.video_path)
        # 将视频捕获对象的位置设置为最后一帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        # 读取最后一帧的图像数据
        ret, frame = cap.read()
        if ret:
            # 将图像从BGR格式转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 获取帧高度和宽度
            height, width, _ = frame.shape
            # 计算每行的字节数
            bytes_per_line = 3 * width
            # 创建QImage对象
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # 从QImage创建QPixmap对象
            pixmap = QPixmap.fromImage(image)
            # 在封面小部件中设置封面图片
            self.coverWidget.set_cover_image(pixmap)
        # 隐藏视频小部件
        self.videoWidget.setVisible(False)
        # 获取控制视频播放/暂停的按钮
        playVideoBtn = self.parent().parent().findChild(QPushButton, "playVideo")
        # 设置按钮图标
        playVideoBtn.setIcon(QIcon('./02-Image/begin.png'))
        # 设置按钮提示文本
        playVideoBtn.setToolTip("开始播放")
        # 释放视频捕获对象
        cap.release()


    """
    函数名称：update_position
    参数说明：position:视频播放的位置
    函数返回：无
    功能概要：更新播放器的当前播放位置
    """
    def update_position(self, position):
        # 调用回调函数，更新滑块位置
        self.slider_callback(position)


    """
    函数名称：update_duration
    参数说明：duration:视频的总时长
    函数返回：无
    功能概要：更新视频的总时长
    """
    def update_duration(self, duration):
        # 调用回调函数，处理新的视频时长
        self.duration_callback(duration)

    """
    函数名称：update_duration
    参数说明：duration:视频的总时长
    函数返回：无
    功能概要：更新视频的总时长
    """
    def clear_video(self):
        # 隐藏视频小部件
        self.videoWidget.setVisible(False)
        self.update_position(0)
        self.coverWidget.clear()