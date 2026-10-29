from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QDialog,QDialogButtonBox, QMessageBox, QSizePolicy, QPushButton
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import Qt, QEvent, QSize, QPoint, Signal
from . customButton import HoverButton
from . customTooltip import ToolTip
import os


"""
类名：ImageLabel
基类：QWidget:Qt部件类
功能：自定义图片标签组件
"""
class ImageLabel(QWidget):
    """
    函数名称：__init__
    参数说明：image_name:图片名称  pixmap:图片像素数据  delete_callback:删除图片的回调函数（可选）。默认为None  parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义图片标签
    """
    def __init__(self, image_name:str, pixmap:QPixmap, imageWidth, imageHeight, delete_callback=None, parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__(parent)
        # 初始化图片名称
        self.image_name = image_name
        # 初始化图片的像素数据
        self.pixmap = pixmap
        # 删除图片的回调函数
        self.delete_callback = delete_callback
        # 设置固定大小
        self.setFixedSize(imageWidth + 5, imageHeight + 5) 
        # 创建用于显示图片的标签
        self.image_label = QLabel(self)
        # 将图片缩放到 imageWidth x imageHeight 大小，保持宽高比，并进行平滑转换
        self.image_label.setPixmap(pixmap.scaled(imageWidth, imageHeight, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        # 设置图片在标签中居中对齐
        self.image_label.setAlignment(Qt.AlignCenter)
        # 设置标签的固定大小为 imageWidth x imageHeight
        self.image_label.setFixedSize(imageWidth, imageHeight)
        # 将标签移动到父控件内的 (5, 5) 位置
        self.image_label.move(5, 5)
        # 创建蒙层
        self.overlay = QWidget(self)
        # 设置蒙层样式
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        # 默认隐藏蒙层
        self.overlay.hide()  
        # 创建复选框
        self.checkbox = QCheckBox(self)
        # 设置复选框位置
        self.checkbox.setGeometry(imageWidth+5-20, imageHeight+5-20, 20, 20)
        # 设置复选框样式
        self.checkbox.setStyleSheet(u"QCheckBox{"
                                    "background-color:transparent;"
                                    "}QCheckBox::indicator{"
                                    "width:20px;height:20px;margin:0px;}")
        # 默认隐藏复选框
        self.checkbox.hide() 
        # 创建放大按钮
        self.enlarge_button = HoverButton("./02-Image/enlarge-gray.png", "./02-Image/enlarge.png", "", self.overlay)
        # 设置放大按钮对象名称
        self.enlarge_button.setObjectName("enlargeBtn")
        # 设置放大按钮固定大小
        self.enlarge_button.setFixedSize(20, 20)
        # 设置放大按钮图标大小
        self.enlarge_button.setIconSize(QSize(20, 20))
        # 设置放大按钮样式
        self.enlarge_button.setStyleSheet("background-color: transparent;border:none;")
        # 默认隐藏按钮
        self.enlarge_button.hide()  
        # 绑定放大按钮点击事件
        self.enlarge_button.clicked.connect(self.show_image_dialog)
        # 为放大按钮安装事件过滤器
        self.enlarge_button.installEventFilter(self)
        # 创建删除按钮
        self.delete_button = HoverButton("./02-Image/delete-gray.png", "./02-Image/delete-black.png", "", self.overlay)
        # 设置删除按钮对象名称
        self.delete_button.setObjectName("deleteBtn")
        # 设置删除按钮固定大小
        self.delete_button.setFixedSize(20, 20)
        # 设置删除按钮图标大小
        self.delete_button.setIconSize(QSize(20, 20))
        # 设置删除按钮样式
        self.delete_button.setStyleSheet("background-color: transparent;border:none;")
        # 默认隐藏按钮
        self.delete_button.hide()  
        # 绑定删除按钮点击事件
        self.delete_button.clicked.connect(self.delete_image)
        # 为删除按钮安装事件过滤器
        self.delete_button.installEventFilter(self)
        # 设置蒙层位置
        self.overlay.setGeometry(5, 5, imageWidth, imageHeight)
        # 实例化自定义工具提示组件
        self._tooltip = ToolTip(parent=self)
        # 自定义工具提示组件默认隐藏
        self._tooltip.hide()
        # 安装事件过滤器
        self.installEventFilter(self)


    """
    函数名称：eventFilter
    参数说明：source:被监视的对象，其事件将被过滤 event:要过滤的事件
    函数返回：无
    功能概要：过滤被监视对象的事件
    """
    def eventFilter(self, source, event: QEvent):
        # 获取被监视对象的对象名
        objName = source.objectName()
        # 鼠标移入所执行的功能
        if event.type() == QEvent.Enter:
            # 若鼠标移入放大按钮和删除按钮
            if objName == "enlargeBtn" or objName == "deleteBtn":
                # 设置提示组件中的文本内容
                text = "查看" if objName == "enlargeBtn" else "删除"
                self._tooltip.setText(text)
                # 初始化自定义提示控件的位置
                x = 0
                y = 0
                pos = source.mapTo(self, QPoint(0, 0))
                # 获取被监视对象的可视宽度
                objWidth = source.visibleRegion().boundingRect().width()
                # 获取被监视对象的可视高度
                objHeight = source.visibleRegion().boundingRect().height()
                # 被监视对象的提示组件显示在上方
                x = pos.x() + objWidth//2 - self._tooltip.width()//2
                y = pos.y() - 5 - self._tooltip.height()
                # 将提示组件移动到指定位置
                self._tooltip.move(x, y)
                # 显示提示组件
                self._tooltip.show()
            # 鼠标移入除放大按钮和删除按钮以外的组件
            else:
                # 显示复选框
                self.checkbox.show()
                # 显示蒙层
                self.overlay.show()
                # 显示放大按钮
                self.enlarge_button.show()
                # 显示删除按钮
                self.delete_button.show()
        # 鼠标移出所执行的功能
        elif event.type() == QEvent.Leave:
            # 若鼠标移出放大按钮和删除按钮
            if objName == "enlargeBtn" or objName == "deleteBtn":
                # 隐藏工具提示组件
                self._tooltip.hide()
            # 若鼠标移出除放大按钮和删除按钮以外的组件
            else:
                # 如果复选框未被选中，则鼠标移出时将复选框隐藏
                if not self.checkbox.isChecked():
                    self.checkbox.hide()
                # 隐藏蒙层
                self.overlay.hide()
                # 隐藏放大按钮
                self.enlarge_button.hide()
                # 隐藏删除按钮
                self.delete_button.hide()  
        # 调用基类的eventFilter方法处理未处理的事件
        return super().eventFilter(source, event)


    """
    函数名称：resizeEvent
    参数说明：event:窗口大小改变事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理窗口大小改变事件
    """
    def resizeEvent(self, event: QResizeEvent):
        # 调用父类的 resizeEvent 方法，确保继承的事件处理行为
        super().resizeEvent(event)
        # 设置蒙层的几何位置和大小与图片标签一致
        self.overlay.setGeometry(self.image_label.geometry())
        # 调整放大按钮的位置，使其位于图片标签中央偏左的位置 
        self.enlarge_button.move(
            self.image_label.width() // 2 - self.enlarge_button.width() - 5,
            self.image_label.height() // 2 - self.enlarge_button.height() // 2
        )
        # 调整删除按钮的位置，使其位于图片标签中央偏右的位置
        self.delete_button.move(
            self.image_label.width() // 2 + 5,
            self.image_label.height() // 2 - self.delete_button.height() // 2
        )


    """
    函数名称：show_image_dialog
    参数说明：无
    函数返回：无
    功能概要：显示一个对话框，用于放大显示图片
    """
    def show_image_dialog(self):
        # 创建一个新的 QDialog 对象，设置其父控件为当前对象
        dialog = QDialog(self)
        # 设置对话框标题
        dialog.setWindowTitle("放大图片")
        # 创建垂直布局，并将其设置为对话框的布局
        dialog_layout = QVBoxLayout(dialog)
        # 设置对话框背景颜色
        dialog.setStyleSheet("background-color:#eef2ff;")
        # 显示放大图片
        enlarged_label = QLabel(dialog)
        # 获取当前图片
        pixmap = self.pixmap
        # 缩放图片到 400x400，保持宽高比并进行平滑转换
        enlarged_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # 设置图片在标签中居中对齐
        enlarged_label.setAlignment(Qt.AlignCenter)
        # 将标签添加到对话框的布局中
        dialog_layout.addWidget(enlarged_label)
        # 创建 QDialogButtonBox 对象，包含一个"确定"按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        # 设置按钮样式
        button_box.setStyleSheet(u"QPushButton{\n"
                "	border: none;\n"
                "	background-color: #e1d9fe;\n"
                "	color:  #b28cfe;\n"
                "	font-weight: 600;\n"
                "	padding: 4px 8px;\n"
                "	border-radius: 4px;\n"
                "}\n"
                "QPushButton:hover{\n"
                "	color: #fff;\n"
                "	background-color: #b28cfe;\n"
                "}")
        # 连接"确定"按钮的点击信号到对话框的accept槽函数
        button_box.accepted.connect(dialog.accept)
        # 将按钮框添加到对话框的布局中
        dialog_layout.addWidget(button_box)
        # 显示对话框，并阻塞直到对话框关闭
        dialog.exec()


    """
    函数名称：delete_image
    参数说明：无
    函数返回：无
    功能概要：显示删除确认对话框，并在用户确认时删除图片
    """
    def delete_image(self):
        # 创建一个 QMessageBox 对象，用于显示确认删除对话框
        messageBox = QMessageBox(self)
        # 设置对话框标题
        messageBox.setWindowTitle("删除确认")
        # 设置对话框内容
        messageBox.setText("您确定要删除这张图片吗？")
        # 设置标准按钮：确定和取消
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 设置对话框样式
        messageBox.setStyleSheet("font-weight: 600; font-size: 14px; background-color: #eef2ff;color:#000000;")
        # 获取"确定"按钮
        buttonYes = messageBox.button(QMessageBox.Yes)
        # 设置确定按钮内容
        buttonYes.setText("确定")
        # 设置确定按钮对象名称
        buttonYes.setObjectName("buttonYes")
        # 设置确定按钮样式
        buttonYes.setStyleSheet("""
            QPushButton {
                border:none;
                background-color: #e0e7ff;
                color: #4f46e9;
                padding: 4px 8px;
                font-weight: 600;
                font-size: 12px;
                border-radius: 2px;
            }
            QPushButton:hover{
                background-color: #4f46e5;
                color: #fff;
            }
            """)
        # 获取"取消"按钮
        buttonNo = messageBox.button(QMessageBox.No)
        # 设置取消按钮文本
        buttonNo.setText("取消")
        # 设置取消按钮对象名称
        buttonNo.setObjectName("buttonNo")
        # 设置取消按钮样式
        buttonNo.setStyleSheet("""
            QPushButton {
                border:none;
                background-color: #e5e7eb;
                color: #374151;
                padding: 4px 8px;
                font-weight: 600;
                font-size: 12px;
                border-radius: 2px;
            }
            QPushButton:hover{
                background-color: #374151;
                color: #fff;
            }
        """)
        # 显示对话框，并阻塞当前窗口，直到用户做出选择 
        messageBox.exec_()
        # 如果用户点击了"确定"按钮，则调用删除回调函数删除图片
        if messageBox.clickedButton() == buttonYes:
            self.delete_callback(self.image_name)


    """
    函数名称：checked
    参数说明：无
    函数返回：无
    功能概要：将复选框设置为选中状态并显示复选框
    """
    def checked(self):
        # 设置复选框为选中状态
        self.checkbox.setChecked(True)
        # 显示复选框
        self.checkbox.show()


    """
    函数名称：unchecked
    参数说明：无
    函数返回：无
    功能概要：将复选框设置为未选中状态并隐藏复选框
    """
    def unchecked(self):
        # 设置复选框为未选中状态
        self.checkbox.setChecked(False)
        # 隐藏复选框
        self.checkbox.hide()


"""
类名：CustomLabel
基类：QLabel:Qt标签控件类
功能：自定义标签组件
"""
class CustomLabel(QLabel):

    """
    函数名称：__init__
    参数说明：text:标签内容  parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义图片标签
    """
    def __init__(self, text="", parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__(parent)
        # QLabel中显示的文本
        self.content = text
        # 设置标签尺寸策略
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        # 设置标签允许通过鼠标选择文本
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)


    """
    函数名称：resizeEvent
    参数说明：event:窗口大小改变事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理窗口大小改变事件
    """
    def resizeEvent(self, event: QResizeEvent):
        # 调用父类的 resizeEvent 方法，确保继承的事件处理行为
        super().resizeEvent(event)
        # 计算显示文本的宽度，减去固定宽度123
        showTextWidth = self.parent().width()-123
        # 根据显示文本的宽度，截断文本内容以适应新的宽度，并在中间添加省略号
        showText = self.fontMetrics().elidedText(self.content, Qt.ElideMiddle, showTextWidth)
        # 更新显示的文本
        self.setText(showText)


    """
    函数名称：setContent
    参数说明：content:标签内容
    函数返回：无
    功能概要：设置标签的内容，并根据当前宽度调整显示的文本
    """
    def setContent(self, content):
        # 设置内容
        self.content = content
        # 设置工具提示为内容
        self.setToolTip(content)
        # 计算显示文本的宽度，减去固定宽度123
        showTextWidth = self.parent().width()-123
        # 根据显示文本的宽度，截断文本内容以适应新的宽度，并在中间添加省略号
        showText = self.fontMetrics().elidedText(self.content, Qt.ElideMiddle, showTextWidth)
        # 更新显示的文本
        self.setText(showText)


class CustomImageWidget(QWidget):
    # 删除请求信号
    delete_requested = Signal(QWidget)
    STYLE_SHEET = """
            QLabel{
                border: 1px solid #c5cdd3;
                border-radius: 4px;
            }
            QLabel:hover{
                border: 1px solid #6a7bff;
            }
            QLabel:focus{
                border: 2px solid #6a7bff;
            }
    """
    def __init__(self, image_path: str, image_height:int, image_width:int, is_selected:bool, click_callback=None, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.image_height = image_height
        self.image_width = image_width
        self.label_width = image_width
        self.label_height = image_height
        self.click_callback = click_callback
        self.is_selected = is_selected
        self.init_ui()
    def init_ui(self):
        # self.setStyleSheet(self.STYLE_SHEET)
        # 设置标签尺寸策略
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        # 图像像素标签
        self.image_pixmap_label = QLabel(self)
        self.image_pixmap_label.setFixedSize(120, 80)
        self.image_pixmap_label.setStyleSheet(self.STYLE_SHEET)
        self.image_pixmap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_image()

        
        # 更新显示的文本
        self.image_name_label = QLabel(self)
        self.update_image_name()
        
        # 删除按钮
        self.delete_button = QPushButton("×", self)
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #d4d4d9;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #25292d;
            }
""")
        self.delete_button.move(self.label_width - 24, 14)
        self.delete_button.clicked.connect(self.on_delete_clicked)

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)  # 设置上下左右的边距为 0
        layout.setAlignment(Qt.AlignHCenter)  # 水平居中
        layout.addWidget(self.image_pixmap_label)
        layout.addWidget(self.image_name_label)
        self.setLayout(layout)

        # 设置被选中样式
        if self.is_selected:
            self.image_pixmap_label.setStyleSheet("""
                QLabel{
                    border: 2px solid #6a7bff;
                    border-radius: 8px;
                }
            """)
        
    # 更新图片，保持宽高比
    def update_image(self):
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.label_width, self.label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_pixmap_label.setPixmap(scaled_pixmap)
        
    def update_image_name(self):
        # 图像名称标签
        image_name = os.path.basename(self.image_path)
        # 根据显示文本的宽度，截断文本内容以适应新的宽度，并在中间添加省略号
        show_image_name = self.fontMetrics().elidedText(image_name, Qt.TextElideMode.ElideRight, self.width())
        self.image_name_label.setText(show_image_name)


    def enterEvent(self, event):
        # 鼠标进入时设置背景颜色
        self.setStyleSheet("background-color: transparent;")

    def leaveEvent(self, event):
        # 鼠标离开时恢复背景颜色
        self.setStyleSheet("background-color: transparent;")

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        self.click_callback(self)
        self.is_selected = True
        self.clickedStyle()

    def resetStyle(self):
        self.image_pixmap_label.setStyleSheet(self.STYLE_SHEET)

    def clickedStyle(self):
        self.image_pixmap_label.setStyleSheet("""
                QLabel{
                    border: 2px solid #6a7bff;
                    border-radius: 8px;
                }
            """)
        
    def on_delete_clicked(self):
        self.delete_requested.emit(self.list_item) # 发出删除请求信号

    