# coding:utf-8
from PySide6.QtCore import QPropertyAnimation,Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QFrame, QGraphicsDropShadowEffect,
                                QHBoxLayout, QLabel)


"""
类名：ToolTip
基类：QFrame:Qt中用来创建有边框的窗口或者其他组件的容器类
功能：自定义工具提示组件
"""
class ToolTip(QFrame):

    """
    函数名称：__init__
    参数说明：text:提示组件内容  parent:父控件（可选），默认值为None，表示没有父控件
    函数返回：无
    功能概要：初始化自定义工具提示组件
    """
    def __init__(self, text='', parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__(parent=parent)
        # 初始化文本内容
        self.__text = text
        # 创建水平布局
        self.hBox = QHBoxLayout(self)
        # 创建显示文本的标签
        self.label = QLabel(text, self)
        # 创建属性动画，用于窗口透明度动画效果
        self.ani = QPropertyAnimation(self, b'windowOpacity', self)
        # 在水平布局中添加标签组件
        self.hBox.addWidget(self.label)
        # 水平布局设置内容边距
        self.hBox.setContentsMargins(10, 6, 10, 6)
        # 创建一个 QGraphicsDropShadowEffect对象，添加阴影效果
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        # 设置其模糊半径
        self.shadowEffect.setBlurRadius(32)
        # 设置颜色
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        # 设置偏移量
        self.shadowEffect.setOffset(0, 5)
        # 将阴影效果应用到当前窗口
        self.setGraphicsEffect(self.shadowEffect)
        # 设置样式属性，启用自定义样式
        self.setAttribute(Qt.WA_StyledBackground)
        # 调用私有方法设置样式表
        self.__setQss()


    """
    函数名称：text
    参数说明：无
    函数返回：返回自定义工具提示内容
    功能概要：获取自定义工具提示内容
    """
    def text(self):
        return self.__text


    """
    函数名称：setText
    参数说明：text: 要显示的文本内容
    函数返回：无
    功能概要：设置工具提示上显示的文本内容
    """
    def setText(self, text: str):
        # 设置私有变量中的文本内容
        self.__text = text
        # 设置标签显示的文本内容
        self.label.setText(text)
        # 调整标签的尺寸以适应新的文本内容
        self.label.adjustSize()
        # 调整工具提示窗口的尺寸以适应新的文本内容
        self.adjustSize()


    """
    函数名称：__setQss
    参数说明：无
    函数返回：无
    功能概要：设置工具提示窗口和标签的样式表
    """
    def __setQss(self):
        # 设置工具提示窗口的样式表
        self.setStyleSheet(u"ToolTip {"
                                "border: none;"
                                "border-radius: 5px;"
                                "background-color: #333333;"
                            "}"

                            "QLabel {"
                                "background-color: transparent;"
                                "font: 12px 'Segoe UI', 'Microsoft YaHei';"
                                "color: #fff;"
                            "}")
        # 调整标签的尺寸，以适应样式表的设置
        self.label.adjustSize()
        # 调整工具提示窗口的尺寸，以适应样式表的设置
        self.adjustSize()
