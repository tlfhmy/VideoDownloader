from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.Qt import QThread, QMutex, pyqtSignal, pyqtSlot
import downloader
import json
import os, time

class ResolveURL_Thread(QThread):
    completeSignal = pyqtSignal(list)
    
    def __init__(self, you_get_downloader):
        super(ResolveURL_Thread, self).__init__()
        self.you_get_downloader = you_get_downloader

    def run(self):
        res = self.you_get_downloader.format_list()
        self.completeSignal.emit(res)

class Download_Thread(QThread):
    completeSignal = pyqtSignal()

    def __init__(self):
        super(Download_Thread, self).__init__()

    def run(self):
        pass

class DownloaderWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(DownloaderWidget, self).__init__()
        self.uiSetting()
        self.historyPaths = set()
        self.setSlots()
        self.readHistory()
        self.youGetDownloader = None
        self.video_sources_dicr = {}

    def uiSetting(self):
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.info_Label = QtWidgets.QLabel(self.centralwidget)
        self.info_Label.setObjectName("info_Label")
        self.gridLayout.addWidget(self.info_Label, 5, 0, 1, 1)
        self.url_Label = QtWidgets.QLabel(self.centralwidget)
        self.url_Label.setObjectName("url_Label")
        self.gridLayout.addWidget(self.url_Label, 1, 0, 1, 1)
        self.url_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.url_Edit.setObjectName("url_Edit")
        self.gridLayout.addWidget(self.url_Edit, 1, 1, 1, 1)
        self.source_Button = QtWidgets.QPushButton(self.centralwidget)
        self.source_Button.setObjectName("source_Button")
        self.gridLayout.addWidget(self.source_Button, 2, 2, 1, 1)
        self.download_Button = QtWidgets.QPushButton(self.centralwidget)
        self.download_Button.setObjectName("download_Button")
        self.gridLayout.addWidget(self.download_Button, 7, 2, 1, 1)
        self.save_Button = QtWidgets.QPushButton(self.centralwidget)
        self.save_Button.setObjectName("save_Button")
        self.gridLayout.addWidget(self.save_Button, 0, 2, 1, 1)
        self.save_Label = QtWidgets.QLabel(self.centralwidget)
        self.save_Label.setObjectName("save_Label")
        self.gridLayout.addWidget(self.save_Label, 0, 0, 1, 1)
        self.resolve_Button = QtWidgets.QPushButton(self.centralwidget)
        self.resolve_Button.setObjectName("resolve_Button")
        self.gridLayout.addWidget(self.resolve_Button, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.source_Label = QtWidgets.QLabel(self.centralwidget)
        self.source_Label.setObjectName("source_Label")
        self.gridLayout.addWidget(self.source_Label, 2, 0, 1, 1)
        self.port_Label = QtWidgets.QLabel(self.centralwidget)
        self.port_Label.setObjectName("port_Label")
        self.gridLayout.addWidget(self.port_Label, 4, 0, 1, 1)
        self.proxy_CheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.proxy_CheckBox.setObjectName("proxy_CheckBox")
        self.gridLayout.addWidget(self.proxy_CheckBox, 4, 2, 1, 1)
        self.source_Box = QtWidgets.QComboBox(self.centralwidget)
        self.source_Box.setObjectName("source_Box")
        self.gridLayout.addWidget(self.source_Box, 2, 1, 1, 1)
        self.save_Box = QtWidgets.QComboBox(self.centralwidget)
        self.save_Box.setObjectName("save_Box")
        self.gridLayout.addWidget(self.save_Box, 0, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.spinBox.setReadOnly(True)
        self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBox.setAccelerated(False)
        self.spinBox.setMaximum(65536)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 4, 1, 1, 1)
        self.info_Browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.info_Browser.setObjectName("info_Browser")
        self.gridLayout.addWidget(self.info_Browser, 5, 1, 2, 3)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 759, 24))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "视频下载器"))
        self.info_Label.setText(_translate("MainWindow", "视频信息:"))
        self.url_Label.setText(_translate("MainWindow", "视频链接:"))
        self.source_Button.setText(_translate("MainWindow", "确认"))
        self.download_Button.setText(_translate("MainWindow", "下载"))
        self.save_Button.setText(_translate("MainWindow", "选择"))
        self.save_Label.setText(_translate("MainWindow", "视频保存位置:"))
        self.resolve_Button.setText(_translate("MainWindow", "解析"))
        self.source_Label.setText(_translate("MainWindow", "视频源:"))
        self.port_Label.setText(_translate("MainWindow", "端口号："))
        self.proxy_CheckBox.setText(_translate("MainWindow", "使用代理"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.saveHistory()

    def resolveURL(self):
        url = self.url_Edit.text()
        if url == '':
            QMessageBox.information(self,
                                    'URL错误',
                                    '请填写URL',
                                    QMessageBox.Yes)
            return 

        if self.youGetDownloader is None:
            savePath = self.save_Box.currentText()
            if savePath == '':
                QMessageBox.information(self,
                                        '文件保存路径',
                                        '请选择将下载的视频文件的保存路径！',
                                        QMessageBox.Yes)
                return

        if self.proxy_CheckBox.checkState():
            self.youGetDownloader = downloader.YouGet(savePath, self.spinBox.value())
        else:
            self.youGetDownloader = downloader.YouGet(savePath)
        self.youGetDownloader.set_url(url)

        self.resolve_Button.setEnabled(False)
        self.resolveWorker = ResolveURL_Thread(self.youGetDownloader)
        self.resolveWorker.completeSignal.connect(self.getVideoSourceList)
        self.resolveWorker.start()



    @pyqtSlot(list)
    def getVideoSourceList(self, res):
        self.video_sources_dicr = {}
        for i, ele in enumerate(res):
            self.video_sources_dicr[f'视频源{i + 1}: {ele.quality}'] = ele

        for k in self.video_sources_dicr.keys():
            self.source_Box.addItem(k)

        self.resolve_Button.setEnabled(True)


    def select_source(self):
        self.info_Browser.clear()
        video_source = self.source_Box.currentText()
        self.info_Browser.setText(str(self.video_sources_dicr[video_source]))

    def checkPort(self):
        self.spinBox.setReadOnly(not self.proxy_CheckBox.checkState())

    def saveHistory(self):
        dict = {'paths':[]}
        for ele in self.historyPaths:
            dict['paths'].append(ele)
        dict['proxy_enable'] = self.proxy_CheckBox.checkState()
        dict['proxy_port'] = self.spinBox.value()

        cont = json.dumps(dict, indent=2)
        with open('./history.ini', 'w') as f:
            f.write(cont)


    def readHistory(self):
        if not os.path.exists("./history.ini"):
            with open("./history.ini", "w"):
                return
        with open("./history.ini", 'r') as f:
            try:
                cont = f.read()
                his_paths = json.loads(cont)
                for path in his_paths['paths']:
                    self.save_Box.addItem(path)
                    self.historyPaths.add(path)
                if 'proxy_enable' in his_paths:
                    self.proxy_CheckBox.setCheckState(his_paths['proxy_enable'])
                    self.spinBox.setValue(his_paths['proxy_port'])
                    self.spinBox.setReadOnly(not self.proxy_CheckBox.checkState())
            except:
                QMessageBox.warning(self, '历史文件内容错误！',
                                    'history.ini文件存在问题, 将清空并覆写历史文件！',
                                    QMessageBox.Yes)

    def setSlots(self):
        self.save_Button.clicked.connect(self.openPath)
        self.resolve_Button.clicked.connect(self.resolveURL)
        self.source_Button.clicked.connect(self.select_source)
        self.proxy_CheckBox.stateChanged.connect(self.checkPort)

    def openPath(self):
        openPathName = QFileDialog.getExistingDirectory(self, '选取文件夹')
        self.save_Box.addItem(openPathName)
        self.historyPaths.add(openPathName)