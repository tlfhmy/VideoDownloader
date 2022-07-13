import sys
import DownloaderWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DownloaderWidget.DownloaderWidget()
    mainWindow.show()
    sys.exit(app.exec_())