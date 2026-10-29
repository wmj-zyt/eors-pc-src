# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataAcuisitionWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QTabWidget, QToolBox, QVBoxLayout, QWidget)
from . import image_rc

class Ui_DataAcuisitionWidget(object):
    def setupUi(self, DataAcuisitionWidget):
        if not DataAcuisitionWidget.objectName():
            DataAcuisitionWidget.setObjectName(u"DataAcuisitionWidget")
        DataAcuisitionWidget.resize(1042, 660)
        DataAcuisitionWidget.setStyleSheet(u"")
        self.verticalLayout_9 = QVBoxLayout(DataAcuisitionWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.tabWidget = QTabWidget(DataAcuisitionWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"    margin-bottom: 0px;\n"
"}\n"
"QTabBar::tab {\n"
"    min-width: 90px;\n"
"    height: 32px;\n"
"    padding: 4px 12px;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"    font-size: 15px;\n"
"    color: #6b7280;\n"
"    background-color: rgba(255, 255, 255, 0.6);\n"
"    border-radius: 6px 6px 0 0;\n"
"    margin: 0 2px;\n"
"    transition: all 0.2s ease;\n"
"}\n"
"QTabBar::tab:hover {\n"
"    background-color: rgba(255, 255, 255, 0.8);\n"
"    color: #9265F4;\n"
"    transform: translateY(-1px);\n"
"}\n"
"QTabBar::tab:selected {\n"
"    background-color: rgba(255, 255, 255, 0.95);\n"
"    color: #9265F4;\n"
"    border-bottom: 3px solid #9265F4;\n"
"}\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    padding-top: 0px;\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.tab)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QFrame{\n"
"background-color: rgb(238, 242, 255);\n"
"padding:4px;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toolBox = QToolBox(self.frame)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setEnabled(True)
        self.toolBox.setStyleSheet(u"QToolBox::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border-radius: 5px;\n"
"    color: darkgray;\n"
"	font-weight: 600;\n"
"}\n"
"\n"
"QToolBox::tab:selected { /* italicize selected tabs */\n"
"    font: italic;\n"
"    color: white;\n"
"	font-weight: 600;\n"
"}")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 467, 529))
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.page)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_7)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.frame_14 = QFrame(self.frame_7)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.serialButton = QPushButton(self.frame_14)
        self.serialButton.setObjectName(u"serialButton")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serialButton.sizePolicy().hasHeightForWidth())
        self.serialButton.setSizePolicy(sizePolicy)
        self.serialButton.setMinimumSize(QSize(80, 0))
        self.serialButton.setStyleSheet(u"QPushButton{\n"
"            border: none;\n"
"            	background-color: #b5eadb;\n"
"            	color:  #0abb87;\n"
"            	font-weight: 600;\n"
"            	padding: 8px 12px;\n"
"            	border-radius: 4px;\n"
"            }\n"
"            QPushButton:hover{\n"
"            	color: #fff;\n"
"            	background-color: #0abb87;\n"
"            \n"
"            }")

        self.horizontalLayout_5.addWidget(self.serialButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.uartStateLabel = QLabel(self.frame_14)
        self.uartStateLabel.setObjectName(u"uartStateLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.uartStateLabel.sizePolicy().hasHeightForWidth())
        self.uartStateLabel.setSizePolicy(sizePolicy1)
        self.uartStateLabel.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_5.addWidget(self.uartStateLabel)


        self.verticalLayout.addWidget(self.frame_14)

        self.frame_18 = QFrame(self.frame_7)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_60 = QLabel(self.frame_18)
        self.label_60.setObjectName(u"label_60")
        font = QFont()
        font.setBold(True)
        self.label_60.setFont(font)
        self.label_60.setStyleSheet(u"font-weight:600;\n"
"padding:4px;")

        self.horizontalLayout_12.addWidget(self.label_60)

        self.horizontalSpacer_36 = QSpacerItem(203, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_36)

        self.selectPicBtn = QPushButton(self.frame_18)
        self.selectPicBtn.setObjectName(u"selectPicBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.selectPicBtn.sizePolicy().hasHeightForWidth())
        self.selectPicBtn.setSizePolicy(sizePolicy2)
        self.selectPicBtn.setMinimumSize(QSize(80, 0))
        self.selectPicBtn.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"height:30px;\n"
"background-color: #5156be;\n"
"font-weight: bold;\n"
"color: #fff;\n"
"padding: 0 4px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #4549a2;\n"
"}\n"
"/* \ud83d\udd34 \u4e0d\u53ef\u70b9\u51fb\uff08\u7981\u7528\uff09\u72b6\u6001 */\n"
"QPushButton:disabled {\n"
"    background-color: #b0b0b0;   /* \u7070\u8272\u80cc\u666f */\n"
"    color: #666666;              /* \u7070\u8272\u6587\u5b57 */\n"
"}")

        self.horizontalLayout_12.addWidget(self.selectPicBtn)

        self.sendPicBtn = QPushButton(self.frame_18)
        self.sendPicBtn.setObjectName(u"sendPicBtn")
        sizePolicy2.setHeightForWidth(self.sendPicBtn.sizePolicy().hasHeightForWidth())
        self.sendPicBtn.setSizePolicy(sizePolicy2)
        self.sendPicBtn.setMinimumSize(QSize(80, 0))
        self.sendPicBtn.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"height:30px;\n"
"background-color: #5156be;\n"
"font-weight: bold;\n"
"color: #fff;\n"
"padding: 0 4px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #4549a2;\n"
"}\n"
"/* \ud83d\udd34 \u4e0d\u53ef\u70b9\u51fb\uff08\u7981\u7528\uff09\u72b6\u6001 */\n"
"QPushButton:disabled {\n"
"    background-color: #b0b0b0;   /* \u7070\u8272\u80cc\u666f */\n"
"    color: #666666;              /* \u7070\u8272\u6587\u5b57 */\n"
"}")

        self.horizontalLayout_12.addWidget(self.sendPicBtn)


        self.verticalLayout.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.frame_7)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_58 = QLabel(self.frame_19)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setMinimumSize(QSize(74, 32))
        self.label_58.setMaximumSize(QSize(74, 32))
        self.label_58.setStyleSheet(u"font-weight:600;\n"
"padding:4px;")

        self.horizontalLayout_13.addWidget(self.label_58)

        self.selectModelComboBox = QComboBox(self.frame_19)
        self.selectModelComboBox.setObjectName(u"selectModelComboBox")
        self.selectModelComboBox.setMinimumSize(QSize(300, 0))
        self.selectModelComboBox.setStyleSheet(u"QComboBox {\n"
"        background-color: rgba(255,255,255,90);\n"
"		color: rgba(0, 0, 0, 200);\n"
"        border: 1px solid lightgray;\n"
"        border-radius: 4px;\n"
"		padding: 4px;\n"
"        }\n"
"QComboBox:on {\n"
"         border: 1px solid #63acfb;\n"
"        }\n"
"\n"
"QComboBox::drop-down {\n"
"       width: 22px;\n"
"       border-left: 1px solid lightgray;\n"
"       border-top-right-radius: 8px;\n"
"       border-bottom-right-radius: 8px;\n"
"        }\n"
"        \n"
"QComboBox::drop-down:on {\n"
"            border-left: 1px solid #63acfb;\n"
"        }\n"
"\n"
"QComboBox::down-arrow {\n"
"            width: 16px;\n"
"            height: 16px;\n"
"            image: url(:/img/02-Image/box_down.png);\n"
"        }\n"
"\n"
"        QComboBox::down-arrow:on {\n"
"            image: url(:/img/02-Image/box_up.png);\n"
"        }\n"
"\n"
"        QComboBox QAbstractItemView {\n"
"            border: none;\n"
"            outline: none;\n"
"			padding: 10px;\n"
"            background-color: rgb"
                        "(223, 188, 220);\n"
"        }\n"
"\n"
"\n"
"        QComboBox QScrollBar:vertical {\n"
"            width: 2px;\n"
"           background-color: rgba(255,255,255,150);\n"
"        }\n"
"\n"
"        QComboBox QScrollBar::handle:vertical {\n"
"            background-color: rgba(255,255,255,90);\n"
"        }")

        self.horizontalLayout_13.addWidget(self.selectModelComboBox)

        self.horizontalSpacer_35 = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_35)


        self.verticalLayout.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.frame_7)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_59 = QLabel(self.frame_20)
        self.label_59.setObjectName(u"label_59")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_59.sizePolicy().hasHeightForWidth())
        self.label_59.setSizePolicy(sizePolicy3)
        self.label_59.setMinimumSize(QSize(90, 0))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_59.setFont(font1)

        self.horizontalLayout_16.addWidget(self.label_59)

        self.uart_preLeibie = QLabel(self.frame_20)
        self.uart_preLeibie.setObjectName(u"uart_preLeibie")
        sizePolicy3.setHeightForWidth(self.uart_preLeibie.sizePolicy().hasHeightForWidth())
        self.uart_preLeibie.setSizePolicy(sizePolicy3)
        self.uart_preLeibie.setMinimumSize(QSize(110, 0))
        self.uart_preLeibie.setMaximumSize(QSize(30, 16777215))
        self.uart_preLeibie.setFont(font1)

        self.horizontalLayout_16.addWidget(self.uart_preLeibie)

        self.uart_preData = QLabel(self.frame_20)
        self.uart_preData.setObjectName(u"uart_preData")
        font2 = QFont()
        font2.setPointSize(14)
        self.uart_preData.setFont(font2)

        self.horizontalLayout_16.addWidget(self.uart_preData)

        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(1, 1)
        self.horizontalLayout_16.setStretch(2, 1)

        self.verticalLayout.addWidget(self.frame_20)


        self.verticalLayout_5.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.page)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_8)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.frame_8)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_11)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.delCollectedImgButton = QPushButton(self.frame_11)
        self.delCollectedImgButton.setObjectName(u"delCollectedImgButton")
        self.delCollectedImgButton.setStyleSheet(u"QPushButton{\n"
"\n"
"background-origin:content;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"border-radius: 5px;\n"
"border: 10px;\n"
"border-color: rgb(255, 247, 249);\n"
"}\n"
"QPushButton:hover{\n"
"background-image:url(:/img/images/clearTextEdit.png);\n"
"}")

        self.horizontalLayout_8.addWidget(self.delCollectedImgButton)


        self.verticalLayout_6.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.frame_8)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.collectImageLabel = QLabel(self.frame_12)
        self.collectImageLabel.setObjectName(u"collectImageLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.collectImageLabel.sizePolicy().hasHeightForWidth())
        self.collectImageLabel.setSizePolicy(sizePolicy4)
        self.collectImageLabel.setMinimumSize(QSize(0, 244))

        self.gridLayout.addWidget(self.collectImageLabel, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.frame_12)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_10)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.serialData = QLabel(self.frame_10)
        self.serialData.setObjectName(u"serialData")

        self.horizontalLayout_7.addWidget(self.serialData)

        self.clearSerialDataButton = QPushButton(self.frame_10)
        self.clearSerialDataButton.setObjectName(u"clearSerialDataButton")
        self.clearSerialDataButton.setStyleSheet(u"QPushButton:hover{\n"
"	text-decoration: underline;\n"
"	background-color: transparent;\n"
"}")

        self.horizontalLayout_7.addWidget(self.clearSerialDataButton)

        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_6.addWidget(self.frame_10)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 5)
        self.verticalLayout_6.setStretch(2, 1)

        self.verticalLayout_5.addWidget(self.frame_8)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 4)
        icon = QIcon()
        icon.addFile(u":/img/images/\u62cd\u7167.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page, icon, u"\u62cd\u7167\u91c7\u96c6")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 484, 513))
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.page_2)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.loadVideoButton = QPushButton(self.frame_13)
        self.loadVideoButton.setObjectName(u"loadVideoButton")
        self.loadVideoButton.setStyleSheet(u"QPushButton{\n"
"	border: 1px solid #6a6e92;\n"
"	background-color: #6a6e92;\n"
"	padding: 8px 12px;\n"
"	color: #fff;\n"
"	border-radius: 4px;\n"
"	font-weight: 600;\n"
"	font-size: 12px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #4c5074;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/img/images/\u5bfc\u5165\u89c6\u9891.png", QSize(), QIcon.Normal, QIcon.Off)
        self.loadVideoButton.setIcon(icon1)

        self.horizontalLayout_9.addWidget(self.loadVideoButton)

        self.deleteVideoButton = QPushButton(self.frame_13)
        self.deleteVideoButton.setObjectName(u"deleteVideoButton")
        icon2 = QIcon()
        icon2.addFile(u":/img/images/\u5220\u9664\u89c6\u9891.png", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteVideoButton.setIcon(icon2)

        self.horizontalLayout_9.addWidget(self.deleteVideoButton)

        self.videoName = QLabel(self.frame_13)
        self.videoName.setObjectName(u"videoName")

        self.horizontalLayout_9.addWidget(self.videoName)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)

        self.decomposeVideoButton = QPushButton(self.frame_13)
        self.decomposeVideoButton.setObjectName(u"decomposeVideoButton")
        self.decomposeVideoButton.setEnabled(False)
        self.decomposeVideoButton.setStyleSheet(u"QPushButton{\n"
"	border: 1px solid #4f46e5;\n"
"	background-color: #4f46e5;\n"
"	padding: 8px 12px;\n"
"	color: #fff;\n"
"	border-radius: 4px;\n"
"	font-weight: 600;\n"
"	font-size: 12px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #4338ca;\n"
"}\n"
"QPushButton:disabled\n"
"{\n"
"	border:1px solid #9ea1b8;\n"
"    background-color:#9ea1b8;/*\u6539\u53d8\u80cc\u666f\u8272*/\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/img/images/\u9010\u5e27\u5206\u89e3.png", QSize(), QIcon.Normal, QIcon.Off)
        self.decomposeVideoButton.setIcon(icon3)

        self.horizontalLayout_9.addWidget(self.decomposeVideoButton)


        self.verticalLayout_7.addWidget(self.frame_13)

        self.videoFrame = QFrame(self.page_2)
        self.videoFrame.setObjectName(u"videoFrame")
        self.videoFrame.setFrameShape(QFrame.StyledPanel)
        self.videoFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.videoFrame)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.videoHorizontalLayout = QHBoxLayout()
        self.videoHorizontalLayout.setObjectName(u"videoHorizontalLayout")

        self.horizontalLayout_15.addLayout(self.videoHorizontalLayout)


        self.verticalLayout_7.addWidget(self.videoFrame)

        self.frame_15 = QFrame(self.page_2)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.playVideoButton = QPushButton(self.frame_15)
        self.playVideoButton.setObjectName(u"playVideoButton")
        icon4 = QIcon()
        icon4.addFile(u":/img/images/begin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.playVideoButton.setIcon(icon4)

        self.horizontalLayout_10.addWidget(self.playVideoButton)

        self.videoStartTime = QLabel(self.frame_15)
        self.videoStartTime.setObjectName(u"videoStartTime")

        self.horizontalLayout_10.addWidget(self.videoStartTime)

        self.videoSlider = QSlider(self.frame_15)
        self.videoSlider.setObjectName(u"videoSlider")
        self.videoSlider.setStyleSheet(u"/* \u6c34\u5e73\u6ed1\u5757\u57fa\u7840\u6837\u5f0f */\n"
"QSlider::horizontal {\n"
"    height: 10px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u8f68\u9053 */\n"
"QSlider::groove:horizontal {\n"
"    height: 4px;\n"
"    background-color: #e1d9fe;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u5df2\u586b\u5145\u90e8\u5206 */\n"
"QSlider::sub-page:horizontal {\n"
"    height: 4px;\n"
"    background-color: #9265F4;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u672a\u586b\u5145\u90e8\u5206 */\n"
"QSlider::add-page:horizontal {\n"
"    height: 4px;\n"
"    background-color: #e1d9fe;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u624b\u67c4 */\n"
"QSlider::handle:horizontal {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #9265F4;\n"
"    border-radius: 8px;\n"
"    margin: -6px 0;\n"
"    transition: all 0.2s ease;\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u624b"
                        "\u67c4\u60ac\u505c\u72b6\u6001 */\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: #f0e6ff;\n"
"    border-color: #7942F0;\n"
"    transform: scale(1.1);\n"
"}\n"
"\n"
"/* \u6c34\u5e73\u6ed1\u5757\u624b\u67c4\u6309\u4e0b\u72b6\u6001 */\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: #9265F4;\n"
"    border-color: #9265F4;\n"
"    transform: scale(1.2);\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u57fa\u7840\u6837\u5f0f\uff08\u5982\u679c\u9700\u8981\uff09 */\n"
"QSlider::vertical {\n"
"    width: 10px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u8f68\u9053 */\n"
"QSlider::groove:vertical {\n"
"    width: 4px;\n"
"    background-color: #e1d9fe;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u5df2\u586b\u5145\u90e8\u5206 */\n"
"QSlider::sub-page:vertical {\n"
"    width: 4px;\n"
"    background-color: #9265F4;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u672a\u586b\u5145\u90e8\u5206 */\n"
"QSlider::add-page:ver"
                        "tical {\n"
"    width: 4px;\n"
"    background-color: #e1d9fe;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u624b\u67c4 */\n"
"QSlider::handle:vertical {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #9265F4;\n"
"    border-radius: 8px;\n"
"    margin: 0 -6px;\n"
"    transition: all 0.2s ease;\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u624b\u67c4\u60ac\u505c\u72b6\u6001 */\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: #f0e6ff;\n"
"    border-color: #7942F0;\n"
"    transform: scale(1.1);\n"
"}\n"
"\n"
"/* \u5782\u76f4\u6ed1\u5757\u624b\u67c4\u6309\u4e0b\u72b6\u6001 */\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: #9265F4;\n"
"    border-color: #9265F4;\n"
"    transform: scale(1.2);\n"
"}")
        self.videoSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.videoSlider)

        self.videoEndTime = QLabel(self.frame_15)
        self.videoEndTime.setObjectName(u"videoEndTime")

        self.horizontalLayout_10.addWidget(self.videoEndTime)


        self.verticalLayout_7.addWidget(self.frame_15)

        self.verticalLayout_7.setStretch(1, 1)
        icon5 = QIcon()
        icon5.addFile(u":/img/images/\u89c6\u9891.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page_2, icon5, u"\u89c6\u9891\u89e3\u6790")

        self.verticalLayout_3.addWidget(self.toolBox)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.tab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"QFrame{\n"
"background-color: rgb(238, 242, 255);\n"
"padding:0px;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy5)
        self.frame_3.setMinimumSize(QSize(10, 40))
        self.frame_3.setStyleSheet(u"background-color: rgb(238, 242, 255);\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #9370DB , stop:1 #9b88f0);\n"
"	border:none;\n"
"    border-radius: 5px;\n"
"	padding: 4px;\n"
"    color: white;\n"
"	text-align:left;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/img/images/\u56fe\u7247\u7ba1\u7406.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon6)

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.batchDeleteButton = QPushButton(self.frame_4)
        self.batchDeleteButton.setObjectName(u"batchDeleteButton")
        self.batchDeleteButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: #eeeeee;\n"
"	color: #2c323f;\n"
"	padding: 8px 12px;\n"
"	font-weight: 600;\n"
"	border-radius: 4px;\n"
"	border: 1px solid #e3e7ee;\n"
"}\n"
"QPushButton:hover{\n"
"	border: 1px solid #2c323f;\n"
"	background-color: #d3d4d5;\n"
"}")

        self.horizontalLayout_2.addWidget(self.batchDeleteButton)

        self.batchSaveButton = QPushButton(self.frame_4)
        self.batchSaveButton.setObjectName(u"batchSaveButton")
        self.batchSaveButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: #c3c4ff;\n"
"	color: #696cff;\n"
"	padding: 8px 12px;\n"
"	font-weight: 600;\n"
"	border-radius: 4px;\n"
"	border: 1px solid #e3e7ee;\n"
"}\n"
"QPushButton:hover{\n"
"	border: 1px solid #696cff;\n"
"}")

        self.horizontalLayout_2.addWidget(self.batchSaveButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.selectAllImgCheckBox = QCheckBox(self.frame_4)
        self.selectAllImgCheckBox.setObjectName(u"selectAllImgCheckBox")
        self.selectAllImgCheckBox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.selectAllImgCheckBox)


        self.verticalLayout_4.addWidget(self.frame_4)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"QFrame{\n"
"background-color: rgb(238, 242, 255);\n"
"border-radius:5px;\n"
"padding:4px;\n"
"}")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.savedImgsArea = QScrollArea(self.frame_6)
        self.savedImgsArea.setObjectName(u"savedImgsArea")
        self.savedImgsArea.setStyleSheet(u"background-color: transparent;")
        self.savedImgsArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 491, 454))
        self.horizontalLayout_14 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.showImgHorizontalLayout = QHBoxLayout()
        self.showImgHorizontalLayout.setObjectName(u"showImgHorizontalLayout")

        self.horizontalLayout_14.addLayout(self.showImgHorizontalLayout)

        self.savedImgsArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.savedImgsArea)

        self.imgNum = QLabel(self.frame_6)
        self.imgNum.setObjectName(u"imgNum")

        self.verticalLayout_2.addWidget(self.imgNum)


        self.verticalLayout_4.addWidget(self.frame_6)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.imgPath = QLabel(self.frame_5)
        self.imgPath.setObjectName(u"imgPath")

        self.horizontalLayout_4.addWidget(self.imgPath)

        self.horizontalSpacer = QSpacerItem(450, 18, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.clearImgManageAreaButton = QPushButton(self.frame_5)
        self.clearImgManageAreaButton.setObjectName(u"clearImgManageAreaButton")
        self.clearImgManageAreaButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-weight: 600;\n"
"	font-size: 13px;\n"
"	padding: 4px 8px;\n"
"}\n"
"QPushButton:hover{\n"
"	text-decoration: underline;\n"
"}")

        self.horizontalLayout_4.addWidget(self.clearImgManageAreaButton)


        self.verticalLayout_4.addWidget(self.frame_5)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 30)
        self.verticalLayout_4.setStretch(3, 1)

        self.horizontalLayout.addWidget(self.frame_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_8 = QVBoxLayout(self.tab_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_16 = QFrame(self.tab_2)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"QPushButton{\n"
"	background-color: #fff;\n"
"	font-size: 15px;\n"
"	padding: 10px 20px;\n"
"	border: 1px solid #eef0f4;\n"
"	border-radius: 4px;\n"
"	color: #5a6288;\n"
"	width: 90px;\n"
"}\n"
"QPushButton:hover{\n"
"	border: 1px solid #6a7bff;\n"
"}\n"
"QPushButton:focus, QPushButton:checked{\n"
"	border: 1px solid #6a7bff;\n"
"	color: #6a7bff;\n"
"	background: #eaf5ff;\n"
"}\n"
"QFrame#frame_79{\n"
"	border-bottom: 1px solid #eef0f4;\n"
"}")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.pushButton_11 = QPushButton(self.frame_16)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_11.addWidget(self.pushButton_11)

        self.pushButton_14 = QPushButton(self.frame_16)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.horizontalLayout_11.addWidget(self.pushButton_14)

        self.pushButton_15 = QPushButton(self.frame_16)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.horizontalLayout_11.addWidget(self.pushButton_15)

        self.pushButton_16 = QPushButton(self.frame_16)
        self.pushButton_16.setObjectName(u"pushButton_16")

        self.horizontalLayout_11.addWidget(self.pushButton_16)

        self.pushButton_17 = QPushButton(self.frame_16)
        self.pushButton_17.setObjectName(u"pushButton_17")

        self.horizontalLayout_11.addWidget(self.pushButton_17)


        self.verticalLayout_8.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.tab_2)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)

        self.verticalLayout_8.addWidget(self.frame_17)

        self.verticalLayout_8.setStretch(1, 1)
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_9.addWidget(self.tabWidget)


        self.retranslateUi(DataAcuisitionWidget)

        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DataAcuisitionWidget)
    # setupUi

    def retranslateUi(self, DataAcuisitionWidget):
        DataAcuisitionWidget.setWindowTitle(QCoreApplication.translate("DataAcuisitionWidget", u"Form", None))
        self.serialButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u8fde\u63a5GEC", None))
        self.uartStateLabel.setText("")
        self.label_60.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u56fe\u7247\u4e0b\u53d1\uff1a", None))
        self.selectPicBtn.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u9009\u62e9\u56fe\u7247", None))
        self.sendPicBtn.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u53d1\u9001\u56fe\u7247", None))
        self.label_58.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.label_59.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u9884\u6d4b\u7ed3\u679c\uff1a", None))
        self.uart_preLeibie.setText("")
        self.uart_preData.setText("")
        self.label_4.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u91c7\u96c6\u56fe\u50cf\u663e\u793a(\u5bbd\uff1a160\uff0c \u9ad8\uff1a150)", None))
        self.delCollectedImgButton.setText("")
        self.collectImageLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u4e32\u53e3\u63a5\u6536\u6570\u636e\uff1a", None))
        self.serialData.setText("")
        self.clearSerialDataButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6e05\u7a7a", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("DataAcuisitionWidget", u"\u62cd\u7167\u91c7\u96c6", None))
        self.loadVideoButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u5bfc\u5165\u89c6\u9891", None))
        self.deleteVideoButton.setText("")
        self.videoName.setText("")
        self.decomposeVideoButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u9010\u5e27\u5206\u89e3", None))
        self.playVideoButton.setText("")
        self.videoStartTime.setText(QCoreApplication.translate("DataAcuisitionWidget", u"00:00", None))
        self.videoEndTime.setText(QCoreApplication.translate("DataAcuisitionWidget", u"00:00", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("DataAcuisitionWidget", u"\u89c6\u9891\u89e3\u6790", None))
        self.pushButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u56fe\u7247\u7ba1\u7406", None))
        self.batchDeleteButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u5220\u9664", None))
        self.batchSaveButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u4fdd\u5b58", None))
        self.selectAllImgCheckBox.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u5168\u9009", None))
        self.imgNum.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u56fe\u7247\u6570\u91cf\uff1a", None))
        self.imgPath.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u56fe\u50cf\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.clearImgManageAreaButton.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6e05\u7a7a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("DataAcuisitionWidget", u"\u91c7\u96c6\u56fe\u7247", None))
        self.pushButton_11.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u65cb\u8f6c", None))
        self.pushButton_14.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u88c1\u526a", None))
        self.pushButton_15.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u4eff\u5c04\u53d8\u6362", None))
        self.pushButton_16.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u989c\u8272\u589e\u5f3a", None))
        self.pushButton_17.setText(QCoreApplication.translate("DataAcuisitionWidget", u"\u6279\u91cf\u6a21\u7cca\u589e\u5f3a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("DataAcuisitionWidget", u"\u6570\u636e\u589e\u5f3a\uff08\u9884\u7559\uff09", None))
    # retranslateUi

