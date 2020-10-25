import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import psutil
from cpuinfo import get_cpu_info


#gui fike
from ui_main import Ui_MainWindow

#import functions
from ui_functions import *

counter = 0
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_3 = self.cpuBrand()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh)

        self.timer.start(500)

        
      
        #move window
        def moveWindow(event):
            #restore before move
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximixe_restore(self)

            #if left click move window
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()


        #set title bar
        self.ui.title_bar.mouseMoveEvent = moveWindow
        
        #set ui definitions
        UIFunctions.uiDefinitions(self)

        self.show()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    

    def refresh(self):
        #cpuRefresh
        value = psutil.cpu_percent()
        self.ui.label_2.setText(str(value)+"%")

        # temp = psutil.sensors_temperatures()
        # print(temp)

        #gpuRefresh
        # value = psutil.gpu_percent()
        self.ui.label_6.setText(str(value)+"%")    
        
        value3 = psutil.virtual_memory()
        value3a = f"{(value3[3]/(1024**3)):.1f}"
        #value3aa = f"{value3a:.1f}"  
        self.ui.label_10.setText(str(value3a)+"GB")


    def cpuBrand(self):
        proc = get_cpu_info()
        cB = proc["brand_raw"]
        self.ui.label_3.setText(cB)

# 'brand_raw': 'AMD Ryzen 5 1600 Six-Core Processor'
# 'hz_actual_friendly': '3.2000 GHz'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())





