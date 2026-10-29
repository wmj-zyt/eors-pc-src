from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from . customTooltip import ToolTip

"""
类名：HoverButton
基类：QPushButton:Qt框架中表示可点击按钮部件的类
功能：自定义按钮组件
"""
class HoverButton(QPushButton):

    """
    函数名称：__init__
    参数说明：normal_icon:按钮的默认图标 hover_icon:鼠标悬停在按钮上时显示的图标 text:按钮中显示的文本 parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义按钮组件
    """
    def __init__(self, normal_icon, hover_icon, text='', parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super(HoverButton, self).__init__(text, parent)
        # 初始化默认图标
        self.normal_icon = QIcon(normal_icon)
        # 初始化鼠标悬停时的图标
        self.hover_icon = QIcon(hover_icon)
        self.setIcon(self.normal_icon)
        # 初始化按钮的工具提示组件
        self._tooltip = ToolTip(parent=self)
        # 默认隐藏工具提示组件
        self._tooltip.hide()


    """
    函数名称：enterEvent
    参数说明：event:鼠标进入事件对象，包含事件相关信息
    函数返回：无
    功能概要：鼠标进入按钮时，设置按钮图标
    """
    def enterEvent(self, event):
        # 将按钮图标更换为悬停时的图标
        self.setIcon(self.hover_icon)
        # 调用父类的enterEvent方法
        super().enterEvent(event)


    """
    函数名称：leaveEvent
    参数说明：event:鼠标离开事件对象，包含事件相关信息
    函数返回：无
    功能概要：鼠标离开按钮时，设置按钮图标
    """
    def leaveEvent(self, event):
        # 将按钮图标恢复为默认图标
        self.setIcon(self.normal_icon)
        # 调用父类的leaveEvent方法
        super().leaveEvent(event)


    """
    函数名称：changeIcon
    参数说明：normal_icon:按钮默认图标 hover_icon:鼠标悬停在按钮上时显示的图标
    函数返回：无
    功能概要：更换按钮绑定的默认图标以及悬停图标
    """
    def changeIcon(self, normal_icon, hover_icon):
        # 设置按钮默认图标
        self.normal_icon = QIcon(normal_icon)
        # 设置按钮悬停图标
        self.hover_icon = QIcon(hover_icon)
