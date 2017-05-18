import sys
from PyQt5.QtWidgets import (QWidget,QToolTip,QMainWindow,
                             QPushButton,QApplication,
                             QLineEdit,QLabel,
                             QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication
from BandMain import BandUI
from collections import deque
import scipy.io as sio
import numpy as np
from time import localtime,strftime
import pandas as pd

class PhoneUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.Centrals=sio.loadmat('Centrals.mat')
        self.Centrals=self.Centrals['C']            #Centrals location
        self.xmin=[1.15620005130768,0,10,0,0,37,0,0,
                   1.15620005130768,0,10,0,0,37,0,0,
                   1.15620005130768,0,10,0,0,37,0,0,
                   1.15620005130768,0,10,0,0,37,0,0,
                   1.15620005130768,0,10,0,0,37,0,0,
                   1.15620005130768,0,10,0,0,37,0,0]
        self.xmax=[13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186,
                   13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186,
                   13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186,
                   13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186,
                   13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186,
                   13.0707101821899, 3, 113, 0.246800005435944, 5, 184, 3, 186]
        self.xrange=[11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186,
                     11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186,
                     11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186,
                     11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186,
                     11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186,
                     11.9145101308823, 3, 103, 0.246800005435944, 5, 147, 3, 186]
        self.numDict={'calories':1,'calorieslevel':2,'caloriesmets':3,'distance':4,
                      'floors':5,'heartrate':6,'sleep':7,'steps':8}
        self.queue=deque(maxlen=48)

    def initUI(self):
        #initialize
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a Phone')

        # Quit Button
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 530)

        # status
        self._statusLabel = QLabel('Status:', self)
        self._statusLabel.move(50, 100)
        self.statusLine = QLineEdit('0', self)
        self.statusLine.setReadOnly(True)
        self.statusLine.move(150, 100)

        self.setGeometry(300,600,400,600)
        self.setWindowTitle('Phone')
        self.show()
    def setBandMain(self, bm):
        self.bm = bm
    def cal(self):
        self._calories = self.psTrans('calories')
        self._calorieslevel = self.psTrans('calorieslevel')
        self._caloriesmets = self.psTrans('caloriesmets')
        self._distance = self.psTrans('distance')
        self._floors = self.psTrans('floors')
        self._heartrate = self.psTrans('heartrate')
        self._sleep = self.psTrans('sleep')
        self._steps = self.psTrans('steps')
        self.queue.append(self._steps)          #queue right out left in
        self.queue.append(self._sleep)
        self.queue.append(self._heartrate)
        self.queue.append(self._floors)
        self.queue.append(self._distance)
        self.queue.append(self._caloriesmets)
        self.queue.append(self._calorieslevel)
        self.queue.append(self._calories)
        if len(self.queue)<48:
            return 1
        elif self.bm.counter>=self.bm.counterDict[str(self.bm.status)]:
            self.refreshStatus()
            return self.bm.status
        return self.bm.status

    def refreshStatus(self):
        self.centralDistance=[]
        for i in range(8):
            self.centralDistance.append(np.sqrt(np.sum((np.array(self.queue)-self.Centrals[i])**2)))
        self.bm.status=self.centralDistance.index(min(self.centralDistance))+1


    def psTrans(self,type):
        return (2*self.bm.dataInDay[type]-(self.xmin[self.numDict[type]-1]+self.xmax[self.numDict[type]-1]))/self.xrange[self.numDict[type]-1]
if __name__ == '__main__':
    app=QApplication(sys.argv)
    Phone = PhoneUI()
    Band = BandUI()
    Phone.setBandMain(Band)
    Band.setPhoneMain(Phone)
    sys.exit(app.exec_())