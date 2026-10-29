from PySide6.QtWidgets import QHeaderView, QStyleOptionButton, QStyle
from PySide6.QtCore import Signal, Qt, QRect
from PySide6.QtGui import QPainter, QMouseEvent

# 所有行复选框列表
all_header_checkbox =[]

"""
类名：CheckBoxHeader
基类：QHeaderView:Qt表格组件的表头类
功能：自定义带复选框的表头
"""
class CheckBoxHeader(QHeaderView):
    # select_all_clicked信号在全选复选框被点击时发射
    select_all_clicked = Signal(bool)
    # 列头复选框的水平偏移量
    _x_offset = 5
    # 列头复选框的垂直偏移量
    _y_offset = 0
    # 列头复选框的宽度
    _width = 20
    # 列头复选框的高度
    _height = 20

    """
    函数名称：__init__
    参数说明：orientation:表头的方向，默认为水平方向  parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义表头
    """
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        # 调用父类的构造函数初始化复选框头部
        super(CheckBoxHeader, self).__init__(orientation, parent)
        # 初始化表头复选框状态为关闭
        self.isOn = False
        
        self.select_all_clicked.connect(CheckBoxHeader.change_state)


    """
    函数名称：paintSection
    参数说明：painter:绘画设备  rect:表头的矩形区域  logicalIndex:表头的逻辑索引
    函数返回：无
    功能概要：重写绘制表头的方法，在表头上绘制复选框
    """
    def paintSection(self, painter:QPainter, rect:QRect, logicalIndex:int):
        # 保存当前绘画状态
        painter.save()
        # 调用父类的paintSection方法绘制默认表头
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        # 恢复之前保存的绘画状态
        painter.restore()
        # 计算复选框的垂直偏移量
        self._y_offset = int((rect.height() - self._width) / 2.)
        # 如果是第一个表头
        if logicalIndex == 0:
            # 创建QStyleOptionButton对象来设置复选框的绘制选项
            option = QStyleOptionButton()
            # 设置复选框的绘制区域
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            # 设置复选框的状态
            option.state = QStyle.State_Enabled | QStyle.State_Active
            # 根据复选框的状态绘制复选框
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            # 绘制表头
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)


    """
    函数名称：mousePressEvent
    参数说明：event:鼠标点击事件对象，包含事件的相关信息
    函数返回：无
    功能概要：重写鼠标点击事件处理方法，处理点击行表头复选框的行为
    """
    def mousePressEvent(self, event:QMouseEvent):
        # 获取鼠标点击位置对应的表头索引
        index = self.logicalIndexAt(event.pos())
        # 如果是第一个表头
        if 0 == index:
            # 获取第一个表头的位置
            x = self.sectionPosition(index)
            # 判断鼠标点击位置是否在复选框的范围内
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                # 切换复选框状态
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                # 当用户点击了表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)
                # 更新第一个表头，以便重新绘制复选框
                self.updateSection(0)
        # 调用父类的鼠标点击事件处理方法
        super(CheckBoxHeader, self).mousePressEvent(event)


    """
    函数名称：change_state
    参数说明：isOn: 表头复选框状态 True=勾选，False=未勾选
    函数返回：无
    功能概要：自定义信号 select_all_clicked 的槽方法
    """
    def change_state(isOn):
        # 如果表头复选框为勾选状态
        if isOn:
            # 将所有的复选框都设为勾选状态
            for i in all_header_checkbox:
                i.setCheckState(Qt.Checked)
        else:
            # 将所有的复选框都设为未勾选状态
            for i in all_header_checkbox:
                i.setCheckState(Qt.Unchecked)
