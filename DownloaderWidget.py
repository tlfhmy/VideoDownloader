from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.Qt import QThread, QMutex, pyqtSignal, pyqtSlot
import downloader
import json
import os


"""
解析视频源的线程, 它将解析结果通过自定义信号发送给主进程
"""
class ResolveURL_Thread(QThread):
    completeSignal = pyqtSignal(list)
    
    def __init__(self, you_get_downloader):
        super(ResolveURL_Thread, self).__init__()
        self.you_get_downloader = you_get_downloader

    def run(self):
        res = self.you_get_downloader.format_list()
        self.completeSignal.emit(res)


"""
视频下载子进程, 下载进度信息通过信号发送给主进程
"""
class Download_Thread(QThread):
    completeSignal = pyqtSignal(str)

    def __init__(self, you_get_downloader, itag):
        super(Download_Thread, self).__init__()
        self.youGetDownloader = you_get_downloader
        self.itag = itag

    def run(self):
        download_info_io = self.youGetDownloader.download(self.itag)
        tmp_line = bytearray()
        while download_info_io.poll() is None:
            a = download_info_io.stdout.read(1)
            if a in [b'\r', b'\n']:
                tmp_line.extend(a)
                res = tmp_line.decode('utf-8')
                self.completeSignal.emit(res.strip())
                tmp_line = bytearray()
            else:
                tmp_line.extend(a)
        self.completeSignal.emit("Download Completed!")


class DownloaderWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(DownloaderWidget, self).__init__()
        self.uiSetting()
        self.historyPaths = set()
        self.setSlots()
        self.readHistory()
        self.youGetDownloader = None
        self.video_sources_dict = {}
        self.initButton()

    """
    UI的布局代码, 通过QtDesigner生成并作出适当的修改以适合本自定义类
    """
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

    """
    关闭程序时, 存储历史信息(主要为视频存储路径和代理端口信息)
    """
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.saveHistory()

    def resolveURL(self):
        """
        按下解析按钮
        解析指定的URL的视频信息, 在此过程中会创建you-get下载类的对象, 并初步初始化存储视频地址
        以及URL信息
        :return: None
        """
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

        #根据检测框是否勾选, 决定是否使用代理
        if self.proxy_CheckBox.checkState():
            self.youGetDownloader = downloader.YouGet(savePath, self.spinBox.value())
        else:
            self.youGetDownloader = downloader.YouGet(savePath)
        self.youGetDownloader.set_url(url)

        #开启解析视频url地址, 解析过程中需要禁用解析按钮
        self.resolve_Button.setEnabled(False)
        self.resolveWorker = ResolveURL_Thread(self.youGetDownloader)
        self.resolveWorker.completeSignal.connect(self.getVideoSourceList)
        self.resolveWorker.start()



    @pyqtSlot(list)
    def getVideoSourceList(self, res):
        """
        通过信号获取到视频源的解析结果, 将结果存储到下拉菜单中
        :param res: list 解析结果列表
        :return: None
        """
        self.video_sources_dict = {}
        for i, ele in enumerate(res):
            self.video_sources_dict[f'视频源{i + 1}: {ele.quality}'] = ele

        for k in self.video_sources_dict.keys():
            self.source_Box.addItem(k)

        self.resolve_Button.setEnabled(True)
        self.source_Button.setEnabled(True)

    @pyqtSlot(str)
    def getDownloadInfo(self, res):
        """
        开始下载文件, 接受传入的下载进度信息并显示在TextBrowser中
        恢复解析、确认及下载按钮
        :param res: str文件下载的进度信息
        :return: None
        """
        if res == "Download Completed!":
            self.source_Button.setEnabled(True)
            self.resolve_Button.setEnabled(True)
            self.download_Button.setEnabled(True)
        else:
            self.info_Browser.append(res)


    def select_source(self):
        """
        确认视频源的按钮, 选定解析的视频源并进行下载器的进一步的设置
        :return: None
        """
        self.info_Browser.clear()
        video_source = self.source_Box.currentText()
        self.info_Browser.setText(str(self.video_sources_dict[video_source]))

        dir_name = ""
        for ch in self.video_sources_dict[video_source].title:
            if ch in ' @#$%^&*{}}|?><\\/':
                dir_name += "_"
            else:
                dir_name += ch
        video_save_path = self.save_Box.currentText() + "/" + dir_name
        if not os.path.exists(video_save_path):
            os.mkdir(video_save_path)
        self.youGetDownloader.Savepath = video_save_path
        self.download_Button.setEnabled(True)


    def checkPort(self):
        """
        如果端口复选框未选中, 则端口设定spinBox不能修改
        反之则可以
        :return: None
        """
        self.spinBox.setReadOnly(not self.proxy_CheckBox.checkState())


    def download_video(self):
        """
        开始下载视频, 并显示下载进度
        下载过程中禁用解析、确认及下载按钮
        :return:
        """
        self.info_Browser.clear()
        self.download_Button.setEnabled(False)
        self.source_Button.setEnabled(False)
        self.resolve_Button.setEnabled(False)
        video_source = self.source_Box.currentText()
        self.downloadWorker = Download_Thread(self.youGetDownloader, int(self.video_sources_dict[video_source].flag))
        self.downloadWorker.completeSignal.connect(self.getDownloadInfo)
        self.downloadWorker.start()



    def saveHistory(self):
        """
        存储一些设置, 以便下一次运行软件可以复用
        :return: None
        """
        dict = {'paths':[]}
        for ele in self.historyPaths:
            dict['paths'].append(ele)
        dict['proxy_enable'] = self.proxy_CheckBox.checkState()
        dict['proxy_port'] = self.spinBox.value()

        cont = json.dumps(dict, indent=2)
        with open('./history.ini', 'w') as f:
            f.write(cont)


    def readHistory(self):
        """
        软件打开, 则读取并加载历史记录文件
        如果历史文件被破坏则重建
        :return: None
        """
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
        """
        初始化信号与槽的连接
        :return: None
        """
        self.save_Button.clicked.connect(self.openPath)
        self.resolve_Button.clicked.connect(self.resolveURL)
        self.source_Button.clicked.connect(self.select_source)
        self.proxy_CheckBox.stateChanged.connect(self.checkPort)
        self.download_Button.clicked.connect(self.download_video)


    def openPath(self):
        """
        选取文件对话框
        :return: None
        """
        openPathName = QFileDialog.getExistingDirectory(self, '选取文件夹')
        self.save_Box.addItem(openPathName)
        self.historyPaths.add(openPathName)

    def initButton(self):
        """
        URL解析完成前保持确认按钮非激活状态
        :return: None
        """
        self.source_Button.setEnabled(False)
        self.download_Button.setEnabled(False)
