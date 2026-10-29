# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ComponentGenerateWidget.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_ComponentGenerateWidget(object):
    def setupUi(self, ComponentGenerateWidget):
        if not ComponentGenerateWidget.objectName():
            ComponentGenerateWidget.setObjectName(u"ComponentGenerateWidget")
        ComponentGenerateWidget.resize(851, 611)
        self.horizontalLayout = QHBoxLayout(ComponentGenerateWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ComponentGenerationFrame = QFrame(ComponentGenerateWidget)
        self.ComponentGenerationFrame.setObjectName(u"ComponentGenerationFrame")
        self.ComponentGenerationFrame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_22 = QVBoxLayout(self.ComponentGenerationFrame)
        self.verticalLayout_22.setSpacing(2)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.ComponentGenerationFrame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 55))
        self.frame_6.setMaximumSize(QSize(16777215, 55))
        self.frame_6.setStyleSheet(u"QFrame#frame_6{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px\n"
"}")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_33 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background:transparent;")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setLineWidth(0)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_8)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(u"font-size:14px;\n"
"font-weight:600;")

        self.horizontalLayout_34.addWidget(self.label_2)

        self.ComponentModelComboBox = QComboBox(self.frame_8)
        self.ComponentModelComboBox.setObjectName(u"ComponentModelComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ComponentModelComboBox.sizePolicy().hasHeightForWidth())
        self.ComponentModelComboBox.setSizePolicy(sizePolicy1)
        self.ComponentModelComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.ComponentModelComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_34.addWidget(self.ComponentModelComboBox)


        self.horizontalLayout_33.addWidget(self.frame_8)

        self.frame_12 = QFrame(self.frame_6)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setStyleSheet(u"background:transparent;")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.loadTerminalInferenceProject = QPushButton(self.frame_12)
        self.loadTerminalInferenceProject.setObjectName(u"loadTerminalInferenceProject")
        self.loadTerminalInferenceProject.setStyleSheet(u"QPushButton#loadTerminalInferenceProject{\n"
"	border:none;\n"
"	border-radius: 4px;\n"
"	border: 1px solid #b08bfd;\n"
"	background-color:#e1d9fe;\n"
"	color: #b08bfd;\n"
"	font-weight: bold;\n"
"	font-size:14px;\n"
"	padding: 8px;\n"
"	margin-right: 8px;\n"
"}\n"
"QPushButton#loadTerminalInferenceProject:hover{\n"
"	background-color:#b08bfd;\n"
"	color: #fff;\n"
"}")

        self.horizontalLayout_35.addWidget(self.loadTerminalInferenceProject)

        self.inferenceProjectPathLineEdit = QLineEdit(self.frame_12)
        self.inferenceProjectPathLineEdit.setObjectName(u"inferenceProjectPathLineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.inferenceProjectPathLineEdit.sizePolicy().hasHeightForWidth())
        self.inferenceProjectPathLineEdit.setSizePolicy(sizePolicy2)
        self.inferenceProjectPathLineEdit.setStyleSheet(u" background-color: rgba(255,255,255,90);\n"
"		color: rgba(0, 0, 0, 200);\n"
"		font: 600 14px \"Segoe UI\";\n"
"        border: 1px solid lightgray;\n"
"        border-radius: 4px;")
        self.inferenceProjectPathLineEdit.setReadOnly(True)

        self.horizontalLayout_35.addWidget(self.inferenceProjectPathLineEdit)

        self.generateComponentButton = QPushButton(self.frame_12)
        self.generateComponentButton.setObjectName(u"generateComponentButton")
        self.generateComponentButton.setStyleSheet(u"QPushButton#generateComponentButton{\n"
"	border:none;\n"
"	border-radius: 4px;\n"
"	border: 1px solid #b18bfd;\n"
"	background-color:#e1d9fe;\n"
"	color: #b18bfd;\n"
"	font-weight: bold;\n"
"	font-size:14px;\n"
"	padding: 8px;\n"
"	margin-left: 8px;\n"
"}\n"
"QPushButton#generateComponentButton:hover{\n"
"	background-color:#b18bfd;\n"
"	color: #fff;\n"
"}\n"
"QPushButton#generateComponentButton:disabled\n"
"{\n"
"	border:1px solid #9ea1b8;\n"
"    background-color:#9ea1b8;/*\u6539\u53d8\u80cc\u666f\u8272*/\n"
"    color: #fff;\n"
"}")

        self.horizontalLayout_35.addWidget(self.generateComponentButton)


        self.horizontalLayout_33.addWidget(self.frame_12)

        self.horizontalLayout_33.setStretch(0, 3)
        self.horizontalLayout_33.setStretch(1, 4)

        self.verticalLayout_22.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.ComponentGenerationFrame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_36.setSpacing(4)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_38 = QFrame(self.frame_7)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setStyleSheet(u"QFrame#frame_38{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"padding:4px;\n"
"}")
        self.frame_38.setFrameShape(QFrame.NoFrame)
        self.frame_38.setLineWidth(0)
        self.verticalLayout_23 = QVBoxLayout(self.frame_38)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_38)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        self.label_6.setStyleSheet(u"font: 600 14px \"Segoe UI\"; \n"
"font-weight:bold;\n"
"padding:4px;\n"
"background-color: transparent;")

        self.verticalLayout_23.addWidget(self.label_6)

        self.frame_43 = QFrame(self.frame_38)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setStyleSheet(u"background-color:transparent;\n"
"border-top:1px solid #fff;")
        self.frame_43.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_38 = QVBoxLayout(self.frame_43)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.graphvizInfo = QLabel(self.frame_43)
        self.graphvizInfo.setObjectName(u"graphvizInfo")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.graphvizInfo.sizePolicy().hasHeightForWidth())
        self.graphvizInfo.setSizePolicy(sizePolicy4)
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        self.graphvizInfo.setFont(font)
        self.graphvizInfo.setStyleSheet(u"QLabel#graphvizInfo{\n"
"font-family:Times New Roman,Microsoft YaHei;\n"
"border:none;\n"
"background:transparent;\n"
"}")
        self.graphvizInfo.setWordWrap(True)

        self.verticalLayout_38.addWidget(self.graphvizInfo)


        self.verticalLayout_23.addWidget(self.frame_43)


        self.horizontalLayout_36.addWidget(self.frame_38)

        self.frame_39 = QFrame(self.frame_7)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setStyleSheet(u"QFrame#frame_39{\n"
"background-color: rgb(238, 242, 255);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"padding:4px;\n"
"}")
        self.frame_39.setFrameShape(QFrame.NoFrame)
        self.frame_39.setLineWidth(0)
        self.verticalLayout_24 = QVBoxLayout(self.frame_39)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.frame_39)
        self.label_15.setObjectName(u"label_15")
        sizePolicy3.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy3)
        self.label_15.setStyleSheet(u"font: 600 14px \"Segoe UI\"; \n"
"font-weight:bold;\n"
"padding:4px;\n"
"background-color: transparent;")

        self.verticalLayout_24.addWidget(self.label_15)

        self.frame_40 = QFrame(self.frame_39)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setStyleSheet(u"border:none;\n"
"border-top:1px solid #fff;\n"
"background:transparent;")
        self.frame_40.setFrameShape(QFrame.NoFrame)
        self.frame_40.setLineWidth(0)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_37.setSpacing(0)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.frame_41 = QFrame(self.frame_40)
        self.frame_41.setObjectName(u"frame_41")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_41.sizePolicy().hasHeightForWidth())
        self.frame_41.setSizePolicy(sizePolicy5)
        self.frame_41.setMinimumSize(QSize(0, 0))
        self.frame_41.setMaximumSize(QSize(16777215, 16777215))
        self.frame_41.setStyleSheet(u"border:none;\n"
"border-right:1px solid #fff;")
        self.frame_41.setFrameShape(QFrame.NoFrame)
        self.frame_41.setLineWidth(0)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_38.setSpacing(0)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.modelInfoTreeWidget = QTreeWidget(self.frame_41)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.modelInfoTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.modelInfoTreeWidget.setObjectName(u"modelInfoTreeWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.modelInfoTreeWidget.sizePolicy().hasHeightForWidth())
        self.modelInfoTreeWidget.setSizePolicy(sizePolicy6)
        self.modelInfoTreeWidget.setMinimumSize(QSize(200, 0))
        font1 = QFont()
        self.modelInfoTreeWidget.setFont(font1)
        self.modelInfoTreeWidget.setStyleSheet(u"QTreeWidget QHeaderView::section {\n"
"   background-color: transparent;\n"
"	border:none;\n"
"	padding:4px;\n"
"	font-weight: bold;\n"
"	font-size: 14px;\n"
"}\n"
"QTreeWidget{\n"
"	border:none;\n"
"	font-size: 13px;\n"
"}")
        self.modelInfoTreeWidget.setFrameShape(QFrame.NoFrame)
        self.modelInfoTreeWidget.setLineWidth(1)
        self.modelInfoTreeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modelInfoTreeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modelInfoTreeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.modelInfoTreeWidget.setRootIsDecorated(True)
        self.modelInfoTreeWidget.setUniformRowHeights(False)
        self.modelInfoTreeWidget.setAnimated(True)
        self.modelInfoTreeWidget.setWordWrap(True)
        self.modelInfoTreeWidget.setHeaderHidden(True)
        self.modelInfoTreeWidget.header().setVisible(False)
        self.modelInfoTreeWidget.header().setCascadingSectionResizes(False)
        self.modelInfoTreeWidget.header().setDefaultSectionSize(200)
        self.modelInfoTreeWidget.header().setHighlightSections(True)
        self.modelInfoTreeWidget.header().setStretchLastSection(True)

        self.horizontalLayout_38.addWidget(self.modelInfoTreeWidget)


        self.horizontalLayout_37.addWidget(self.frame_41)

        self.frame_42 = QFrame(self.frame_40)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setStyleSheet(u"border:none;")
        self.frame_42.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_40.setSpacing(0)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.modelStructureInfo = QTextEdit(self.frame_42)
        self.modelStructureInfo.setObjectName(u"modelStructureInfo")
        self.modelStructureInfo.setStyleSheet(u"font-weight:bold;")
        self.modelStructureInfo.setReadOnly(True)

        self.horizontalLayout_40.addWidget(self.modelStructureInfo)


        self.horizontalLayout_37.addWidget(self.frame_42)


        self.verticalLayout_24.addWidget(self.frame_40)


        self.horizontalLayout_36.addWidget(self.frame_39)

        self.horizontalLayout_36.setStretch(0, 3)
        self.horizontalLayout_36.setStretch(1, 4)

        self.verticalLayout_22.addWidget(self.frame_7)


        self.horizontalLayout.addWidget(self.ComponentGenerationFrame)


        self.retranslateUi(ComponentGenerateWidget)

        QMetaObject.connectSlotsByName(ComponentGenerateWidget)
    # setupUi

    def retranslateUi(self, ComponentGenerateWidget):
        ComponentGenerateWidget.setWindowTitle(QCoreApplication.translate("ComponentGenerateWidget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("ComponentGenerateWidget", u"\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.loadTerminalInferenceProject.setText(QCoreApplication.translate("ComponentGenerateWidget", u"\u5bfc\u5165\u63a8\u7406\u6a21\u677f", None))
        self.generateComponentButton.setText(QCoreApplication.translate("ComponentGenerateWidget", u"\u751f\u6210\u6784\u4ef6", None))
        self.label_6.setText(QCoreApplication.translate("ComponentGenerateWidget", u"Model Architecture", None))
        self.graphvizInfo.setText("")
        self.label_15.setText(QCoreApplication.translate("ComponentGenerateWidget", u"Model Information", None))
    # retranslateUi

