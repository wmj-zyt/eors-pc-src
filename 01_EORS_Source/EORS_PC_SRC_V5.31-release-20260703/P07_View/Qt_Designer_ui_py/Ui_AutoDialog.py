# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AutoDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(669, 488)
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.info_label = QLabel(Dialog)
        self.info_label.setObjectName(u"info_label")

        self.verticalLayout.addWidget(self.info_label)

        self.example_label = QLabel(Dialog)
        self.example_label.setObjectName(u"example_label")
        self.example_label.setStyleSheet(u"color: gray; font-size: 10px;")

        self.verticalLayout.addWidget(self.example_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_frame = QFrame(Dialog)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setFrameShape(QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.left_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.input_label = QLabel(self.left_frame)
        self.input_label.setObjectName(u"input_label")

        self.verticalLayout_2.addWidget(self.input_label)

        self.text_edit = QTextEdit(self.left_frame)
        self.text_edit.setObjectName(u"text_edit")

        self.verticalLayout_2.addWidget(self.text_edit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_btn = QPushButton(self.left_frame)
        self.add_btn.setObjectName(u"add_btn")

        self.horizontalLayout_2.addWidget(self.add_btn)

        self.clear_btn = QPushButton(self.left_frame)
        self.clear_btn.setObjectName(u"clear_btn")

        self.horizontalLayout_2.addWidget(self.clear_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.updata_btn = QPushButton(self.left_frame)
        self.updata_btn.setObjectName(u"updata_btn")

        self.verticalLayout_2.addWidget(self.updata_btn)

        self.ok_btn = QPushButton(self.left_frame)
        self.ok_btn.setObjectName(u"ok_btn")

        self.verticalLayout_2.addWidget(self.ok_btn)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.left_frame)

        self.right_frame = QFrame(Dialog)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setFrameShape(QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.right_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.preview_label = QLabel(self.right_frame)
        self.preview_label.setObjectName(u"preview_label")

        self.verticalLayout_3.addWidget(self.preview_label)

        self.table_widget = QTableWidget(self.right_frame)
        if (self.table_widget.columnCount() < 4):
            self.table_widget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_widget.setObjectName(u"table_widget")
        self.table_widget.setColumnCount(4)

        self.verticalLayout_3.addWidget(self.table_widget)

        self.cancel_btn = QPushButton(self.right_frame)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.verticalLayout_3.addWidget(self.cancel_btn)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.right_frame)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 10)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u81ea\u52a8\u8bad\u7ec3\u53c2\u6570\u8bbe\u7f6e", None))
        self.info_label.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u8f93\u5165\u8bad\u7ec3\u53c2\u6570\u7ec4\u5408\uff08\u6bcf\u884c\u4e00\u7ec4\u53c2\u6570\uff0c\u683c\u5f0f\uff1a\u8f6e\u6570,\u6279\u91cf\u5927\u5c0f,\u5b66\u4e60\u7387\uff09", None))
        self.example_label.setText(QCoreApplication.translate("Dialog", u"\u793a\u4f8b\uff1a100,16,0.0001  \uff08\u8868\u793a\uff1a100\u8f6e\uff0c\u6279\u91cf16\uff0c\u5b66\u4e60\u73870.0001\uff09", None))
        self.input_label.setText(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u8f93\u5165\uff1a", None))
        self.text_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"\"\u8bf7\u8f93\u5165\u53c2\u6570\u7ec4\u5408\uff0c\u6bcf\u884c\u4e00\u7ec4\uff1a\\n100,16,0.0001\\n200,32,0.0002\\n300,16,0.0001\"", None))
        self.add_btn.setText(QCoreApplication.translate("Dialog", u"\u6dfb\u52a0\u793a\u4f8b\u53c2\u6570", None))
        self.clear_btn.setText(QCoreApplication.translate("Dialog", u"\u6e05\u7a7a", None))
        self.updata_btn.setText(QCoreApplication.translate("Dialog", u"\u66f4\u65b0\u53c2\u6570", None))
        self.ok_btn.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.preview_label.setText(QCoreApplication.translate("Dialog", u"\u53c2\u6570\u9884\u89c8\uff1a", None))
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\u5e8f\u53f7", None));
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u8bad\u7ec3\u8f6e\u6570", None));
        ___qtablewidgetitem2 = self.table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"\u6279\u91cf\u5927\u5c0f", None));
        ___qtablewidgetitem3 = self.table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"\u5b66\u4e60\u7387", None));
        self.cancel_btn.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

