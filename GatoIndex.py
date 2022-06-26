import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import *
from OpenGL.GLUT import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore
import datetime, time

from Viewer3DWidget import *


# Ventana principal
class Ventana(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ejemplogl.ui')
        self.ui.setWindowIcon(QtGui.QIcon('uoh.jpg'))
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.viewer3D = Viewer3DWidget(self)
        self.ui.OpenGLLayout.addWidget(self.viewer3D)
        self.ui.show()
        self.song = 'videoplayback.mpeg'

        # variables
        self._cambiarsymbol = "x"
        #music timer
        self.url = QtCore.QUrl.fromLocalFile(self.song)
        self.content = QMediaContent(self.url)
        self.player = QMediaPlayer()
        self.player.setMedia(self.content)
        self.player.play()
        self.timer2 = QTimer()
        self.time = QtCore.QTime(0, 0, 0)
        self.timer2.timeout.connect(self.timerEvent)
        self.timer2.start(1000)
        # Triggers


        self.ui.confirm.clicked.connect(self.changeSymbol)

        self.ui.rBX.toggled.connect(self.cSX)
        self.ui.rBO.toggled.connect(self.cSO)

    def changeSymbol(self):
        self.viewer3D.Symbol = self._cambiarsymbol

    def cSX(self):
        self._cambiarsymbol = "x"

    def cSO(self):
        self._cambiarsymbol = "o"

    def playAudioFile(self):
        full_file_path = os.path.join(os.getcwd(), self.song)
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def timerEvent(self):
        self.time = self.time.addSecs(1)
        if (self.time.toString("mm:ss") == "01:33"):
            self.url = QtCore.QUrl.fromLocalFile(self.song)
            self.content = QMediaContent(self.url)
            self.player = QMediaPlayer()
            self.player.setMedia(self.content)
            self.player.play()
        self.ui.cronometro_2.display(self.time.toString("mm:ss"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec_())
