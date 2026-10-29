from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QWheelEvent, QMouseEvent
from PySide6.QtCore import QPoint, Qt

"""
类名：CustomImageView
基类：QGraphicsView:Qt框架中用于显示和编辑2D图形和图片的类
功能：自定义可滚动视口
"""
class CustomImageView(QGraphicsView):

    """
    函数名称：__init__
    参数说明：frame:父控件
    函数返回：无
    功能概要：初始化自定义可视化视口
    """
    def __init__(self, frame):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super(CustomImageView, self).__init__(frame)
        # 启用拖动
        self.setDragMode(QGraphicsView.ScrollHandDrag)  


    """
    函数名称：wheelEvent
    参数说明：event:鼠标滚轮滚动事件，包含事件的相关信息
    函数返回：无
    功能概要：处理鼠标滚轮事件，实现视图的缩放功能
    """
    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.scene() is None:
            return
        # 如果场景中没有任何项目，直接返回，不进行缩放操作
        if len(self.scene().items()) == 0:
            return
        # 获取当前鼠标滚轮事件的位置
        curPoint = event.position()
        # 将视图坐标转换为场景坐标
        scenePos = self.mapToScene(QPoint(curPoint.x(), curPoint.y()))
        # 获取视口的宽度和高度
        viewWidth = self.viewport().width()
        viewHeight = self.viewport().height()
        # 计算水平和垂直缩放比例
        hScale = curPoint.x() / viewWidth
        vScale = curPoint.y() / viewHeight
        # 获取滚轮滚动的角度增量值
        wheelDeltaValue = event.angleDelta().y()
        # 获取当前的缩放比例因子
        scaleFactor = self.transform().m11()
        # 限制缩放比例的范围，如果超出范围则返回
        if (scaleFactor < 0.05 and wheelDeltaValue < 0) or (scaleFactor > 50 and wheelDeltaValue > 0):
            return
        # 根据滚轮滚动的方向进行缩放操作
        if wheelDeltaValue > 0:
            # 向上滚动，放大视图
            self.scale(1.2, 1.2)
        else:
            # 向下滚动，缩小视图
            self.scale(1.0 / 1.2, 1.0 / 1.2)
        # 获取缩放后的视图坐标
        viewPoint = self.transform().map(scenePos)
        # 根据缩放后的视图坐标调整滚动条的值
        self.horizontalScrollBar().setValue(int(viewPoint.x() - viewWidth * hScale))
        self.verticalScrollBar().setValue(int(viewPoint.y() - viewHeight * vScale))
        # 更新视图
        self.update()


    """
    函数名称：mousePressEvent
    参数说明：event:鼠标按下事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理鼠标按下事件
    """
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # 检查鼠标是否是左键按下
        if event.button() == Qt.LeftButton:
            # 如果是左键按下，将拖动模式设置为滚动手拖动模式
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        # 调用父类的mousePressEvent方法，确保继承的事件处理行为
        super(CustomImageView, self).mousePressEvent(event)


    """
    函数名称：mouseReleaseEvent
    参数说明：event:鼠标释放事件对象，包含事件的相关信息
    函数返回：无
    功能概要：处理鼠标释放事件
    """
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # 检查鼠标是否是左键释放
        if event.button() == Qt.LeftButton:
            # 如果是左键释放，将拖动模式设置为无拖动模式
            self.setDragMode(QGraphicsView.NoDrag)
        # 调用父类的mouseReleaseEvent方法，确保继承的事件处理行为
        super(CustomImageView, self).mouseReleaseEvent(event)
