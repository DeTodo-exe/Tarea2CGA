from PyQt5.QtCore import Qt
from PyQt5 import QtOpenGL
from OpenGL.GL import *
from PyQt5.QtWidgets import QMessageBox
from math import *
from random import *


def symbol(_s, _coords, _v):
    if _s == "x" and _v:
        glColor3fv([1, 1, 1])
        glBegin(GL_LINES)
        glVertex2f(-1 / 3 + _coords[0], 1 / 3 + _coords[1])
        glVertex2f(1 / 3 + _coords[0], -1 / 3 + _coords[1])
        glVertex2f(-1 / 3 + _coords[0], -1 / 3 + _coords[1])
        glVertex2f(1 / 3 + _coords[0], 1 / 3 + _coords[1])
        glEnd()
    elif _s == "o" and _v:
        glColor3fv([1, 1, 1])
        glBegin(GL_LINE_LOOP)
        n = 100
        for i in range(n):
            theta = (2.0 * pi * float(i)) / float(n)
            glVertex2f((-sin(theta) / 3) + _coords[0], (cos(theta) / 3) + _coords[1])
        glEnd()


def grid():
    glColor3fv([1, 1, 1])
    glBegin(GL_LINES)
    glVertex2f(-1, 1 / 3)
    glVertex2f(1, 1 / 3)
    glEnd()
    glColor3fv([1, 1, 1])
    glBegin(GL_LINES)
    glVertex2f(-1, - 1 / 3)
    glVertex2f(1, - 1 / 3)
    glEnd()
    glColor3fv([1, 1, 1])
    glBegin(GL_LINES)
    glVertex2f(-1 / 3, 1)
    glVertex2f(-1 / 3, - 1)
    glEnd()
    glColor3fv([1, 1, 1])
    glBegin(GL_LINES)
    glVertex2f(1 / 3, 1)
    glVertex2f(1 / 3, - 1)
    glEnd()


# Ventana clase OpenGL

def upgradeVerifier2Colum(_m):
    a, b, c = [], [], []
    for i in range(len(_m)):
        if i <= 2:
            a.append(_m[i])
        elif i <= 5:
            b.append(_m[i])
        elif i <= 8:
            c.append(_m[i])
    return [a] + [b] + [c]


class Viewer3DWidget(QtOpenGL.QGLWidget):
    def __init__(self, _symbol, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.verifiercolum = list()
        self.current_turn = True # Si es verdad sera turno del jugador

        # Simbolos 

        self.Symbol = "x"
        self.iASymbol = "o"

        # Coords

        self.x = 0
        self.y = 0
        self.n = 2 / 3
        # Corresponden a las esquinas superiores izquierdas de cada cuadrado
        # Desde es punto es posible obtener los 3 restantes
        self.coords = [[(-self.n, self.n), (0, self.n), (self.n, self.n)],
                       [(-self.n, 0), (0, 0), (self.n, 0)],
                       [(-self.n, -self.n), (0, -self.n), (self.n, -self.n)]]

        self.coordsx = [self.coords[i][j] for i in range(len(self.coords)) for j in range(len(self.coords))]
        self.coordsy = [self.coords[j][i] for i in range(len(self.coords)) for j in range(len(self.coords))]
        self.setFocusPolicy(Qt.StrongFocus)

        self.verifier = [[[0, ""], [0, ""], [0, ""]],
                         [[0, ""], [0, ""], [0, ""]],
                         [[0, ""], [0, ""], [0, ""]]]
        # Corresponde a los mensajes
        self.msg = QMessageBox()

    def paintGL(self):
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        for i in range(len(self.coords)):
            for j in range(len(self.coords)):
                if self.verifier[i][j]:
                    symbol(self.verifier[i][j][1], self.coords[i][j], self.verifier[i][j][0])
        grid()
        self.playerPos()
        glFlush()

    def Refresh(self):
        self.verifier = [[[0, ""], [0, ""], [0, ""]],
                         [[0, ""], [0, ""], [0, ""]],
                         [[0, ""], [0, ""], [0, ""]]]
        self.current_turn = True

    def resizeGL(self, widthInPixels, heightInPixels):
        glViewport(0, 0, widthInPixels, heightInPixels)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

    def playerPos(self):
        glColor3fv([0.25, 0.25, 0.25])

        glBegin(GL_POLYGON)
        glVertex2f(-1 / 3 + self.x, 1 / 3 + self.y)
        glVertex2f(-1 / 3 + self.x, -1 / 3 + self.y)
        glVertex2f(1 / 3 + self.x, -1 / 3 + self.y)
        glVertex2f(1 / 3 + self.x, 1 / 3 + self.y)
        glEnd()

    def moveRight(self, evento):
        if evento.key() == Qt.Key_Right and (self.x + self.n, self.y) in self.coordsx:
            self.x += self.n

    def moveLeft(self, evento):
        if evento.key() == Qt.Key_Left and (self.x - self.n, self.y) in self.coordsx:
            self.x -= self.n

    def moveUp(self, evento):
        if evento.key() == Qt.Key_Up and (self.x, self.y + self.n) in self.coordsy:
            self.y += self.n

    def moveDown(self, evento):
        if evento.key() == Qt.Key_Down and (self.x, self.y - self.n) in self.coordsy:
            self.y -= self.n

    def placeFigure(self, evento):
        if evento.key() == Qt.Key_Space:
            for i in range(len(self.coords)):
                for j in range(len(self.coords)):
                    if (self.x, self.y) == self.coords[i][j] and self.verifier[i][j][1] == "" and self.current_turn:
                        self.verifier[i][j] = [1, self.Symbol]
                        self.verifiercolum = [self.verifier[j][i] for i in range(len(self.verifier)) for j in
                                              range(len(self.verifier))]
                        self.verifiercolum = upgradeVerifier2Colum(self.verifiercolum)
                        self.current_turn = False
                        self.whoWins()
                        """
                        if self.verifier[i][j][0]:
                            self.verifier[i][j] = [0, self.Symbol]
                        else:
                            self.verifier[i][j] = [1, self.Symbol]
                        """

    def iAResponce(self):
        for i in range(randint(0, len(self.coords))):
            for j in range(randint(0, len(self.coords))):
                if self.verifier[i][j][1] == "" and self.current_turn == False:
                    self.verifier[i][j] = [1, self.iASymbol]
                    self.verifiercolum = [self.verifier[j][i] for i in range(len(self.verifier)) for j in
                                          range(len(self.verifier))]
                    self.verifiercolum = upgradeVerifier2Colum(self.verifiercolum)
                    self.current_turn = True
                    self.whoWins()
                    """
                    if self.verifier[i][j][0]:
                        self.verifier[i][j] = [0, self.Symbol]
                    else:
                        self.verifier[i][j] = [1, self.Symbol]
                    """

    def keyPressEvent(self, evento):
        # Función que permite identificar algún botón (arriba, abajo, izquierda, derecha, espacio)
        self.moveRight(evento)
        self.moveLeft(evento)
        self.moveUp(evento)
        self.moveDown(evento)
        self.placeFigure(evento)
        self.iAResponce()
        self.playerPos()
        self.updateGL()

    def displayWin(self, strMsg, title="Victory", setext="You Win!"):
        self.msg.setText(setext)
        self.msg.setWindowTitle(title)
        self.msg.setInformativeText(strMsg)
        self.msg.exec()
    
    def displaydraw(self, strMsg, title="DRAW", setext="DRAW"):
        self.msg.setText(setext)
        self.msg.setWindowTitle(title)
        self.msg.setInformativeText(strMsg)
        self.msg.exec()

    def callwin(self):
        if self.Symbol == "x":
            self.displayWin("Ganador juagor X")
        elif self.Symbol == "o":
            self.displayWin("Ganador jugador O")
        self.Refresh()
    
    def calldraw(self):
        self.displaydraw("Empate")
        self.Refresh()

    def whoWins(self):
        for _l in range(2):
            for _j in self.verifiercolum:
                if _j[0] == _j[1] == _j[2] == [1, 'x'] or _j[0] == _j[1] == _j[2] == [1, 'o']:
                    return self.callwin()

        for _i in self.verifier:
            if _i[0] == _i[1] == _i[2] == [1, 'x'] or _i[0] == _i[1] == _i[2] == [1, 'o']:
                return self.callwin()

        if self.verifier[0][0] == self.verifier[1][1] == self.verifier[2][2] == [1, 'x'] or self.verifier[0][2] == self.verifier[1][1] == self.verifier[2][0] == [1, 'x']:
            return self.callwin()
        elif  self.verifier[0][0] == self.verifier[1][1] == self.verifier[2][2] == [1, 'o'] or self.verifier[0][2] == self.verifier[1][1] == self.verifier[2][0] == [1, 'o']:
            return self.callwin()
        
        if self.verifier[0][0][0] and self.verifier[0][1][0] and self.verifier[0][2][0] and self.verifier[1][0][0] and self.verifier[1][1][0] and self.verifier[1][2][0] and self.verifier[2][0][0] and self.verifier[2][1][0] and self.verifier[2][2][0]:
            return self.calldraw()
