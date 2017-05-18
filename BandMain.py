import sys
from PyQt5.QtWidgets import (QWidget,QToolTip,QMainWindow,
                             QPushButton,QApplication,
                             QLineEdit,QLabel,
                             QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, pyqtSignal,QObject
from time import localtime,strftime
import pandas as pd
class Communicate(QObject):
    changeStatus = pyqtSignal()
class BandUI(QWidget):
    def __init__(self):
        super().__init__()
        self.status=2
        self.counter=0
        self.counterDict={'1':1, '2':1, '3':1, '4':1, '5':3, '6':5, '7':15, '8':0}    #8 kernels & their sending speed
        self._timeStamp = 1488754980
        self._data=pd.read_csv('FinalData.csv')
        self._data=self._data.set_index('time')
        self.initUI()
        self._signal = Communicate()
        self._signal.changeStatus.connect(self.statusLineSlot)

    ################################Main
    def initUI(self):
        #initialize
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a Band')

        #function
            #Next Button
        btn=QPushButton('Next',self)
        btn.setToolTip('Next Minute')
        btn.clicked.connect(self.nextclicked)
        btn.resize(btn.sizeHint())
        btn.move(50,280)
            #Quit Button
        qbtn=QPushButton('Quit',self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150,280)

            #show time
        self._TimeLabel=QLabel("Time:",self)
        self._TimeLabel.move(50,50)
        self.refreshtime()
        self._timeLine=QLineEdit(self._timeStr,self)
        self._timeLine.setReadOnly(True)
        self._timeLine.move(50,70)

            #show status
        self.refreshstatus()
                #Heartrate
        self._HeartrateLabel=QLabel('Heartrate:',self)
        self._HeartrateLabel.move(50,100)
        self._HeartrateLine=QLineEdit(str(self._heartrate),self)
        self._HeartrateLine.setReadOnly(True)
        self._HeartrateLine.move(50,120)
                #distance
        self._DistanceLabel = QLabel('Speed:', self)
        self._DistanceLabel.move(50, 150)
        self._DistanceLine = QLineEdit(str(self._distance), self)
        self._DistanceLine.setReadOnly(True)
        self._DistanceLine.move(50, 170)
                #floors
        self._floorsLabel = QLabel('Height:', self)
        self._floorsLabel.move(50, 200)
        self._floorsLine = QLineEdit(str(self._floors), self)
        self._floorsLine.setReadOnly(True)
        self._floorsLine.move(50, 220)

        #show the window
        self.setGeometry(300,300,300,350)
        self.setWindowTitle('Band')
        self.show()


        ##################Other Function
    def refreshtime(self):
        self._timeArray = localtime(self._timeStamp)
        self._timeStr = strftime("%Y-%m-%d %H:%M:%S", self._timeArray)

    def refreshstatus(self):
        self.dataInDay=self._data.loc[self._timeStamp]     #this is a Series
        self._calories=self.dataInDay['calories']          #those below are all numbers
        self._calorieslevel=self.dataInDay['calorieslevel']
        self._caloriesmets=self.dataInDay['caloriesmets']
        self._distance=self.dataInDay['distance']
        self._floors=self.dataInDay['floors']
        self._heartrate=self.dataInDay['heartrate']
        self._sleep=self.dataInDay['sleep']
        self._steps=self.dataInDay['steps']

    def nextclicked(self):
        self._timeStamp += 60
        self.counter += 1

        self.refreshtime()
        self._timeLine.setText(self._timeStr)
        self.refreshstatus()
        self._HeartrateLine.setText(str(self._heartrate))
        self._floorsLine.setText(str(self._floors))
        self._DistanceLine.setText(str(self._distance))

        self.checkcounter()

    def checkcounter(self):

        self.status = self.exchangemessage()
        self._signal.changeStatus.emit()

    def exchangemessage(self):
        return self.pm.cal()

    def statusLineSlot(self):
        self.pm.statusLine.setText(str(self.status))

    def setPhoneMain(self, pm):
        self.pm = pm

if __name__ == '__main__':
    app=QApplication(sys.argv)
    Band=BandUI()
    sys.exit(app.exec_())