import sys
from PyQt5.QtWidgets import (QWidget,QToolTip,QMainWindow,
                             QPushButton,QApplication,
                             QLabel,QLineEdit)
from PyQt5.QtGui import QFont,QPalette
from PyQt5.QtCore import QCoreApplication,QTimer


class ServerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #initialize
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a Server')

        # Quit Button
        qbtn = QPushButton('Quit', self)
        qbtn.setStyleSheet("color:rgb(30,30,30);")
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 250)

        # push Button
        pushtn = QPushButton('Push', self)
        pushtn.setToolTip('Push the advertisement')
        pushtn.setStyleSheet("color:rgb(30,30,30);")
        pushtn.clicked.connect(self.push)
        pushtn.resize(qbtn.sizeHint())
        pushtn.move(50, 250)

        # sync status
        self.statusLabel = QLabel('Suspending', self)
        self.statusLabel.setStyleSheet("color:rgb(30,30,30);")
        self.statusLabel.move(100, 25)

        #Advertisement lineEdit
        self.adLine=QLineEdit('',self)
        self.adLine.setStyleSheet("color:rgb(30,30,30);")
        self.adLine.move(50,50)
        self.adLine.setFixedWidth(200)
        self.adLine.setFixedHeight(175)

        self.setGeometry(1200,300,300,300)
        #set background as gray
        self.setStyleSheet("background-color:rgb(180,180,180);")

        self.setWindowTitle('Server')
        self.show()

    def sync(self):
        self.statusLabel.setText('Syncing...')
        QTimer.singleShot(2000, lambda: self.statusLabel.setText('Succeed'))
        QTimer.singleShot(5000, lambda: self.statusLabel.setText('Suspending'))

    def push(self):
        self.ad=self.adLine.text()
        self.pm.adLine.setText(self.ad)

    def setPhoneMain(self,pm):
        self.pm=pm

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Server = ServerUI()
    sys.exit(app.exec_())