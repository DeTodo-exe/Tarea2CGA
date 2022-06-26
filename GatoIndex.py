import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import *
from OpenGL.GLUT import *

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

        # variables
        self._cambiarsymbol = "x"

        self.timer = QTimer()
        self.timer.timeout.connect(self.timeUpdater)

        self.timer.start(1000)

        self.timeUpdater()

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

    def timeUpdater(self):
        current_time = datetime.datetime.now()

        put_time = current_time.strftime("%S")

        self.ui.cronometro_1.display(put_time)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec_())
