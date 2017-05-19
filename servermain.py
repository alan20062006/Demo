import sys
from PyQt5.QtWidgets import (QWidget,QToolTip,QMainWindow,
                             QPushButton,QApplication,
                             QLabel)
from PyQt5.QtGui import QFont,QPalette
from PyQt5.QtCore import QCoreApplication
from time import sleep

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
        qbtn.move(25, 75)

        # sync status
        self.statusLabel = QLabel('Suspending', self)
        self.statusLabel.setStyleSheet("color:rgb(30,30,30);")
        self.statusLabel.move(30, 25)


        self.setGeometry(1200,300,50,125)
        #set background as gray
        self.setStyleSheet("background-color:rgb(180,180,180);")

        self.setWindowTitle('Server')
        self.show()

    def sync(self):
        self.statusLabel.setText('Syncing...')
        #sleep(3)
        #self.statusLabel.setText('Succeed')
        #sleep(2)
        #self.statusLabel.setText('Suspending')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Server = ServerUI()
    sys.exit(app.exec_())