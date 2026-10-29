from . customLabel import ImageLabel
from PySide6.QtWidgets import QGridLayout, QWidget
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import Qt
"""
类名：CustomGridLayout
基类：QWidget:Qt部件类
功能：自定义网格布局
"""
class CustomGridLayout(QWidget):

    """
    函数名称：__init__
    参数说明：parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义网格布局
    """
    def __init__(self, collectImgWidth, colletcImgHeight, parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__(parent)
        # 初始化布局为 QGridLayout，并将其设置为该窗口的布局
        self.layout = QGridLayout(self)
        # 设置布局中的控件间距为 0
        self.layout.setSpacing(0)
        # 初始化图片列表，用于存储图片名称
        self.images = []
        # 初始化图片标签列表，用于存储ImageLabel对象
        self.image_labels = []
        # 设置默认的列数为 5
        self.columns = 5
        # 初始化采集图像的宽度
        self.colletImgWidth = collectImgWidth
        # 初始化采集图像的高度
        self.colletImgHeight = colletcImgHeight


    """
    函数名称：update
    参数说明：beforeImageNum:更新图片管理区前图片的数量
    函数返回：无
    功能概要：更新图片管理区
    """
    def update(self, beforeImageNum):
        # 获取父窗口的宽度
        grid_width = self.parent().parent().width()
        # 每个ImageLabel的宽度为self.colletImgWidth
        image_label_width = self.colletImgWidth 
        # 根据父窗口的宽度计算每行可以放置的图片标签数量
        self.columns = max(1, grid_width // image_label_width)
        # 根据列数计算需要的行数
        rows = beforeImageNum // self.columns + 1
        # 初始化图片索引
        idx = 0
        # 遍历每一行
        for row in range(rows):
            # 遍历每一列
            for col in range(self.columns):
                # 如果索引超出图片数量
                if idx >= len(self.images):
                    # 获取当前网格位置的项目
                    item = self.layout.itemAtPosition(row, col)
                    if item is not None:
                        # 如果有项目，获取其对应的小部件
                        widget = item.widget()
                        # 从布局中移除该小部件
                        self.layout.removeWidget(widget)
                        # 删除该小部件
                        widget.deleteLater()
                else:
                    # 如果索引未超出图片数量，将图片标签添加到布局中的指定位置
                    self.layout.addWidget(self.image_labels[idx], row, col)
                    # 更新索引
                    idx += 1


    """
    函数名称：resizeEvent
    参数说明：event:窗口大小改变事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理窗口大小改变事件
    """
    def resizeEvent(self, event: QResizeEvent):
        # 获取当前图片数量
        imgNum = len(self.images)
        # 调用 update 方法重新布局图片标签
        self.update(imgNum)
        # 调用父类的 resizeEvent 方法，确保继承的事件处理行为
        super().resizeEvent(event)


    """
    函数名称：add_image
    参数说明：image:图片名称（默认是点击保留按钮时的时间戳） pixmap:图片像素数据
    函数返回：无
    功能概要：向布局中添加一张图片
    """
    def add_image(self, image:str, pixmap:QPixmap):
        # 计算图片应该放置的行号和列号
        row = len(self.images) // self.columns
        col = len(self.images) % self.columns
        # 如果图片不在图片列表中，才进行添加操作
        if image not in self.images:
            # 创建图片标签对象，并指定删除回调函数为self._del_image
            image_label = ImageLabel(image, pixmap, self.colletImgWidth, self.colletImgHeight, delete_callback=self._del_image)
            # 将图片标签添加到布局中的指定位置
            self.layout.addWidget(image_label, row, col)
            # 将图片名称添加到图片列表中
            self.images.append(image)
            # 将图片标签对象添加到图片标签列表中
            self.image_labels.append(image_label)


    """
    函数名称：_del_image
    参数说明：image:要删除的图片名称
    函数返回：无
    功能概要：图片标签的删除回调函数
    """
    def _del_image(self, image):
        # 获取当前图片数量
        currentImgNum = len(self.images)
        # 调用del_image方法删除指定的图片标签
        self.del_image(image)
        # 更新布局，重新布局图片标签
        self.update(currentImgNum)


    """
    函数名称：del_image
    参数说明：image:要删除的图片名称
    函数返回：无
    功能概要：删除指定的图片标签
    """
    def del_image(self, image):
        # 尝试从图片列表中找到指定的图片
        try:
            # 获取指定图片的索引
            idx = self.images.index(image)
            # 删除图片标签列表中对应索引的图片标签
            del self.image_labels[idx]
            # 删除图片列表中对应索引的图片名称
            del self.images[idx]
        # 捕获可能发生的异常，并打印异常信息
        except Exception as e:
            print('An exception occurred', e)


    """
    函数名称：selectAllImg
    参数说明：无
    函数返回：无
    功能概要：选中所有图片标签
    """
    def selectAllImg(self):
        # 遍历布局中所有图片标签
        for image_label in self.image_labels:
            # 调用图片标签的checked方法选中图片标签
            image_label.checked()


    """
    函数名称：cancelSelectAllImg
    参数说明：无
    函数返回：无
    功能概要：取消选中所有图片标签
    """
    def cancelSelectAllImg(self):
        # 遍历布局中所有图片标签
        for image_label in self.image_labels:
            # 调用图片标签的unchecked方法取消选中图片标签
            image_label.unchecked()


    """
    函数名称：get_selected_images
    参数说明：无
    函数返回：所有选中的图片标签列表，包括图片名称和图片像素数据
    功能概要：获取所有选中的图片标签列表
    """
    def get_selected_images(self):
        # 初始化选中的图片列表
        selected_images = []
        # 遍历图片标签列表
        for image_label in self.image_labels:
            # 检查图片标签对应的复选框是否被选中
            if image_label.checkbox.isChecked():
                pixmap = image_label.pixmap.scaled(self.colletImgWidth, self.colletImgHeight, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                # 如果被选中，将图片名称和 QPixmap 对象添加到选中的图片列表中
                selected_images.append((image_label.image_name,pixmap))
        # 返回选中的图片列表
        return selected_images


    """
    函数名称：del_all_image
    参数说明：无
    函数返回：无
    功能概要：删除所有图片标签
    """
    def del_all_image(self):
        # 清空图片列表
        self.images.clear()
        # 清空图片标签列表
        self.image_labels.clear()
