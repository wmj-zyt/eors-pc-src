#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
帮助文档对话框模块
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QSize, QUrl
import sys
import os
# 标准输出流重定向
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
# 标准错误流重定向
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("帮助文档")
        self.setFixedSize(QSize(1000, 700))
        
        # 创建垂直布局
        layout = QVBoxLayout()
        
        # 创建Web视图用于显示HTML内容
        self.web_view = QWebEngineView()
        
        # 添加关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        
        # 将控件添加到布局中
        layout.addWidget(self.web_view)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        # 加载HTML内容
        self.load_help_content()
    
    def load_help_content(self):
        if hasattr(sys, '_MEIPASS'):
            self.projectRoot = sys._MEIPASS
        else:
            self.projectRoot = os.path.abspath(os.getcwd()) 
            print(f"help:{self.projectRoot}")

        if hasattr(sys, 'frozen'):
            # 打包环境下，使用sys._MEIPASS获取临时解压目录
            base_path = sys._MEIPASS
            html_path = os.path.join(base_path, "P02_Resource/HelpDoc.html")
        else:
            # 开发环境下，使用原来的路径
            html_path = os.path.join(self.projectRoot, "P02_Resource/HelpDoc.html") 
        # 获取HTML文件路径（直接位于 P02_Resource 目录下）
        # html_path = os.path.join(
        #     os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),  # 4次 dirname
        #     "P02_Resource",
        #     "HelpDoc.html"
        # )
        print(f"HTML路径: {html_path}")
        # self.projectRoot = os.path.abspath(os.getcwd()) 
        # print(f"projectRoot: {self.projectRoot}")
        
        # 检查文件是否存在
        if os.path.exists(html_path):
            self.web_view.load(QUrl.fromLocalFile(html_path))
        else:
            self.web_view.setHtml("<h1>错误</h1><p>找不到帮助文档文件。</p>")