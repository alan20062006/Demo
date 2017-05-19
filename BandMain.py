import sys
from PyQt5.QtWidgets import (QWidget,QToolTip,QMainWindow,
                             QPushButton,QApplication,
                             QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, pyqtSignal,QObject
from time import localtime,strftime
import pandas as pd
class Communicate(QObject):
    changeStatus = pyqtSignal()
class BandUI(QWidget):
    def __init__(self):
        super().__init__()
        self.status=0
        self.counter=0
        self.counterDict={'1':1, '2':1, '3':1, '4':1, '5':3, '6':5, '7':15, '8':0,'0':1}    #8 kernels & their sending speed
        self.statusDict={'1': 'Jogging','2': 'Long Run','3':'Resting','4':'Climb or Jump',
                      '5': 'Walking','6':'Slight Moving','7':'Sitting','8':'Sleeping','0':'Unwear'}
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
        btn.setStyleSheet("color:rgb(160,160,160);")
        btn.setToolTip('Next Minute')
        btn.clicked.connect(self.nextclicked)
        btn.resize(btn.sizeHint())
        btn.move(25,280)
            #Quit Button
        qbtn=QPushButton('Quit',self)
        qbtn.setStyleSheet("color:rgb(160,160,160);")
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(125,280)

            #show time
        self._TimeLabel=QLabel("Time:",self)
        self._TimeLabel.setStyleSheet("color:rgb(160,160,160);")
        self._TimeLabel.move(100,50)
        self.refreshtime()
        self._timeLine=QLabel(self._timeStr,self)
        self._timeLine.setStyleSheet("color:rgb(160,160,160);")
        #self._timeLine.setReadOnly(True)
        self._timeLine.move(50,70)

            #show status
        self.refreshstatus()
                #Heartrate
        self._HeartrateLabel=QLabel('Heartrate:',self)
        self._HeartrateLabel.setStyleSheet("color:rgb(160,160,160);")
        self._HeartrateLabel.move(50,100)
        self._HeartrateLine=QLabel(str(self._heartrate),self)
        self._HeartrateLine.setStyleSheet("color:rgb(160,160,160);")
        #self._HeartrateLine.setReadOnly(True)
        self._HeartrateLine.move(50,120)
                #distance
        self._DistanceLabel = QLabel('Speed:', self)
        self._DistanceLabel.setStyleSheet("color:rgb(160,160,160);")
        self._DistanceLabel.move(50, 150)
        self._DistanceLine = QLabel(str(self._distance), self)
        self._DistanceLine.setStyleSheet("color:rgb(160,160,160);")
        #self._DistanceLine.setReadOnly(True)
        self._DistanceLine.move(50, 170)
                #floors
        self._floorsLabel = QLabel('Height:', self)
        self._floorsLabel.setStyleSheet("color:rgb(160,160,160);")
        self._floorsLabel.move(50, 200)
        self._floorsLine = QLabel(str(self._floors), self)
        self._floorsLine.setStyleSheet("color:rgb(160,160,160);")
        #self._floorsLine.setReadOnly(True)
        self._floorsLine.move(50, 220)

        #show the window
        self.setGeometry(300,300,250,350)
        # set background as black
        self.setStyleSheet("background-color:rgb(30,30,30);")

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
        self.pm.statusLine.setText(self.statusDict[str(self.status)])

    def setPhoneMain(self, pm):
        self.pm = pm

if __name__ == '__main__':
    app=QApplication(sys.argv)
    Band=BandUI()
    sys.exit(app.exec_())