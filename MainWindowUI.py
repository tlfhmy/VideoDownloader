# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.info_Browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.info_Browser.setObjectName("info_Browser")
        self.gridLayout.addWidget(self.info_Browser, 3, 1, 2, 3)
        self.url_Label = QtWidgets.QLabel(self.centralwidget)
        self.url_Label.setObjectName("url_Label")
        self.gridLayout.addWidget(self.url_Label, 1, 0, 1, 1)
        self.info_Label = QtWidgets.QLabel(self.centralwidget)
        self.info_Label.setObjectName("info_Label")
        self.gridLayout.addWidget(self.info_Label, 3, 0, 1, 1)
        self.source_Label = QtWidgets.QLabel(self.centralwidget)
        self.source_Label.setObjectName("source_Label")
        self.gridLayout.addWidget(self.source_Label, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.resolve_Button = QtWidgets.QPushButton(self.centralwidget)
        self.resolve_Button.setObjectName("resolve_Button")
        self.gridLayout.addWidget(self.resolve_Button, 1, 2, 1, 1)
        self.source_Box = QtWidgets.QComboBox(self.centralwidget)
        self.source_Box.setObjectName("source_Box")
        self.gridLayout.addWidget(self.source_Box, 2, 1, 1, 1)
        self.save_Label = QtWidgets.QLabel(self.centralwidget)
        self.save_Label.setObjectName("save_Label")
        self.gridLayout.addWidget(self.save_Label, 0, 0, 1, 1)
        self.url_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.url_Edit.setObjectName("url_Edit")
        self.gridLayout.addWidget(self.url_Edit, 1, 1, 1, 1)
        self.save_Button = QtWidgets.QPushButton(self.centralwidget)
        self.save_Button.setObjectName("save_Button")
        self.gridLayout.addWidget(self.save_Button, 0, 2, 1, 1)
        self.download_Button = QtWidgets.QPushButton(self.centralwidget)
        self.download_Button.setObjectName("download_Button")
        self.gridLayout.addWidget(self.download_Button, 5, 2, 1, 1)
        self.save_Box = QtWidgets.QComboBox(self.centralwidget)
        self.save_Box.setObjectName("save_Box")
        self.gridLayout.addWidget(self.save_Box, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.url_Label.setText(_translate("MainWindow", "视频链接:"))
        self.info_Label.setText(_translate("MainWindow", "视频信息:"))
        self.source_Label.setText(_translate("MainWindow", "视频源:"))
        self.resolve_Button.setText(_translate("MainWindow", "解析"))
        self.save_Label.setText(_translate("MainWindow", "视频保存位置:"))
        self.save_Button.setText(_translate("MainWindow", "选择"))
        self.download_Button.setText(_translate("MainWindow", "下载"))

