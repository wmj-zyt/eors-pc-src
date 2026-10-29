# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModelTrainingWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)
from . import image_rc

class Ui_ModelTrainingWidget(object):
    def setupUi(self, ModelTrainingWidget):
        if not ModelTrainingWidget.objectName():
            ModelTrainingWidget.setObjectName(u"ModelTrainingWidget")
        ModelTrainingWidget.resize(1408, 874)
        ModelTrainingWidget.setContextMenuPolicy(Qt.NoContextMenu)
        ModelTrainingWidget.setStyleSheet(u"background-color: rgb(245, 249, 254);")
        self.verticalLayout = QVBoxLayout(ModelTrainingWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.TrainRunningFrame = QFrame(ModelTrainingWidget)
        self.TrainRunningFrame.setObjectName(u"TrainRunningFrame")
        self.TrainRunningFrame.setStyleSheet(u"")
        self.TrainRunningFrame.setFrameShape(QFrame.NoFrame)
        self.TrainRunningFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_12 = QVBoxLayout(self.TrainRunningFrame)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_29 = QFrame(self.TrainRunningFrame)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMinimumSize(QSize(0, 180))
        self.frame_29.setMaximumSize(QSize(16777215, 180))
        self.frame_29.setStyleSheet(u"QFrame#frame_29{\n"
"background-color: rgb(238, 242, 255);\n"
"border:3px dashed rgb(255, 255, 255);\n"
"border-radius:4px;\n"
"margin:0 4px;\n"
"margin-top:4px;\n"
"padding:4px;\n"
"}")
        self.frame_29.setFrameShape(QFrame.NoFrame)
        self.frame_29.setLineWidth(0)
        self.verticalLayout_18 = QVBoxLayout(self.frame_29)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.TrainDatasetInfo = QTableWidget(self.frame_29)
        if (self.TrainDatasetInfo.columnCount() < 4):
            self.TrainDatasetInfo.setColumnCount(4)
        self.TrainDatasetInfo.setObjectName(u"TrainDatasetInfo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrainDatasetInfo.sizePolicy().hasHeightForWidth())
        self.TrainDatasetInfo.setSizePolicy(sizePolicy)
        self.TrainDatasetInfo.setMinimumSize(QSize(0, 0))
        self.TrainDatasetInfo.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei"])
        self.TrainDatasetInfo.setFont(font)
        self.TrainDatasetInfo.setStyleSheet(u"QTableWidget{\n"
"border:none;\n"
"font-size:13px;\n"
"font-family:\"Microsoft YaHei\";\n"
"color:#2c2c2c;\n"
"text-align:center;\n"
"}\n"
"QHeaderView::section {\n"
" font-weight:bold;\n"
"font-size:16px;\n"
" font-family: Arial;\n"
"height:30px;\n"
"color:#4549a2;\n"
"}\n"
"QScrollBar{\n"
"width:8px;\n"
"background-color:#fff;\n"
"}\n"
"QScrollBar::handle{\n"
"border:none;\n"
"border-radius:4px;\n"
"background-color:#dcdafa;\n"
"}")
        self.TrainDatasetInfo.setFrameShape(QFrame.NoFrame)
        self.TrainDatasetInfo.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.TrainDatasetInfo.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.TrainDatasetInfo.setAutoScroll(True)
        self.TrainDatasetInfo.setAutoScrollMargin(0)
        self.TrainDatasetInfo.setDragDropOverwriteMode(False)
        self.TrainDatasetInfo.setShowGrid(True)
        self.TrainDatasetInfo.setGridStyle(Qt.NoPen)
        self.TrainDatasetInfo.setSortingEnabled(False)
        self.TrainDatasetInfo.setWordWrap(True)
        self.TrainDatasetInfo.setCornerButtonEnabled(False)
        self.TrainDatasetInfo.setRowCount(0)
        self.TrainDatasetInfo.setColumnCount(4)
        self.TrainDatasetInfo.horizontalHeader().setVisible(False)
        self.TrainDatasetInfo.horizontalHeader().setCascadingSectionResizes(True)
        self.TrainDatasetInfo.horizontalHeader().setMinimumSectionSize(0)
        self.TrainDatasetInfo.horizontalHeader().setDefaultSectionSize(224)
        self.TrainDatasetInfo.horizontalHeader().setHighlightSections(False)
        self.TrainDatasetInfo.horizontalHeader().setProperty("showSortIndicator", False)
        self.TrainDatasetInfo.horizontalHeader().setStretchLastSection(False)
        self.TrainDatasetInfo.verticalHeader().setVisible(False)
        self.TrainDatasetInfo.verticalHeader().setMinimumSectionSize(0)
        self.TrainDatasetInfo.verticalHeader().setDefaultSectionSize(30)
        self.TrainDatasetInfo.verticalHeader().setHighlightSections(False)
        self.TrainDatasetInfo.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_18.addWidget(self.TrainDatasetInfo)

        self.TrainLoadDataset = QPushButton(self.frame_29)
        self.TrainLoadDataset.setObjectName(u"TrainLoadDataset")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TrainLoadDataset.sizePolicy().hasHeightForWidth())
        self.TrainLoadDataset.setSizePolicy(sizePolicy1)
        font1 = QFont()
        self.TrainLoadDataset.setFont(font1)
        self.TrainLoadDataset.setCursor(QCursor(Qt.PointingHandCursor))
        self.TrainLoadDataset.setStyleSheet(u"QPushButton{\n"
"margin:0 auto;\n"
"\n"
"border: 2px solid #b18bfd;\n"
"border-radius: 4px;\n"
"color: #b18bfd;\n"
"font-size:14px;\n"
"width:180px;\n"
"height: 40px;\n"
"}\n"
"QPushButton:hover{\n"
"color:transparent;\n"
"background-color:#b18bfd;\n"
"background-image: url(:/img/loadDataset-white.png);\n"
"background-origin:content;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"}\n"
"")

        self.verticalLayout_18.addWidget(self.TrainLoadDataset)

        self.TrainLoadDatasetProgressBar = QProgressBar(self.frame_29)
        self.TrainLoadDatasetProgressBar.setObjectName(u"TrainLoadDatasetProgressBar")
        self.TrainLoadDatasetProgressBar.setMinimumSize(QSize(0, 8))
        self.TrainLoadDatasetProgressBar.setMaximumSize(QSize(16777215, 8))
        self.TrainLoadDatasetProgressBar.setStyleSheet(u"QProgressBar{ \n"
"font: 500 8pt \"Microsoft YaHei UI\";\n"
"color: #ff7b15; \n"
"text-align:center; \n"
"border:none;\n"
"background-color: rgb(245, 249, 255);\n"
"font-weight:bold;\n"
"} \n"
"\n"
"QProgressBar:chunk{\n"
"background: rgba(119, 111, 252, 200);\n"
"\n"
"}")
        self.TrainLoadDatasetProgressBar.setValue(15)

        self.verticalLayout_18.addWidget(self.TrainLoadDatasetProgressBar)

        self.TrainDeleteDataset = QPushButton(self.frame_29)
        self.TrainDeleteDataset.setObjectName(u"TrainDeleteDataset")
        self.TrainDeleteDataset.setMinimumSize(QSize(0, 40))
        self.TrainDeleteDataset.setMaximumSize(QSize(16777215, 40))
        self.TrainDeleteDataset.setFont(font1)
        self.TrainDeleteDataset.setCursor(QCursor(Qt.PointingHandCursor))
        self.TrainDeleteDataset.setStyleSheet(u"QPushButton#TrainDeleteDataset_2{\n"
"border:none;\n"
"border:2px solid #b08bfd;\n"
"background:#b08bfd;\n"
"padding:4px;\n"
"color:#fff;\n"
"font-size:14px;\n"
"margin-top:4px;\n"
"}\n"
"QPushButton#TrainDeleteDataset_2:hover{\n"
"background:#e1d9fe;\n"
"}\n"
"QPushButton#TrainDeleteDataset_2:disabled\n"
"{\n"
"	border:1px solid #9ea1b8;\n"
"    background-color:#9ea1b8;/*\u6539\u53d8\u80cc\u666f\u8272*/\n"
"}")
        icon = QIcon()
        icon.addFile(u":/img/04-Image/unloadDataset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.TrainDeleteDataset.setIcon(icon)

        self.verticalLayout_18.addWidget(self.TrainDeleteDataset)


        self.verticalLayout_12.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.TrainRunningFrame)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setMinimumSize(QSize(0, 0))
        self.frame_30.setMaximumSize(QSize(16777215, 16777215))
        self.frame_30.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(4, 0, 6, 0)
        self.tabWidget = QTabWidget(self.frame_30)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setCursor(QCursor(Qt.PointingHandCursor))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane{\n"
"border-top: 2px solid #4f46e5;\n"
"left: 4px;\n"
"}\n"
"QTabBar::tab{\n"
"	left: 4px;\n"
"	font-size:14px;\n"
"	font-weight:bold;\n"
"	background-color: transparent;\n"
"	padding:12px 16px;\n"
"	border:none;\n"
"	border-top-left-radius: 8px;\n"
"	border-top-right-radius: 8px;\n"
"	margin-right: 4px;\n"
"	color: #475569;\n"
"}\n"
"QTabBar::tab:hover{\n"
"	background-color: #e2e8f0;\n"
"}\n"
"QTabBar::tab:selected{\n"
"	background-color: #4f46e5;\n"
"	color: #fff;\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_19 = QVBoxLayout(self.tab)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.tab)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMinimumSize(QSize(0, 50))
        self.frame_32.setMaximumSize(QSize(16777215, 50))
        self.frame_32.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_32)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"font-size:14px;\n"
"font-weight:600;")

        self.horizontalLayout_26.addWidget(self.label_14)

        self.trainModelComboBox = QComboBox(self.frame_32)
        self.trainModelComboBox.setObjectName(u"trainModelComboBox")
        sizePolicy1.setHeightForWidth(self.trainModelComboBox.sizePolicy().hasHeightForWidth())
        self.trainModelComboBox.setSizePolicy(sizePolicy1)
        self.trainModelComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.trainModelComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_26.addWidget(self.trainModelComboBox)

        self.refreshModelList2 = QPushButton(self.frame_32)
        self.refreshModelList2.setObjectName(u"refreshModelList2")
        font2 = QFont()
        font2.setBold(True)
        font2.setUnderline(True)
        self.refreshModelList2.setFont(font2)
        self.refreshModelList2.setStyleSheet(u"QPushButton{\n"
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

        self.horizontalLayout_26.addWidget(self.refreshModelList2)

        self.horizontalSpacer_7 = QSpacerItem(520, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_7)

        self.startTrainRunning = QPushButton(self.frame_32)
        self.startTrainRunning.setObjectName(u"startTrainRunning")
        self.startTrainRunning.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.startTrainRunning.sizePolicy().hasHeightForWidth())
        self.startTrainRunning.setSizePolicy(sizePolicy2)
        self.startTrainRunning.setMinimumSize(QSize(150, 0))
        self.startTrainRunning.setStyleSheet(u"QPushButton{\n"
"	background-color: #4f46e5;\n"
"	color: #fff;\n"
"	font-size: 14px;\n"
"	font-weight: bold;\n"
"	padding: 8px 36px;\n"
"	border:1px solid #4f46e5;\n"
"	border-radius: 4px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #4338ca;\n"
"	border:1px solid #4338ca;\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: #4f46e5;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"	border:1px solid #9ea1b8;\n"
"    background-color:#9ea1b8;/*\u6539\u53d8\u80cc\u666f\u8272*/\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/img/images/startTrain.png", QSize(), QIcon.Normal, QIcon.Off)
        self.startTrainRunning.setIcon(icon1)

        self.horizontalLayout_26.addWidget(self.startTrainRunning)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer)

        self.startAutoTrainRunning = QPushButton(self.frame_32)
        self.startAutoTrainRunning.setObjectName(u"startAutoTrainRunning")
        self.startAutoTrainRunning.setMinimumSize(QSize(150, 0))
        self.startAutoTrainRunning.setStyleSheet(u"QPushButton{\n"
"	background-color: #4f46e5;\n"
"	color: #fff;\n"
"	font-size: 14px;\n"
"	font-weight: bold;\n"
"	padding: 8px 36px;\n"
"	border:1px solid #4f46e5;\n"
"	border-radius: 4px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: #4338ca;\n"
"	border:1px solid #4338ca;\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: #4f46e5;\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"	border:1px solid #9ea1b8;\n"
"    background-color:#9ea1b8;/*\u6539\u53d8\u80cc\u666f\u8272*/\n"
"}")
        self.startAutoTrainRunning.setIcon(icon1)

        self.horizontalLayout_26.addWidget(self.startAutoTrainRunning)


        self.verticalLayout_19.addWidget(self.frame_32)

        self.frame_31 = QFrame(self.tab)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_20 = QVBoxLayout(self.frame_31)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.frame_35 = QFrame(self.frame_31)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_33 = QFrame(self.frame_35)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setStyleSheet(u"QFrame#frame_33{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"padding:4px;\n"
"}")
        self.frame_33.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_21 = QVBoxLayout(self.frame_33)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_36 = QFrame(self.frame_33)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setStyleSheet(u"background-color: transparent;")
        self.frame_36.setFrameShape(QFrame.NoFrame)
        self.frame_36.setLineWidth(0)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.frame_36)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"font: 600 14px \"Segoe UI\"; \n"
"font-weight:bold;\n"
"padding:4px;")

        self.horizontalLayout_28.addWidget(self.label_17)

        self.horizontalSpacer_8 = QSpacerItem(269, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_8)

        self.clearTrainInfo = QPushButton(self.frame_36)
        self.clearTrainInfo.setObjectName(u"clearTrainInfo")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.clearTrainInfo.sizePolicy().hasHeightForWidth())
        self.clearTrainInfo.setSizePolicy(sizePolicy3)
        self.clearTrainInfo.setToolTipDuration(0)
        self.clearTrainInfo.setStyleSheet(u"QPushButton{\n"
"	background-image: url(:/img/clearTextEdit-black.png);\n"
"background-origin:content;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"}\n"
"QPushButton:hover{\n"
"	background-image: url(:/img/clearTextEdit.png);\n"
"\n"
"}")

        self.horizontalLayout_28.addWidget(self.clearTrainInfo)


        self.verticalLayout_21.addWidget(self.frame_36)

        self.trainInfoText = QTextEdit(self.frame_33)
        self.trainInfoText.setObjectName(u"trainInfoText")
        self.trainInfoText.setStyleSheet(u"border:none;\n"
"border-top:1px solid #fff;\n"
"background:transparent;\n"
"font-weight:bold;")
        self.trainInfoText.setLineWrapMode(QTextEdit.NoWrap)
        self.trainInfoText.setReadOnly(True)
        self.trainInfoText.setOverwriteMode(True)

        self.verticalLayout_21.addWidget(self.trainInfoText)


        self.horizontalLayout_27.addWidget(self.frame_33)

        self.frame_34 = QFrame(self.frame_35)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setStyleSheet(u"QFrame#frame_34{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"padding:4px;\n"
"}")
        self.frame_34.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_11 = QVBoxLayout(self.frame_34)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_34)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color: transparent;")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 600 14px \"Segoe UI\"; \n"
"font-weight:bold;\n"
"padding:4px;")

        self.horizontalLayout_2.addWidget(self.label)

        self.clearTrainChart = QPushButton(self.frame_2)
        self.clearTrainChart.setObjectName(u"clearTrainChart")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.clearTrainChart.sizePolicy().hasHeightForWidth())
        self.clearTrainChart.setSizePolicy(sizePolicy4)
        self.clearTrainChart.setStyleSheet(u"QPushButton{\n"
"background-image:url(:/img/clearTextEdit-black.png);\n"
"\n"
"background-origin:content;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"}\n"
"QPushButton:hover{\n"
"background-image:url(:/img/clearTextEdit.png);\n"
"}")

        self.horizontalLayout_2.addWidget(self.clearTrainChart)


        self.verticalLayout_11.addWidget(self.frame_2)

        self.TrainGraphicsView = QChartView(self.frame_34)
        self.TrainGraphicsView.setObjectName(u"TrainGraphicsView")
        self.TrainGraphicsView.setEnabled(False)
        self.TrainGraphicsView.setStyleSheet(u"border:none;\n"
"border-top:1px solid #fff;\n"
"background:transparent;")
        brush = QBrush(QColor(238, 242, 255, 255))
        brush.setStyle(Qt.NoBrush)
        self.TrainGraphicsView.setBackgroundBrush(brush)

        self.verticalLayout_11.addWidget(self.TrainGraphicsView)


        self.horizontalLayout_27.addWidget(self.frame_34)

        self.horizontalLayout_27.setStretch(0, 1)
        self.horizontalLayout_27.setStretch(1, 1)

        self.verticalLayout_20.addWidget(self.frame_35)

        self.trainModelProgressBar = QProgressBar(self.frame_31)
        self.trainModelProgressBar.setObjectName(u"trainModelProgressBar")
        self.trainModelProgressBar.setStyleSheet(u"QProgressBar{ \n"
"font: 700 10pt \"Microsoft YaHei UI\";\n"
"color: #ff7b15; \n"
"text-align:center; \n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius: 25px; \n"
"background-color: rgba(215, 215, 215,100);\n"
"height:8px;\n"
"} \n"
"\n"
"QProgressBar:chunk{ \n"
"background: rgba(119, 111, 252, 200);\n"
"}")
        self.trainModelProgressBar.setValue(0)

        self.verticalLayout_20.addWidget(self.trainModelProgressBar)


        self.verticalLayout_19.addWidget(self.frame_31)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_19 = QLabel(self.tab_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(360, 170, 261, 16))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_20 = QLabel(self.tab_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(380, 180, 331, 16))
        self.tabWidget.addTab(self.tab_3, "")

        self.horizontalLayout_25.addWidget(self.tabWidget)


        self.verticalLayout_12.addWidget(self.frame_30)


        self.horizontalLayout.addWidget(self.TrainRunningFrame)

        self.TrainSettingsFrame = QFrame(ModelTrainingWidget)
        self.TrainSettingsFrame.setObjectName(u"TrainSettingsFrame")
        self.TrainSettingsFrame.setStyleSheet(u"background:#b08bfd;")
        self.TrainSettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.TrainSettingsFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.TrainSettingsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_13 = QFrame(self.TrainSettingsFrame)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 48))
        self.frame_13.setMaximumSize(QSize(16777215, 48))
        self.frame_13.setStyleSheet(u"background:transparent;")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_4 = QLabel(self.frame_13)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"padding-left: 0px;\n"
"padding-bottom: 2px;\n"
"color: rgba(255, 255, 255, 240);\n"
"font: 700  16pt \"Segoe UI\";")

        self.horizontalLayout_19.addWidget(self.label_4)


        self.verticalLayout_2.addWidget(self.frame_13)

        self.frame_16 = QFrame(self.TrainSettingsFrame)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"*{background:transparent;color: rgba(255, 255, 255, 199);\n"
"font: 700 13pt \"Nirmala UI\";}\n"
"QSpinBox {\n"
"border: 0px solid lightgray;\n"
"border-radius: 2px;\n"
"background-color: rgba(255,255,255,90);\n"
"font: 600 9pt \"Segoe UI\";\n"
"}\n"
"        \n"
"QSpinBox::up-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/img/02-Image/box_up.png);\n"
"}\n"
"QSpinBox::up-button:pressed {\n"
"margin-top: 1px;\n"
"}\n"
"            \n"
"QSpinBox::down-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/img/02-Image/box_down.png);\n"
"}\n"
"QSpinBox::down-button:pressed {\n"
"margin-bottom: 1px;\n"
"}\n"
"QDoubleSpinBox {\n"
"border: 0px solid lightgray;\n"
"border-radius: 2px;\n"
"background-color: rgba(255,255,255,90);\n"
"font: 600 9pt \"Segoe UI\";\n"
"}\n"
"        \n"
"QDoubleSpinBox::up-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image:url(:/img/02-Image/box_up.png);\n"
"}\n"
""
                        "QDoubleSpinBox::up-button:pressed {\n"
"margin-top: 1px;\n"
"}\n"
"            \n"
"QDoubleSpinBox::down-button {\n"
"width: 10px;\n"
"height: 9px;\n"
"margin: 0px 3px 0px 0px;\n"
"border-image: url(:/img/02-Image/box_down.png);\n"
"}\n"
"QDoubleSpinBox::down-button:pressed {\n"
"margin-bottom: 1px;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"border: none;\n"
"height: 10px;\n"
"background-color: rgba(255,255,255,90);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 10px;\n"
"margin: -1px 0px -1px 0px;\n"
"border-radius: 3px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qradialgradient(cx:0, cy:0, radius:1, fx:0.1, fy:0.1, stop:0 rgb(253, 139, 133),  stop:1 rgb(248, 194, 152));\n"
"border-radius: 5px;\n"
"}")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_16)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_19 = QFrame(self.frame_16)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(0, 90))
        self.frame_19.setMaximumSize(QSize(16777215, 90))
        self.frame_19.setSizeIncrement(QSize(0, 0))
        self.frame_19.setStyleSheet(u"QFrame#frame_19{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_4 = QVBoxLayout(self.frame_19)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_7 = QLabel(self.frame_19)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 60))
        self.label_7.setMaximumSize(QSize(16777215, 60))
        self.label_7.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.label_7)

        self.frame_24 = QFrame(self.frame_19)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 0))
        self.frame_24.setSizeIncrement(QSize(0, 60))
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.frame_24.setLineWidth(0)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_20.setSpacing(6)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.epochSpinBox = QSpinBox(self.frame_24)
        self.epochSpinBox.setObjectName(u"epochSpinBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.epochSpinBox.sizePolicy().hasHeightForWidth())
        self.epochSpinBox.setSizePolicy(sizePolicy5)
        self.epochSpinBox.setMinimumSize(QSize(0, 0))
        self.epochSpinBox.setSizeIncrement(QSize(0, 0))
        self.epochSpinBox.setAutoFillBackground(False)
        self.epochSpinBox.setStyleSheet(u"")
        self.epochSpinBox.setWrapping(False)
        self.epochSpinBox.setMaximum(600)
        self.epochSpinBox.setValue(40)

        self.horizontalLayout_20.addWidget(self.epochSpinBox)

        self.epochSlider = QSlider(self.frame_24)
        self.epochSlider.setObjectName(u"epochSlider")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.epochSlider.sizePolicy().hasHeightForWidth())
        self.epochSlider.setSizePolicy(sizePolicy6)
        self.epochSlider.setStyleSheet(u"")
        self.epochSlider.setMaximum(600)
        self.epochSlider.setValue(40)
        self.epochSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_20.addWidget(self.epochSlider)

        self.horizontalLayout_20.setStretch(0, 1)
        self.horizontalLayout_20.setStretch(1, 2)

        self.verticalLayout_4.addWidget(self.frame_24)


        self.verticalLayout_3.addWidget(self.frame_19)

        self.frame_54 = QFrame(self.frame_16)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setStyleSheet(u"QFrame#frame_54{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_54.setFrameShape(QFrame.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_54)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.label_21 = QLabel(self.frame_54)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 60))
        self.label_21.setMaximumSize(QSize(16777215, 60))
        self.label_21.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.label_21)

        self.frame_68 = QFrame(self.frame_54)
        self.frame_68.setObjectName(u"frame_68")
        self.frame_68.setMinimumSize(QSize(0, 0))
        self.frame_68.setSizeIncrement(QSize(0, 60))
        self.frame_68.setFrameShape(QFrame.NoFrame)
        self.frame_68.setLineWidth(0)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_68)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.batchsizeSpinBox = QSpinBox(self.frame_68)
        self.batchsizeSpinBox.setObjectName(u"batchsizeSpinBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.batchsizeSpinBox.sizePolicy().hasHeightForWidth())
        self.batchsizeSpinBox.setSizePolicy(sizePolicy7)
        self.batchsizeSpinBox.setStyleSheet(u"")
        self.batchsizeSpinBox.setMinimum(1)
        self.batchsizeSpinBox.setMaximum(128)
        self.batchsizeSpinBox.setSingleStep(1)
        self.batchsizeSpinBox.setValue(16)

        self.horizontalLayout_55.addWidget(self.batchsizeSpinBox)

        self.batchsizeSlider = QSlider(self.frame_68)
        self.batchsizeSlider.setObjectName(u"batchsizeSlider")
        sizePolicy6.setHeightForWidth(self.batchsizeSlider.sizePolicy().hasHeightForWidth())
        self.batchsizeSlider.setSizePolicy(sizePolicy6)
        self.batchsizeSlider.setStyleSheet(u"")
        self.batchsizeSlider.setMinimum(1)
        self.batchsizeSlider.setMaximum(128)
        self.batchsizeSlider.setSingleStep(1)
        self.batchsizeSlider.setPageStep(16)
        self.batchsizeSlider.setValue(16)
        self.batchsizeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_55.addWidget(self.batchsizeSlider)

        self.horizontalLayout_55.setStretch(0, 1)
        self.horizontalLayout_55.setStretch(1, 2)

        self.verticalLayout_6.addWidget(self.frame_68)


        self.verticalLayout_3.addWidget(self.frame_54)

        self.frame_20 = QFrame(self.frame_16)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setStyleSheet(u"QFrame#frame_20{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_20)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.label_10 = QLabel(self.frame_20)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_5.addWidget(self.label_10)

        self.frame_25 = QFrame(self.frame_20)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.frame_25.setLineWidth(0)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.learningRateSpinBox = QDoubleSpinBox(self.frame_25)
        self.learningRateSpinBox.setObjectName(u"learningRateSpinBox")
        self.learningRateSpinBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.learningRateSpinBox.sizePolicy().hasHeightForWidth())
        self.learningRateSpinBox.setSizePolicy(sizePolicy5)
        self.learningRateSpinBox.setDecimals(4)
        self.learningRateSpinBox.setMaximum(0.100000000000000)
        self.learningRateSpinBox.setSingleStep(0.000100000000000)
        self.learningRateSpinBox.setValue(0.001000000000000)

        self.horizontalLayout_21.addWidget(self.learningRateSpinBox)

        self.learningRateSlider = QSlider(self.frame_25)
        self.learningRateSlider.setObjectName(u"learningRateSlider")
        sizePolicy6.setHeightForWidth(self.learningRateSlider.sizePolicy().hasHeightForWidth())
        self.learningRateSlider.setSizePolicy(sizePolicy6)
        self.learningRateSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: none;\n"
"height: 10px;\n"
"background-color: rgba(255,255,255,90);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 10px;\n"
"margin: -1px 0px -1px 0px;\n"
"border-radius: 3px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #59969b, stop:1 #04e7fa);\n"
"border-radius: 5px;\n"
"}")
        self.learningRateSlider.setMaximum(1000)
        self.learningRateSlider.setValue(10)
        self.learningRateSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_21.addWidget(self.learningRateSlider)

        self.horizontalLayout_21.setStretch(0, 2)
        self.horizontalLayout_21.setStretch(1, 3)

        self.verticalLayout_5.addWidget(self.frame_25)


        self.verticalLayout_3.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_16)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setStyleSheet(u"QFrame#frame_21{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_21)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.label_11 = QLabel(self.frame_21)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 60))
        self.label_11.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_7.addWidget(self.label_11)

        self.frame_26 = QFrame(self.frame_21)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.frame_26.setLineWidth(0)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.testDatasetRatioSpinBox = QDoubleSpinBox(self.frame_26)
        self.testDatasetRatioSpinBox.setObjectName(u"testDatasetRatioSpinBox")
        sizePolicy7.setHeightForWidth(self.testDatasetRatioSpinBox.sizePolicy().hasHeightForWidth())
        self.testDatasetRatioSpinBox.setSizePolicy(sizePolicy7)
        self.testDatasetRatioSpinBox.setDecimals(3)
        self.testDatasetRatioSpinBox.setMinimum(0.100000000000000)
        self.testDatasetRatioSpinBox.setMaximum(0.300000000000000)
        self.testDatasetRatioSpinBox.setSingleStep(0.001000000000000)
        self.testDatasetRatioSpinBox.setValue(0.280000000000000)

        self.horizontalLayout_22.addWidget(self.testDatasetRatioSpinBox)

        self.testDatasetRatioSlider = QSlider(self.frame_26)
        self.testDatasetRatioSlider.setObjectName(u"testDatasetRatioSlider")
        sizePolicy6.setHeightForWidth(self.testDatasetRatioSlider.sizePolicy().hasHeightForWidth())
        self.testDatasetRatioSlider.setSizePolicy(sizePolicy6)
        self.testDatasetRatioSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: none;\n"
"height: 10px;\n"
"background-color: rgba(255,255,255,90);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 10px;\n"
"margin: -1px 0px -1px 0px;\n"
"border-radius: 3px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #59969b, stop:1 #04e7fa);\n"
"border-radius: 5px;\n"
"}")
        self.testDatasetRatioSlider.setMinimum(100)
        self.testDatasetRatioSlider.setMaximum(300)
        self.testDatasetRatioSlider.setValue(280)
        self.testDatasetRatioSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_22.addWidget(self.testDatasetRatioSlider)

        self.horizontalLayout_22.setStretch(0, 2)
        self.horizontalLayout_22.setStretch(1, 3)

        self.verticalLayout_7.addWidget(self.frame_26)


        self.verticalLayout_3.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.frame_16)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setStyleSheet(u"QFrame#frame_22{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_22)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(9, 9, 9, 9)
        self.label_12 = QLabel(self.frame_22)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 60))
        self.label_12.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_8.addWidget(self.label_12)

        self.frame_27 = QFrame(self.frame_22)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.frame_27.setLineWidth(0)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.tailSpinBox = QSpinBox(self.frame_27)
        self.tailSpinBox.setObjectName(u"tailSpinBox")
        sizePolicy7.setHeightForWidth(self.tailSpinBox.sizePolicy().hasHeightForWidth())
        self.tailSpinBox.setSizePolicy(sizePolicy7)
        self.tailSpinBox.setMaximum(100)
        self.tailSpinBox.setValue(20)

        self.horizontalLayout_23.addWidget(self.tailSpinBox)

        self.tailSlider = QSlider(self.frame_27)
        self.tailSlider.setObjectName(u"tailSlider")
        sizePolicy6.setHeightForWidth(self.tailSlider.sizePolicy().hasHeightForWidth())
        self.tailSlider.setSizePolicy(sizePolicy6)
        self.tailSlider.setMaximum(100)
        self.tailSlider.setValue(20)
        self.tailSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_23.addWidget(self.tailSlider)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(1, 2)

        self.verticalLayout_8.addWidget(self.frame_27)


        self.verticalLayout_3.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.frame_16)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setStyleSheet(u"QFrame#frame_23{border:2px solid rgba(255, 255, 255, 70);\n"
"border-radius:15px;}")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_23)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, -1, -1, 6)
        self.label_13 = QLabel(self.frame_23)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 60))
        self.label_13.setMaximumSize(QSize(16777215, 60))
        self.label_13.setTextFormat(Qt.PlainText)

        self.verticalLayout_9.addWidget(self.label_13)

        self.frame_28 = QFrame(self.frame_23)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.NoFrame)
        self.frame_28.setLineWidth(0)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.alphaSpinBox = QSpinBox(self.frame_28)
        self.alphaSpinBox.setObjectName(u"alphaSpinBox")
        sizePolicy7.setHeightForWidth(self.alphaSpinBox.sizePolicy().hasHeightForWidth())
        self.alphaSpinBox.setSizePolicy(sizePolicy7)
        self.alphaSpinBox.setValue(1)

        self.horizontalLayout_24.addWidget(self.alphaSpinBox)

        self.alphaSlider = QSlider(self.frame_28)
        self.alphaSlider.setObjectName(u"alphaSlider")
        sizePolicy6.setHeightForWidth(self.alphaSlider.sizePolicy().hasHeightForWidth())
        self.alphaSlider.setSizePolicy(sizePolicy6)
        self.alphaSlider.setValue(1)
        self.alphaSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_24.addWidget(self.alphaSlider)

        self.horizontalLayout_24.setStretch(0, 1)
        self.horizontalLayout_24.setStretch(1, 2)

        self.verticalLayout_9.addWidget(self.frame_28)


        self.verticalLayout_3.addWidget(self.frame_23)

        self.frame_37 = QFrame(self.frame_16)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_37)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.resetTrainSettings = QPushButton(self.frame_37)
        self.resetTrainSettings.setObjectName(u"resetTrainSettings")
        sizePolicy1.setHeightForWidth(self.resetTrainSettings.sizePolicy().hasHeightForWidth())
        self.resetTrainSettings.setSizePolicy(sizePolicy1)
        self.resetTrainSettings.setStyleSheet(u"QPushButton{\n"
"background-color:#FFF;\n"
"color:#ac8bfa;\n"
"border:none;\n"
"border-radius:16px;\n"
"padding:8px;\n"
"font-size:16px;\n"
"width:140px;\n"
"height:24px;\n"
"margin-top:12px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:#e1d9fe;\n"
"background-image:url(:/img/reset.png);\n"
"background-origin:content;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"color:transparent;\n"
"}")

        self.verticalLayout_10.addWidget(self.resetTrainSettings)


        self.verticalLayout_3.addWidget(self.frame_37)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addWidget(self.frame_16)


        self.horizontalLayout.addWidget(self.TrainSettingsFrame)

        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ModelTrainingWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ModelTrainingWidget)
    # setupUi

    def retranslateUi(self, ModelTrainingWidget):
        ModelTrainingWidget.setWindowTitle(QCoreApplication.translate("ModelTrainingWidget", u"Form", None))
        self.TrainLoadDataset.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u5bfc\u5165\u6570\u636e\u96c6", None))
        self.TrainDeleteDataset.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u6e05\u7a7a\u6570\u636e\u96c6", None))
        self.label_14.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
#if QT_CONFIG(tooltip)
        self.refreshModelList2.setToolTip(QCoreApplication.translate("ModelTrainingWidget", u"\u5237\u65b0\u6a21\u578b\u5217\u8868", None))
#endif // QT_CONFIG(tooltip)
        self.refreshModelList2.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u5237\u65b0", None))
        self.startTrainRunning.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.startAutoTrainRunning.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u81ea\u52a8\u8bad\u7ec3", None))
        self.label_17.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u8bad\u7ec3\u8fdb\u5ea6\u4fe1\u606f", None))
#if QT_CONFIG(tooltip)
        self.clearTrainInfo.setToolTip(QCoreApplication.translate("ModelTrainingWidget", u"\u6e05\u9664\u4fe1\u606f\u6846", None))
#endif // QT_CONFIG(tooltip)
        self.clearTrainInfo.setText("")
        self.trainInfoText.setMarkdown("")
        self.trainInfoText.setHtml(QCoreApplication.translate("ModelTrainingWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:700; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u635f\u5931 & \u7cbe\u786e\u5ea6", None))
#if QT_CONFIG(tooltip)
        self.clearTrainChart.setToolTip(QCoreApplication.translate("ModelTrainingWidget", u"\u6e05\u9664\u66f2\u7ebf\u56fe", None))
#endif // QT_CONFIG(tooltip)
        self.clearTrainChart.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("ModelTrainingWidget", u"\u666e\u901a\u8bad\u7ec3", None))
        self.label_19.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u589e\u91cf\u5b66\u4e60\uff08\u656c\u8bf7\u671f\u5f85\uff09", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("ModelTrainingWidget", u"\u589e\u91cf\u8bad\u7ec3", None))
        self.label_20.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u65ad\u70b9\u7eed\u8bad\uff08\u656c\u8bf7\u671f\u5f85\uff09", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("ModelTrainingWidget", u"\u65ad\u70b9\u7eed\u8bad", None))
        self.label_4.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u8bad\u7ec3\u53c2\u6570\u8bbe\u7f6e", None))
        self.label_7.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u8bad\u7ec3\u8f6e\u6570", None))
        self.label_21.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u6279\u91cf\u5927\u5c0f", None))
        self.label_10.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u5b66\u4e60\u7387\uff080.0001~0.1\uff09", None))
        self.label_11.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u9a8c\u8bc1\u96c6\u6bd4\u7387\uff080.1~0.3\uff09", None))
        self.label_12.setText(QCoreApplication.translate("ModelTrainingWidget", u"tail", None))
        self.label_13.setText(QCoreApplication.translate("ModelTrainingWidget", u"alpha", None))
        self.resetTrainSettings.setText(QCoreApplication.translate("ModelTrainingWidget", u"\u9ed8\u8ba4\u503c", None))
    # retranslateUi

