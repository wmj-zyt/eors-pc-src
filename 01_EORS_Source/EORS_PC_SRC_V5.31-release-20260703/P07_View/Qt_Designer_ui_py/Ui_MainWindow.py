# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
from . import image_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        icon = QIcon()
        icon.addFile(u":/img/images/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(238, 242, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 6, 0)
        self.leftContainer = QFrame(self.centralwidget)
        self.leftContainer.setObjectName(u"leftContainer")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftContainer.sizePolicy().hasHeightForWidth())
        self.leftContainer.setSizePolicy(sizePolicy)
        self.leftContainer.setMinimumSize(QSize(60, 0))
        self.leftContainer.setMaximumSize(QSize(80, 16777215))
        self.leftContainer.setStyleSheet(u"QFrame {\n"
"    background-color:#9265F4;  /* \u6de1\u7d2b\u8272 */\n"
"    margin: 0px;               /* \u65e0\u5916\u95f4\u8ddd */\n"
"    padding: 0px;              /* \u65e0\u5185\u95f4\u8ddd */\n"
"    border: none;              /* \u65e0\u8fb9\u6846 */\n"
"}\n"
"")
        self.leftContainer.setFrameShape(QFrame.StyledPanel)
        self.leftContainer.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.leftContainer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.logo = QWidget(self.leftContainer)
        self.logo.setObjectName(u"logo")
        self.logo.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(50, 50))
        self.logo.setMaximumSize(QSize(100, 100))
        self.logo.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
"image: url(:/img/images/soochow01.png);\n"
"border:2px solid rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"")

        self.gridLayout.addWidget(self.logo, 0, 0, 1, 1)

        self.softwareHelp = QPushButton(self.leftContainer)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.softwareHelp)
        self.softwareHelp.setObjectName(u"softwareHelp")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.softwareHelp.sizePolicy().hasHeightForWidth())
        self.softwareHelp.setSizePolicy(sizePolicy2)
        self.softwareHelp.setMinimumSize(QSize(50, 40))
        self.softwareHelp.setStyleSheet(u"/* \u900f\u660e\u80cc\u666f */\n"
"QPushButton {\n"
"	background-image:url(:/img/images/info.png);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"	background-repeat: no-repeat;\n"
"	background-position: center;\n"
"	border: none;\n"
"	padding: 0px;\n"
"	border-left:  solid transparent;\n"
"	color: rgba(255, 255, 255, 199);\n"
"	margin: 0px;\n"
"    border-radius: 7px;  /* \u5706\u89d2\u534a\u5f84\uff0c\u503c\u8d8a\u5927\u8d8a\u5706 */\n"
"\n"
"}\n"
"\n"
"QPushButton:hover,QPushButton:focus{\n"
"	background-color: #7942F0;\n"
"}")
        self.softwareHelp.setCheckable(True)
        self.softwareHelp.setChecked(True)
        self.softwareHelp.setAutoExclusive(True)

        self.gridLayout.addWidget(self.softwareHelp, 8, 0, 1, 1)

        self.dataAcquisition = QPushButton(self.leftContainer)
        self.buttonGroup.addButton(self.dataAcquisition)
        self.dataAcquisition.setObjectName(u"dataAcquisition")
        sizePolicy2.setHeightForWidth(self.dataAcquisition.sizePolicy().hasHeightForWidth())
        self.dataAcquisition.setSizePolicy(sizePolicy2)
        self.dataAcquisition.setMinimumSize(QSize(50, 45))
        self.dataAcquisition.setStyleSheet(u"/* \u900f\u660e\u80cc\u666f */\n"
"QPushButton {\n"
"	background-image:url(:/img/images/uploadImg.png);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"	background-repeat: no-repeat;\n"
"	background-position: center;\n"
"	border: none;\n"
"	padding: 0px;\n"
"	border-left:  solid transparent;\n"
"	color: rgba(255, 255, 255, 199);\n"
"	margin: 0px;\n"
"    border-radius: 7px;  /* \u5706\u89d2\u534a\u5f84\uff0c\u503c\u8d8a\u5927\u8d8a\u5706 */\n"
"\n"
"}\n"
"\n"
"QPushButton:hover,QPushButton:focus{\n"
"background-color: #7942F0;\n"
"}\n"
"/* \u53ef\u9009\uff1a\u901a\u8fc7\u4f2a\u5143\u7d20\u6dfb\u52a0\u60ac\u6d6e\u63d0\u793a */\n"
"QPushButton:hover::after {\n"
"    content: \"\u60ac\u6d6e\u63d0\u793a\u6587\u5b57\";    /* \u4ec5\u90e8\u5206Qt\u7248\u672c\u652f\u6301 */\n"
"}\n"
"QPushButton[selected=\"true\"] {\n"
"}")
        self.dataAcquisition.setCheckable(True)
        self.dataAcquisition.setChecked(False)
        self.dataAcquisition.setAutoExclusive(True)
        self.dataAcquisition.setAutoDefault(True)

        self.gridLayout.addWidget(self.dataAcquisition, 3, 0, 1, 1)

        self.modelPredict = QPushButton(self.leftContainer)
        self.modelPredict.setObjectName(u"modelPredict")
        self.modelPredict.setMinimumSize(QSize(50, 45))
        self.modelPredict.setStyleSheet(u"/* \u900f\u660e\u80cc\u666f */\n"
"QPushButton {\n"
"	background-image:url(:/img/images/\u6a21\u578b\u63a8\u7406.png);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"	background-repeat: no-repeat;\n"
"	background-position: center;\n"
"	border: none;\n"
"	padding: 0px;\n"
"	border-left:  solid transparent;\n"
"	color: rgba(255, 255, 255, 199);\n"
"	margin: 0px;\n"
"    border-radius: 7px;  /* \u5706\u89d2\u534a\u5f84\uff0c\u503c\u8d8a\u5927\u8d8a\u5706 */\n"
"\n"
"}\n"
"\n"
"QPushButton:hover,QPushButton:focus{\n"
"background-color: #7942F0;\n"
"}\n"
"/* \u53ef\u9009\uff1a\u901a\u8fc7\u4f2a\u5143\u7d20\u6dfb\u52a0\u60ac\u6d6e\u63d0\u793a */\n"
"QPushButton:hover::after {\n"
"    content: \"\u60ac\u6d6e\u63d0\u793a\u6587\u5b57\";    /* \u4ec5\u90e8\u5206Qt\u7248\u672c\u652f\u6301 */\n"
"}")

        self.gridLayout.addWidget(self.modelPredict, 5, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 0, 1, 1)

        self.modelTraining = QPushButton(self.leftContainer)
        self.buttonGroup.addButton(self.modelTraining)
        self.modelTraining.setObjectName(u"modelTraining")
        self.modelTraining.setMinimumSize(QSize(50, 45))
        self.modelTraining.setStyleSheet(u"/* \u900f\u660e\u80cc\u666f */\n"
"QPushButton {\n"
"	background-image:url(:/img/images/\u6a21\u578b\u8bad\u7ec3.png);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"	background-repeat: no-repeat;\n"
"	background-position: center;\n"
"	border: none;\n"
"	padding: 0px;\n"
"	border-left:  solid transparent;\n"
"	color: rgba(255, 255, 255, 199);\n"
"	margin: 0px;\n"
"    border-radius: 7px;  /* \u5706\u89d2\u534a\u5f84\uff0c\u503c\u8d8a\u5927\u8d8a\u5706 */\n"
"\n"
"}\n"
"\n"
"QPushButton:hover,QPushButton:focus{\n"
"background-color: #7942F0;\n"
"}\n"
"/* \u53ef\u9009\uff1a\u901a\u8fc7\u4f2a\u5143\u7d20\u6dfb\u52a0\u60ac\u6d6e\u63d0\u793a */\n"
"QPushButton:hover::after {\n"
"    content: \"\u60ac\u6d6e\u63d0\u793a\u6587\u5b57\";    /* \u4ec5\u90e8\u5206Qt\u7248\u672c\u652f\u6301 */\n"
"}")
        self.modelTraining.setAutoExclusive(False)

        self.gridLayout.addWidget(self.modelTraining, 4, 0, 1, 1)

        self.componentGeneration = QPushButton(self.leftContainer)
        self.componentGeneration.setObjectName(u"componentGeneration")
        self.componentGeneration.setMinimumSize(QSize(50, 45))
        self.componentGeneration.setStyleSheet(u"/* \u900f\u660e\u80cc\u666f */\n"
"QPushButton {\n"
"	background-image:url(:/img/images/\u751f\u6210\u6784\u4ef6.png);\n"
"    background-color: transparent;\n"
"    border: none;\n"
"	background-repeat: no-repeat;\n"
"	background-position: center;\n"
"	border: none;\n"
"	padding: 0px;\n"
"	border-left:  solid transparent;\n"
"	color: rgba(255, 255, 255, 199);\n"
"	margin: 0px;\n"
"    border-radius: 7px;  /* \u5706\u89d2\u534a\u5f84\uff0c\u503c\u8d8a\u5927\u8d8a\u5706 */\n"
"\n"
"}\n"
"\n"
"QPushButton:hover,QPushButton:focus{\n"
"background-color: #7942F0;\n"
"}\n"
"/* \u53ef\u9009\uff1a\u901a\u8fc7\u4f2a\u5143\u7d20\u6dfb\u52a0\u60ac\u6d6e\u63d0\u793a */\n"
"QPushButton:hover::after {\n"
"    content: \"\u60ac\u6d6e\u63d0\u793a\u6587\u5b57\";    /* \u4ec5\u90e8\u5206Qt\u7248\u672c\u652f\u6301 */\n"
"}")

        self.gridLayout.addWidget(self.componentGeneration, 6, 0, 1, 1)


        self.horizontalLayout.addWidget(self.leftContainer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QFrame(self.centralwidget)
        self.header.setObjectName(u"header")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy3)
        self.header.setMinimumSize(QSize(0, 30))
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.appDesc = QLabel(self.header)
        self.appDesc.setObjectName(u"appDesc")
        self.appDesc.setMinimumSize(QSize(0, 20))
        self.appDesc.setStyleSheet(u"font: 700 italic 11pt \"Segoe UI\";\n"
"border:none;\n"
"border-bottom:1px solid #e2e9f7;")

        self.horizontalLayout_2.addWidget(self.appDesc)


        self.verticalLayout.addWidget(self.header)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(30, 30))
        self.stackedWidget.setStyleSheet(u"/* StackedWidget \u6837\u5f0f */\n"
"QStackedWidget {\n"
"    background-color: rgba(255, 255, 255, 0.9);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* StackedWidget \u4e2d\u7684\u9875\u9762\u5185\u5bb9\u533a\u57df */\n"
"QStackedWidget > QWidget {\n"
"    background-color: transparent;\n"
"    border-radius: 4px;\n"
"}")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.footer = QFrame(self.centralwidget)
        self.footer.setObjectName(u"footer")
        sizePolicy1.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy1)
        self.footer.setMinimumSize(QSize(0, 0))
        self.footer.setStyleSheet(u"border:none;border-top:1px solid #e2e9f7;")
        self.footer.setFrameShape(QFrame.StyledPanel)
        self.footer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.footer)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.statusBar = QLabel(self.footer)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setStyleSheet(u"font: 700 11pt \"Segoe UI\";\n"
"color: rgba(0, 0, 0, 140);")

        self.horizontalLayout_3.addWidget(self.statusBar)


        self.verticalLayout.addWidget(self.footer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 13)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.dataAcquisition.setDefault(True)
        self.modelTraining.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EORS", None))
#if QT_CONFIG(tooltip)
        self.softwareHelp.setToolTip(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
#endif // QT_CONFIG(tooltip)
        self.softwareHelp.setText("")
#if QT_CONFIG(tooltip)
        self.dataAcquisition.setToolTip(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u83b7\u53d6", None))
#endif // QT_CONFIG(tooltip)
        self.dataAcquisition.setText("")
#if QT_CONFIG(tooltip)
        self.modelPredict.setToolTip(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u63a8\u7406", None))
#endif // QT_CONFIG(tooltip)
        self.modelPredict.setText("")
#if QT_CONFIG(tooltip)
        self.modelTraining.setToolTip(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u8bad\u7ec3", None))
#endif // QT_CONFIG(tooltip)
        self.modelTraining.setText("")
#if QT_CONFIG(tooltip)
        self.componentGeneration.setToolTip(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u6784\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.componentGeneration.setText("")
        self.appDesc.setText(QCoreApplication.translate("MainWindow", u"\u8fd9\u91cc\u662f\u8f6f\u4ef6\u7248\u672c\u4fe1\u606f", None))
        self.statusBar.setText(QCoreApplication.translate("MainWindow", u"\u8fd9\u91cc\u662f\u72b6\u6001\u680f", None))
    # retranslateUi

