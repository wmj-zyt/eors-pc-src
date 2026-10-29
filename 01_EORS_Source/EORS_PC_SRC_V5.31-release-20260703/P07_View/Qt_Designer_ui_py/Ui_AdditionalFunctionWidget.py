# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AdditionalFunctionWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_AdditionFunctionWidget(object):
    def setupUi(self, AdditionFunctionWidget):
        if not AdditionFunctionWidget.objectName():
            AdditionFunctionWidget.setObjectName(u"AdditionFunctionWidget")
        AdditionFunctionWidget.resize(1050, 652)
        AdditionFunctionWidget.setStyleSheet(u"background-color: rgb(245, 249, 254);")
        self.verticalLayout = QVBoxLayout(AdditionFunctionWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(AdditionFunctionWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::pane{\n"
"left: 4px;\n"
"}\n"
"QTabBar::tab{\n"
"	left: 4px;\n"
"	font-size:14px;\n"
"	font-weight:bold;\n"
"	background-color: transparent;\n"
"	padding:12px 32px;\n"
"	border:none;\n"
"	border-radius: 6px;\n"
"	margin-right: 4px;\n"
"	margin-bottom:4px;\n"
"	margin-top:4px;\n"
"	\n"
"}\n"
"QTabBar::tab:hover{\n"
"	color:#475569;\n"
"}\n"
"QTabBar::tab:selected{\n"
"	background-color:#ab8bfa;\n"
"	color: #fff;\n"
"	\n"
"}")
        self.tabWidget_Data = QWidget()
        self.tabWidget_Data.setObjectName(u"tabWidget_Data")
        self.horizontalLayout_2 = QHBoxLayout(self.tabWidget_Data)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.tabWidget_Data)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.importDatasetPathLabel = QLabel(self.tabWidget_Data)
        self.importDatasetPathLabel.setObjectName(u"importDatasetPathLabel")

        self.horizontalLayout.addWidget(self.importDatasetPathLabel)

        self.selectDatasetButton = QPushButton(self.tabWidget_Data)
        self.selectDatasetButton.setObjectName(u"selectDatasetButton")
        self.selectDatasetButton.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"height:30px;\n"
"background-color: #5156be;\n"
"font-weight: bold;\n"
"color: #fff;\n"
"padding: 0 4px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #4549a2;\n"
"}")

        self.horizontalLayout.addWidget(self.selectDatasetButton)

        self.resizeDatasetButton = QPushButton(self.tabWidget_Data)
        self.resizeDatasetButton.setObjectName(u"resizeDatasetButton")
        self.resizeDatasetButton.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"height:30px;\n"
"background-color: #5156be;\n"
"font-weight: bold;\n"
"color: #fff;\n"
"padding: 0 4px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #4549a2;\n"
"}")

        self.horizontalLayout.addWidget(self.resizeDatasetButton)

        self.sendImageProgressBar = QProgressBar(self.tabWidget_Data)
        self.sendImageProgressBar.setObjectName(u"sendImageProgressBar")
        self.sendImageProgressBar.setStyleSheet(u"QProgressBar{ \n"
"font: 700 8pt \"Microsoft YaHei UI\";\n"
"color: #ff7b15; \n"
"text-align:center; \n"
"border:3px solid rgb(255, 255, 255);\n"
"border-radius: 10px; \n"
"background-color: rgba(215, 215, 215,100);\n"
"} \n"
"\n"
"QProgressBar:chunk{ \n"
"border-radius:0px; \n"
"background: rgba(119, 111, 252, 200);\n"
"border-radius: 7px;\n"
"}")
        self.sendImageProgressBar.setValue(24)

        self.horizontalLayout.addWidget(self.sendImageProgressBar)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.label_2 = QLabel(self.tabWidget_Data)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 5)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tabWidget_Data, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(AdditionFunctionWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AdditionFunctionWidget)
    # setupUi

    def retranslateUi(self, AdditionFunctionWidget):
        AdditionFunctionWidget.setWindowTitle(QCoreApplication.translate("AdditionFunctionWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("AdditionFunctionWidget", u"\u6570\u636e\u96c6\u6807\u51c6\u5316", None))
        self.importDatasetPathLabel.setText(QCoreApplication.translate("AdditionFunctionWidget", u"\u6570\u636e\u96c6\u8def\u5f84:", None))
        self.selectDatasetButton.setText(QCoreApplication.translate("AdditionFunctionWidget", u"\u9009\u62e9\u6570\u636e\u96c6", None))
        self.resizeDatasetButton.setText(QCoreApplication.translate("AdditionFunctionWidget", u"\u6807\u51c6\u5316\u6570\u636e\u96c6\uff08160 X 150\uff09", None))
        self.label_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget_Data), QCoreApplication.translate("AdditionFunctionWidget", u"\u56fe\u50cf\u9884\u5904\u7406", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("AdditionFunctionWidget", u"\u656c\u8bf7\u671f\u5f85", None))
    # retranslateUi

