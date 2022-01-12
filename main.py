import sys

from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QInputDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QMovie, QPainter

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.movie = QMovie("gif.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()
        self.image = QLabel(self)
        self.label = QLabel(self)
        self.setGeometry(700, 700, 700, 700)
        self.setWindowTitle('Игра')
        self.label.setText('Добро пожаловать! Выбирай игру:')
        self.label.setFont(QtGui.QFont("Gabriola", 46, QtGui.QFont.Black))
        self.label.adjustSize()
        self.label.move(450, 150)
        self.image.move(40, 40)
        self.image.resize(600, 610)
        self.button_1 = QPushButton("Фруктовый ниндзя", self)
        self.button_1.move(400, 450)
        self.button_1.setStyleSheet('background: rgb(153, 0, 255);')
        self.button_1.setFont(QtGui.QFont("Gabriola", 30))
        self.button_1.adjustSize()
        self.button_1.clicked.connect(self.run1)
        self.button_2 = QPushButton("Волшебный лабиринт", self)
        self.button_2.move(1120, 450)
        self.button_2.setStyleSheet('background: rgb(153, 0, 255);')
        self.button_2.setFont(QtGui.QFont("Gabriola", 30))
        self.button_2.adjustSize()
        self.button_2.clicked.connect(self.run2)
        self.button_2.hide()
        self.label1 = QLabel(self)
        self.label1.move(900, 300)
        self.label2 = QLabel(self)
        self.label2.move(900, 300)
        self.button_2.show()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def run1(self):
        ninlvl, ok_pressed = QInputDialog.getItem(
            self, "Сложность", "Выбери уровень:",
            ('для новичка', 'средний', 'сложный'), 1, False)
        if ok_pressed:
            self.label1.setText(ninlvl)
            self.label1.setFont(QtGui.QFont("Gabriola", 36, QtGui.QFont.Bold))
            self.label1.adjustSize()
            self.button_1.hide()
            self.button_2.hide()
            self.open_second_form()

    def run2(self):
        lablvl, ok_pressed = QInputDialog.getItem(
            self, "Карта", "Выбери сложность карты:",
            ("простая", "средняя", "сложная"),
            1, False)
        if ok_pressed:
            self.label2.setText(lablvl)
            self.label2.setFont(QtGui.QFont("Gabriola", 36, QtGui.QFont.Bold))
            self.label2.adjustSize()
            self.button_2.hide()
            self.button_1.hide()
            self.open_second_form()


    def open_second_form(self):
        pass


def e(a, b, c):
    sys.__excepthook__(a, b, c)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = e
    ex = Example()
    ex.show()
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("./fon.jpg")))
    ex.setPalette(palette)
    sys.exit(app.exec())