import sys
import platform

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

import psutil
from cpuinfo import get_cpu_info
import wmi
import GPUtil


#gui fike
from ui_main2 import Ui_MainWindow

#import functions
from ui_functions import *

counter = 0

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.computer = wmi.WMI()
        self.proc = get_cpu_info()
        

        self.ui.label_3 = self.cpuBrand()
        self.ui.label_11 = self.totalRam()
        self.ui.label_7 = self.gpuBrand()
        self.ui.label_14 = self.mother()


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

    # def back(self):
    #     back = self.computer.Win32_Processor()[0]
    #     bBrand = back.Manufacturer
    #     if bBrand == "AuthenticAMD":



        
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    

    def refresh(self):
        #cpuRefresh
        value = psutil.cpu_percent()
        self.ui.label_2.setText(str(value)+"%")

        # temp = psutil.sensors_temperatures()
        # print(temp)

        #gpuRefresh
        gpu = GPUtil.getGPUs()
        for gpuV in gpu:
            value2 = f"{gpuV.load*100}"
            value2T = gpuV.temperature
        self.ui.label_6.setText(str(value2)+"%")
        self.ui.label_8.setText(str(value2T)+"°C")    
        
        value3 = psutil.virtual_memory()
        value3a = f"{(value3[3]/(1024**3)):.1f}"
        #value3aa = f"{value3a:.1f}"  
        self.ui.label_10.setText(str(value3a)+"GB")


    def cpuBrand(self):
        
        cB = self.proc["brand_raw"]
        self.ui.label_3.setText(cB)
        hz = self.proc["hz_actual_friendly"]
        self.ui.label_4.setText(hz)

    def gpuBrand(self):
        
        gpu = self.computer.Win32_VideoController()[0]
        gpu_name = gpu.VideoProcessor
        self.ui.label_7.setText(gpu_name)

    def mother(self):
        mb = self.computer.Win32_BaseBoard()[0]
        mbName = mb.Name
        mbModel = mb.Product
        self.ui.label_14.setText(mbName + ":  " + mbModel)


    def totalRam(self):

        ramHz = self.computer.Win32_PhysicalMemory()[0]
        ramHzS = ramHz.Speed
        self.ui.label_12.setText(str(ramHzS)+"MHz")
        r = psutil.virtual_memory()
        ram = f"{(r[0]/(1023**3)):.2f}"
        self.ui.label_11.setText(str(ram)+"GB")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())





