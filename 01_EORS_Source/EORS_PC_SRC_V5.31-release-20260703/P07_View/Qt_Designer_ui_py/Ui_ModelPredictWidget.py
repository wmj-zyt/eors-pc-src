# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModelPredictWidget.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from . import image_rc

class Ui_ModelPredictWidget(object):
    def setupUi(self, ModelPredictWidget):
        if not ModelPredictWidget.objectName():
            ModelPredictWidget.setObjectName(u"ModelPredictWidget")
        ModelPredictWidget.resize(919, 974)
        self.horizontalLayout = QHBoxLayout(ModelPredictWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget_2 = QTabWidget(ModelPredictWidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setStyleSheet(u"QTabWidget::pane{\n"
"left: 4px;\n"
"}\n"
"QTabBar::tab{\n"
"	left: 4px;\n"
"	font-size:14px;\n"
"	font-weight:bold;\n"
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
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_12 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.ImageRecognitionFrame = QFrame(self.tab_4)
        self.ImageRecognitionFrame.setObjectName(u"ImageRecognitionFrame")
        self.ImageRecognitionFrame.setMinimumSize(QSize(0, 0))
        self.ImageRecognitionFrame.setStyleSheet(u"")
        self.ImageRecognitionFrame.setFrameShape(QFrame.NoFrame)
        self.ImageRecognitionFrame.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.ImageRecognitionFrame)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 4, 0)
        self.frame_3 = QFrame(self.ImageRecognitionFrame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 55))
        self.frame_3.setMaximumSize(QSize(16777215, 55))
        self.frame_3.setStyleSheet(u"QFrame#frame_3{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px\n"
"}")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.frame_10 = QFrame(self.frame_3)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"background-color: transparent;")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setLineWidth(0)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.import1Img = QPushButton(self.frame_10)
        self.import1Img.setObjectName(u"import1Img")
        self.import1Img.setMinimumSize(QSize(40, 0))
        self.import1Img.setMaximumSize(QSize(40, 16777215))
        self.import1Img.setCursor(QCursor(Qt.PointingHandCursor))
        self.import1Img.setStyleSheet(u"QPushButton{\n"
"width:40px;\n"
"height:40px;\n"
"background-image:url(:/img/images/\u6587\u4ef6\u5939.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center center;\n"
"background-color:#ab8bfa;\n"
"border: none;\n"
"border-radius: 8px;\n"
"text-align: center;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#e1d9fe;\n"
"}")

        self.horizontalLayout_10.addWidget(self.import1Img)

        self.horizontalSpacer_2 = QSpacerItem(8, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_9.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setStyleSheet(u"background-color: transparent;")
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_11.addItem(self.horizontalSpacer)

        self.label_5 = QLabel(self.frame_11)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font-size:14px;\n"
"font-weight:600;")

        self.horizontalLayout_11.addWidget(self.label_5)

        self.modelSelectComboBox = QComboBox(self.frame_11)
        self.modelSelectComboBox.setObjectName(u"modelSelectComboBox")
        self.modelSelectComboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #FEF9F5;\n"
"    color: #5D4037;\n"
"    border: 1px solid #E8DDD0;\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"    font-size: 13px;\n"
"    min-height: 15px;\n"
"	min-width: 150px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #FDF5EC;\n"
"    border: 1px solid #D7CCC8;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 2px solid #BCAAA4;\n"
"    background-color: #FEFAFA;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    border: 2px solid #A1887F;\n"
"    background-color: #FDF7F0;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 25px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #F3E5D3;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    image: url(:/img/images/box_down.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    image: url(:/img/images/box"
                        "_up.png);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #E8DDD0;\n"
"    border-radius: 6px;\n"
"    outline: none;\n"
"    padding: 5px;\n"
"    background-color: #FEFBF8;\n"
"    selection-background-color: #F0E7D8;\n"
"    selection-color: #5D4037;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    min-height: 25px;\n"
"    padding: 3px 8px;\n"
"    color: #5D4037;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #F5EDE1;\n"
"}\n"
"\n"
"QComboBox QScrollBar:vertical {\n"
"    width: 8px;\n"
"    background-color: #F5F5F5;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QComboBox QScrollBar::handle:vertical {\n"
"    background-color: #D7CCC8;\n"
"    border-radius: 4px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QComboBox QScrollBar::handle:vertical:hover {\n"
"    background-color: #BCAAA4;\n"
"}")
        self.modelSelectComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_11.addWidget(self.modelSelectComboBox)

        self.refreshModelList1 = QPushButton(self.frame_11)
        self.refreshModelList1.setObjectName(u"refreshModelList1")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshModelList1.sizePolicy().hasHeightForWidth())
        self.refreshModelList1.setSizePolicy(sizePolicy)
        self.refreshModelList1.setStyleSheet(u"QPushButton{\n"
"	width:40px;\n"
"	border:none;\n"
"	font-weight: bold;\n"
"	background-color: transparent;\n"
"	text-decoration:underline;\n"
"}\n"
"QPushButton:hover{\n"
"	color: gray;\n"
"	text-decoration:none;\n"
"}")

        self.horizontalLayout_11.addWidget(self.refreshModelList1)

        self.horizontalLayout_11.setStretch(0, 2)
        self.horizontalLayout_11.setStretch(2, 1)

        self.horizontalLayout_9.addWidget(self.frame_11)

        self.horizontalLayout_9.setStretch(1, 2)

        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.ImageRecognitionFrame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setStyleSheet(u"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px;")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_9 = QVBoxLayout(self.frame_4)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.imageLabel = QLabel(self.frame_4)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setStyleSheet(u"background-color: rgb(238, 242, 255);\n"
"/*border:2px solid rgb(255, 255, 255);*/\n"
"/*border-radius:15px;*/\n"
"border: none;\n"
"padding: 0, !important;\n"
"")
        self.imageLabel.setLineWidth(0)

        self.verticalLayout_9.addWidget(self.imageLabel)


        self.verticalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.ImageRecognitionFrame)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setMinimumSize(QSize(0, 50))
        self.frame_5.setMaximumSize(QSize(16777215, 50))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.startPredictionBtn = QPushButton(self.frame_5)
        self.startPredictionBtn.setObjectName(u"startPredictionBtn")
        self.startPredictionBtn.setStyleSheet(u"QPushButton{\n"
"background-image:url(:/img/images/begin.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"border: none;\n"
"}\n"
"")

        self.horizontalLayout_6.addWidget(self.startPredictionBtn)

        self.forecastProgressBar = QProgressBar(self.frame_5)
        self.forecastProgressBar.setObjectName(u"forecastProgressBar")
        self.forecastProgressBar.setStyleSheet(u"QProgressBar{ \n"
"font: 700 10pt \"Microsoft YaHei UI\";\n"
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
        self.forecastProgressBar.setValue(0)

        self.horizontalLayout_6.addWidget(self.forecastProgressBar)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.frame_9 = QFrame(self.ImageRecognitionFrame)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy2.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy2)
        self.frame_9.setMinimumSize(QSize(0, 0))
        self.frame_9.setMaximumSize(QSize(16777215, 16777215))
        self.frame_9.setStyleSheet(u"")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_4)

        self.PredictionResultFrame = QFrame(self.frame_9)
        self.PredictionResultFrame.setObjectName(u"PredictionResultFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.PredictionResultFrame.sizePolicy().hasHeightForWidth())
        self.PredictionResultFrame.setSizePolicy(sizePolicy3)
        self.PredictionResultFrame.setStyleSheet(u"QFrame#PredictionResultFrame{\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;\n"
"background-color: qradialgradient(cx:0, cy:0, radius:1, fx:0.1, fy:0.1, stop:0 rgb(162, 129, 247),  stop:1 rgb(119, 111, 252));\n"
"border: 1px outset rgb(98, 91, 213);\n"
"}\n"
"")
        self.PredictionResultFrame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_5 = QHBoxLayout(self.PredictionResultFrame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.PredictionResultFrame)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"border:none;background-color:transparent;")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setStyleSheet(u"border:none;background-color:transparent;")
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_8 = QLabel(self.frame_15)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color: rgba(255, 255, 255,210);\n"
"font: 700 italic 14pt \"Segoe UI\";\n"
"background-color:transparent;")

        self.horizontalLayout_16.addWidget(self.label_8)

        self.predictionResult = QLabel(self.frame_15)
        self.predictionResult.setObjectName(u"predictionResult")
        self.predictionResult.setStyleSheet(u"color: rgba(255, 255, 255,210);\n"
"font: 700  16pt \"Segoe UI\";")

        self.horizontalLayout_16.addWidget(self.predictionResult)


        self.horizontalLayout_14.addWidget(self.frame_15)


        self.horizontalLayout_5.addWidget(self.frame_14)

        self.horizontalLayout_5.setStretch(0, 3)

        self.horizontalLayout_13.addWidget(self.PredictionResultFrame)

        self.horizontalSpacer_6 = QSpacerItem(80, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_6)

        self.ConfidenceLevelFrame = QFrame(self.frame_9)
        self.ConfidenceLevelFrame.setObjectName(u"ConfidenceLevelFrame")
        sizePolicy3.setHeightForWidth(self.ConfidenceLevelFrame.sizePolicy().hasHeightForWidth())
        self.ConfidenceLevelFrame.setSizePolicy(sizePolicy3)
        self.ConfidenceLevelFrame.setStyleSheet(u"QFrame#ConfidenceLevelFrame{\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 15px;\n"
"background-color: qradialgradient(cx:0, cy:0, radius:1, fx:0.1, fy:0.1, stop:0 rgb(162, 129, 247),  stop:1 rgb(119, 111, 252));\n"
"border: 1px outset rgb(98, 91, 213);\n"
"}\n"
"")
        self.ConfidenceLevelFrame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_97 = QHBoxLayout(self.ConfidenceLevelFrame)
        self.horizontalLayout_97.setSpacing(0)
        self.horizontalLayout_97.setObjectName(u"horizontalLayout_97")
        self.horizontalLayout_97.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.ConfidenceLevelFrame)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"border:none;background-color:transparent;")
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_17)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"color: rgba(255, 255, 255,210);\n"
"font: 700 italic 14pt \"Segoe UI\";\n"
"background-color:transparent;")

        self.horizontalLayout_15.addWidget(self.label_9)

        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setStyleSheet(u"border:none;background-color:transparent;")
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.confidenceLevel = QLabel(self.frame_18)
        self.confidenceLevel.setObjectName(u"confidenceLevel")
        self.confidenceLevel.setStyleSheet(u"color: rgba(255, 255, 255,210);\n"
"font: 700  16pt \"Segoe UI\";")

        self.horizontalLayout_8.addWidget(self.confidenceLevel)


        self.horizontalLayout_15.addWidget(self.frame_18)


        self.horizontalLayout_97.addWidget(self.frame_17)

        self.horizontalLayout_97.setStretch(0, 3)

        self.horizontalLayout_13.addWidget(self.ConfidenceLevelFrame)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addWidget(self.frame_9)


        self.horizontalLayout_12.addWidget(self.ImageRecognitionFrame)

        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.horizontalLayout_64 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_64.setSpacing(0)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.horizontalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.frame_71 = QFrame(self.tab_8)
        self.frame_71.setObjectName(u"frame_71")
        self.frame_71.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_35 = QVBoxLayout(self.frame_71)
        self.verticalLayout_35.setSpacing(2)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 4, 0)
        self.frame_72 = QFrame(self.frame_71)
        self.frame_72.setObjectName(u"frame_72")
        self.frame_72.setMinimumSize(QSize(0, 55))
        self.frame_72.setMaximumSize(QSize(16777215, 55))
        self.frame_72.setStyleSheet(u"QFrame#frame_72{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px\n"
"}")
        self.frame_72.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_65 = QHBoxLayout(self.frame_72)
        self.horizontalLayout_65.setSpacing(6)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_65.setContentsMargins(2, 2, 2, 2)
        self.frame_75 = QFrame(self.frame_72)
        self.frame_75.setObjectName(u"frame_75")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_75.sizePolicy().hasHeightForWidth())
        self.frame_75.setSizePolicy(sizePolicy4)
        self.frame_75.setStyleSheet(u"background-color: transparent;")
        self.frame_75.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_75)
        self.horizontalLayout_66.setSpacing(0)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_66.addItem(self.horizontalSpacer_23)

        self.importBatchImg = QPushButton(self.frame_75)
        self.importBatchImg.setObjectName(u"importBatchImg")
        sizePolicy.setHeightForWidth(self.importBatchImg.sizePolicy().hasHeightForWidth())
        self.importBatchImg.setSizePolicy(sizePolicy)
        self.importBatchImg.setStyleSheet(u"QPushButton{\n"
"width:40px;\n"
"height:40px;\n"
"background-image:url(:/img/images/\u6587\u4ef6\u5939.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center center;\n"
"background-color:#ab8bfa;\n"
"border: none;\n"
"border-radius: 8px;\n"
"text-align: center;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#e1d9fe;\n"
"}")

        self.horizontalLayout_66.addWidget(self.importBatchImg)

        self.horizontalSpacer_22 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_66.addItem(self.horizontalSpacer_22)

        self.deleteBatchImg = QPushButton(self.frame_75)
        self.deleteBatchImg.setObjectName(u"deleteBatchImg")
        sizePolicy.setHeightForWidth(self.deleteBatchImg.sizePolicy().hasHeightForWidth())
        self.deleteBatchImg.setSizePolicy(sizePolicy)
        self.deleteBatchImg.setStyleSheet(u"QPushButton{\n"
"width:40px;\n"
"height:40px;\n"
"background-image:url(:/img/images/\u5220\u9664.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center center;\n"
"background-color:#ab8bfa;\n"
"border: none;\n"
"border-radius: 8px;\n"
"text-align: center;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#e1d9fe;\n"
"}")

        self.horizontalLayout_66.addWidget(self.deleteBatchImg)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_66.addItem(self.horizontalSpacer_24)

        self.label_30 = QLabel(self.frame_75)
        self.label_30.setObjectName(u"label_30")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy5)

        self.horizontalLayout_66.addWidget(self.label_30)


        self.horizontalLayout_65.addWidget(self.frame_75)

        self.frame_76 = QFrame(self.frame_72)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setStyleSheet(u"background-color: transparent;")
        self.frame_76.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.label_25 = QLabel(self.frame_76)
        self.label_25.setObjectName(u"label_25")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy6)
        self.label_25.setStyleSheet(u"font-size:14px;\n"
"font-weight:600;")

        self.horizontalLayout_67.addWidget(self.label_25)

        self.modelListComboBox_batchpredict = QComboBox(self.frame_76)
        self.modelListComboBox_batchpredict.setObjectName(u"modelListComboBox_batchpredict")
        self.modelListComboBox_batchpredict.setStyleSheet(u"QComboBox {\n"
"    background-color: #FEF9F5;\n"
"    color: #5D4037;\n"
"    border: 1px solid #E8DDD0;\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"    font-size: 13px;\n"
"    min-height: 15px;\n"
"	min-width: 150px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #FDF5EC;\n"
"    border: 1px solid #D7CCC8;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 2px solid #BCAAA4;\n"
"    background-color: #FEFAFA;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    border: 2px solid #A1887F;\n"
"    background-color: #FDF7F0;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 25px;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #F3E5D3;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    image: url(:/img/images/box_down.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    image: url(:/img/images/box"
                        "_up.png);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #E8DDD0;\n"
"    border-radius: 6px;\n"
"    outline: none;\n"
"    padding: 5px;\n"
"    background-color: #FEFBF8;\n"
"    selection-background-color: #F0E7D8;\n"
"    selection-color: #5D4037;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    min-height: 25px;\n"
"    padding: 3px 8px;\n"
"    color: #5D4037;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background-color: #F5EDE1;\n"
"}\n"
"\n"
"QComboBox QScrollBar:vertical {\n"
"    width: 8px;\n"
"    background-color: #F5F5F5;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QComboBox QScrollBar::handle:vertical {\n"
"    background-color: #D7CCC8;\n"
"    border-radius: 4px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QComboBox QScrollBar::handle:vertical:hover {\n"
"    background-color: #BCAAA4;\n"
"}")

        self.horizontalLayout_67.addWidget(self.modelListComboBox_batchpredict)

        self.refreshModelList_batchpredict = QPushButton(self.frame_76)
        self.refreshModelList_batchpredict.setObjectName(u"refreshModelList_batchpredict")
        sizePolicy.setHeightForWidth(self.refreshModelList_batchpredict.sizePolicy().hasHeightForWidth())
        self.refreshModelList_batchpredict.setSizePolicy(sizePolicy)
        self.refreshModelList_batchpredict.setStyleSheet(u"QPushButton{\n"
"	width:40px;\n"
"	border:none;\n"
"	font-weight: bold;\n"
"	background-color: transparent;\n"
"	text-decoration:underline;\n"
"}\n"
"QPushButton:hover{\n"
"	color: gray;\n"
"	text-decoration:none;\n"
"}")

        self.horizontalLayout_67.addWidget(self.refreshModelList_batchpredict)


        self.horizontalLayout_65.addWidget(self.frame_76)

        self.horizontalLayout_65.setStretch(0, 1)
        self.horizontalLayout_65.setStretch(1, 1)

        self.verticalLayout_35.addWidget(self.frame_72)

        self.frame_74 = QFrame(self.frame_71)
        self.frame_74.setObjectName(u"frame_74")
        self.frame_74.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_36 = QVBoxLayout(self.frame_74)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(4, 4, 4, 4)
        self.frame_77 = QFrame(self.frame_74)
        self.frame_77.setObjectName(u"frame_77")
        sizePolicy2.setHeightForWidth(self.frame_77.sizePolicy().hasHeightForWidth())
        self.frame_77.setSizePolicy(sizePolicy2)
        self.frame_77.setStyleSheet(u"background-color: #fff;\n"
"border-top-left-radius:8px;\n"
"border-top-right-radius:8px;\n"
"padding:4px;")
        self.frame_77.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_69 = QHBoxLayout(self.frame_77)
        self.horizontalLayout_69.setSpacing(0)
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.label_27 = QLabel(self.frame_77)
        self.label_27.setObjectName(u"label_27")
        sizePolicy6.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy6)
        self.label_27.setPixmap(QPixmap(u":/img/02-Image/\u6307\u6807.png"))

        self.horizontalLayout_69.addWidget(self.label_27)

        self.label_26 = QLabel(self.frame_77)
        self.label_26.setObjectName(u"label_26")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet(u"color:#4a5a6b;")

        self.horizontalLayout_69.addWidget(self.label_26)


        self.verticalLayout_36.addWidget(self.frame_77)

        self.frame_78 = QFrame(self.frame_74)
        self.frame_78.setObjectName(u"frame_78")
        self.frame_78.setStyleSheet(u"background-color: #fff;")
        self.frame_78.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_37 = QVBoxLayout(self.frame_78)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.evaluationMetrixTable = QTableWidget(self.frame_78)
        if (self.evaluationMetrixTable.columnCount() < 4):
            self.evaluationMetrixTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.evaluationMetrixTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.evaluationMetrixTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.evaluationMetrixTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.evaluationMetrixTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.evaluationMetrixTable.rowCount() < 1):
            self.evaluationMetrixTable.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.evaluationMetrixTable.setItem(0, 0, __qtablewidgetitem4)
        self.evaluationMetrixTable.setObjectName(u"evaluationMetrixTable")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.evaluationMetrixTable.sizePolicy().hasHeightForWidth())
        self.evaluationMetrixTable.setSizePolicy(sizePolicy7)
        self.evaluationMetrixTable.setStyleSheet(u"QTableWidget{\n"
"font-size:13px;\n"
"font-family:\"Microsoft YaHei\";\n"
"color:#2c2c2c;\n"
"background-color: #fff;\n"
"border-radius: 8px;\n"
"alternate-background-color: gray;\n"
"}\n"
"QHeaderView::section{\n"
"font-size:16px;\n"
"font-family:Times New Roman,Microsoft YaHei;\n"
"font-weight:bold;\n"
"color:#374557;\n"
"}\n"
"QHeaderView::section:horizontal {\n"
"background-color: #f0f4f7;\n"
"height:48px;\n"
"border-top:1px solid #dee2e6;\n"
"border-bottom:1px solid #dee2e6;\n"
"}\n"
"\n"
"QHeaderView::section:vertical{\n"
"width:200px;\n"
"background-color:#fff;\n"
"border:none;\n"
"border-right:1px solid #d8d8d8;\n"
"border-bottom:1px solid #d8d8d8;\n"
"}\n"
"QTableCornerButton::section{\n"
"background-color: #f0f4f7;\n"
"border-top:1px solid #dee2e6;\n"
"border-bottom:1px solid #dee2e6;\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"	background-color: #f0f4f7;\n"
"}\n"
"QTableView::item:selected {\n"
"	background-color: #808080;\n"
"}\n"
"QScrollBar{\n"
"width:8px;\n"
"background-color:#fff;\n"
"}\n"
"Q"
                        "ScrollBar::handle{\n"
"border:none;\n"
"border-radius:4px;\n"
"background-color:#dcdafa;\n"
"}")
        self.evaluationMetrixTable.setFrameShape(QFrame.NoFrame)
        self.evaluationMetrixTable.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.evaluationMetrixTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.evaluationMetrixTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.evaluationMetrixTable.setShowGrid(True)
        self.evaluationMetrixTable.setGridStyle(Qt.NoPen)
        self.evaluationMetrixTable.setSortingEnabled(False)
        self.evaluationMetrixTable.setWordWrap(True)
        self.evaluationMetrixTable.setCornerButtonEnabled(True)
        self.evaluationMetrixTable.setRowCount(1)
        self.evaluationMetrixTable.horizontalHeader().setCascadingSectionResizes(False)
        self.evaluationMetrixTable.horizontalHeader().setMinimumSectionSize(200)
        self.evaluationMetrixTable.horizontalHeader().setHighlightSections(False)
        self.evaluationMetrixTable.horizontalHeader().setStretchLastSection(True)
        self.evaluationMetrixTable.verticalHeader().setVisible(False)
        self.evaluationMetrixTable.verticalHeader().setCascadingSectionResizes(False)
        self.evaluationMetrixTable.verticalHeader().setMinimumSectionSize(40)
        self.evaluationMetrixTable.verticalHeader().setDefaultSectionSize(40)
        self.evaluationMetrixTable.verticalHeader().setHighlightSections(False)
        self.evaluationMetrixTable.verticalHeader().setProperty("showSortIndicator", False)
        self.evaluationMetrixTable.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_37.addWidget(self.evaluationMetrixTable)

        self.label_28 = QLabel(self.frame_78)
        self.label_28.setObjectName(u"label_28")
        sizePolicy4.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy4)
        self.label_28.setStyleSheet(u"background-color: #fff;")
        self.label_28.setPixmap(QPixmap(u":/img/02-Image/\u7a7a\u767d.png"))

        self.verticalLayout_37.addWidget(self.label_28)

        self.label_29 = QLabel(self.frame_78)
        self.label_29.setObjectName(u"label_29")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_29.setFont(font1)
        self.label_29.setStyleSheet(u"background-color: #fff;\n"
"border-bottom-left-radius:8px;\n"
"border-bottom-right-radius:8px;\n"
"padding-top:8px;")

        self.verticalLayout_37.addWidget(self.label_29)

        self.verticalLayout_37.setStretch(0, 1)
        self.verticalLayout_37.setStretch(1, 1)

        self.verticalLayout_36.addWidget(self.frame_78)


        self.verticalLayout_35.addWidget(self.frame_74)

        self.frame_73 = QFrame(self.frame_71)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setMinimumSize(QSize(0, 50))
        self.frame_73.setMaximumSize(QSize(16777215, 50))
        self.frame_73.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_73)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.startBatchPredictionBtn = QPushButton(self.frame_73)
        self.startBatchPredictionBtn.setObjectName(u"startBatchPredictionBtn")
        self.startBatchPredictionBtn.setStyleSheet(u"QPushButton{\n"
"background-image: url(:/img/images/begin.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"border: none;\n"
"}\n"
"")

        self.horizontalLayout_68.addWidget(self.startBatchPredictionBtn)

        self.batchTestProgressBar = QProgressBar(self.frame_73)
        self.batchTestProgressBar.setObjectName(u"batchTestProgressBar")
        self.batchTestProgressBar.setStyleSheet(u"QProgressBar{ \n"
"font: 700 10pt \"Microsoft YaHei UI\";\n"
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
        self.batchTestProgressBar.setValue(0)

        self.horizontalLayout_68.addWidget(self.batchTestProgressBar)


        self.verticalLayout_35.addWidget(self.frame_73)


        self.horizontalLayout_64.addWidget(self.frame_71)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget_2.addTab(self.tab_5, "")

        self.horizontalLayout.addWidget(self.tabWidget_2)


        self.retranslateUi(ModelPredictWidget)

        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ModelPredictWidget)
    # setupUi

    def retranslateUi(self, ModelPredictWidget):
        ModelPredictWidget.setWindowTitle(QCoreApplication.translate("ModelPredictWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.import1Img.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5bfc\u5165\u56fe\u7247", None))
#endif // QT_CONFIG(tooltip)
        self.import1Img.setText("")
        self.label_5.setText(QCoreApplication.translate("ModelPredictWidget", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
#if QT_CONFIG(tooltip)
        self.refreshModelList1.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5237\u65b0\u6a21\u578b\u5217\u8868", None))
#endif // QT_CONFIG(tooltip)
        self.refreshModelList1.setText(QCoreApplication.translate("ModelPredictWidget", u"\u5237\u65b0", None))
        self.imageLabel.setText("")
#if QT_CONFIG(tooltip)
        self.startPredictionBtn.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5f00\u59cb\u9884\u6d4b", None))
#endif // QT_CONFIG(tooltip)
        self.startPredictionBtn.setText("")
        self.label_8.setText(QCoreApplication.translate("ModelPredictWidget", u"\u9884\u6d4b\u7ed3\u679c", None))
        self.predictionResult.setText("")
        self.label_9.setText(QCoreApplication.translate("ModelPredictWidget", u"\u7f6e\u4fe1\u5ea6", None))
        self.confidenceLevel.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("ModelPredictWidget", u"\u56fe\u50cf\u8bc6\u522b", None))
#if QT_CONFIG(tooltip)
        self.importBatchImg.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5bfc\u5165\u6d4b\u8bd5\u96c6", None))
#endif // QT_CONFIG(tooltip)
        self.importBatchImg.setText("")
#if QT_CONFIG(tooltip)
        self.deleteBatchImg.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5220\u9664\u6d4b\u8bd5\u96c6", None))
#endif // QT_CONFIG(tooltip)
        self.deleteBatchImg.setText("")
        self.label_30.setText("")
        self.label_25.setText(QCoreApplication.translate("ModelPredictWidget", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
#if QT_CONFIG(tooltip)
        self.refreshModelList_batchpredict.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5237\u65b0\u6a21\u578b\u5217\u8868", None))
#endif // QT_CONFIG(tooltip)
        self.refreshModelList_batchpredict.setText(QCoreApplication.translate("ModelPredictWidget", u"\u5237\u65b0", None))
        self.label_27.setText("")
        self.label_26.setText(QCoreApplication.translate("ModelPredictWidget", u"\u6d4b\u8bd5\u8bc4\u4f30\u6307\u6807", None))
        ___qtablewidgetitem = self.evaluationMetrixTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ModelPredictWidget", u"\u7cbe\u786e\u7387\uff08Precision\uff09", None));
        ___qtablewidgetitem1 = self.evaluationMetrixTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ModelPredictWidget", u"\u53ec\u56de\u7387\uff08Recall\uff09", None));
        ___qtablewidgetitem2 = self.evaluationMetrixTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ModelPredictWidget", u"F1-score", None));

        __sortingEnabled = self.evaluationMetrixTable.isSortingEnabled()
        self.evaluationMetrixTable.setSortingEnabled(False)
        self.evaluationMetrixTable.setSortingEnabled(__sortingEnabled)

        self.label_28.setText("")
        self.label_29.setText(QCoreApplication.translate("ModelPredictWidget", u"\u6682\u65e0\u6570\u636e\uff0c\u8bf7\u5148\u5bfc\u5165\u6d4b\u8bd5\u96c6", None))
#if QT_CONFIG(tooltip)
        self.startBatchPredictionBtn.setToolTip(QCoreApplication.translate("ModelPredictWidget", u"\u5f00\u59cb\u6279\u91cf\u6d4b\u8bd5", None))
#endif // QT_CONFIG(tooltip)
        self.startBatchPredictionBtn.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("ModelPredictWidget", u"\u6279\u91cf\u6d4b\u8bd5", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("ModelPredictWidget", u"\u8bed\u97f3\u8bc6\u522b\uff08\u9884\u7559\uff09", None))
    # retranslateUi

