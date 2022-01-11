import sys
import sqlite3
import csv

from PyQt5.QtWidgets import QPushButton, QWidget, QInputDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap('fon.jpg')
        self.image = QLabel(self)
        self.label = QLabel(self)
        self.setGeometry(700, 700, 700, 700)
        self.setWindowTitle('Игра')
        self.label.setText('Выбери игру')
        self.label.setFont(QtGui.QFont("Times", 23, QtGui.QFont.Bold))
        self.label.adjustSize()
        self.label.move(800, 50)
        self.image.move(40, 40)
        self.image.resize(600, 610)
        self.image.setPixmap(self.pixmap)
        self.button_1 = QPushButton("Фруктовый ниндзя", self)
        self.button_1.move(800, 200)
        self.button_1.setFont(QtGui.QFont("Times", 15))
        self.button_1.adjustSize()
        self.button_1.clicked.connect(self.run1)
        self.button_2 = QPushButton("Волшебный лабиринт", self)
        self.button_2.move(800, 350)
        self.button_2.setFont(QtGui.QFont("Times", 15))
        self.button_2.adjustSize()
        self.button_2.clicked.connect(self.run2)
        self.button_2.hide()
        self.label1 = QLabel(self)
        self.label1.move(800, 200)
        self.label2 = QLabel(self)
        self.label2.move(800, 350)
        self.label3 = QLabel(self)
        self.label3.move(800, 500)
        self.label5 = QLabel(self)

    def run1(self):
        ninlvl, ok_pressed = QInputDialog.getItem(
            self, "Сложность", "Выбери уровень:",
            ('для новичка', 'средний', 'сложный'), 1, False)
        if ok_pressed:
            self.label2.setText(ninlvl)
            self.label2.setFont(QtGui.QFont("Times", 15))
            self.label2.adjustSize()
            self.button_2.hide()
            self.button_3.show()

    def run2(self):
        lablvl, ok_pressed = QInputDialog.getItem(
            self, "Страна проживания", "В какой стране ты живёшь?",
            ("Бразилия", "Россия", "Австралия", "Австрия", "Финляндия", "Япония", "Норвегия", "Эстония", "Латвия",
             "Литва", "Польша", "Белоруссия", "Украина", "Абхазия", "Грузия", "Южная Осетия", "Азербайджан",
             "Казахстан", "Китай", "Монголия", "Северная Корея", "Германия", "США", "другая страна"),
            1, False)
        if ok_pressed:
            self.label3.setText(lablvl)
            self.label3.setFont(QtGui.QFont("Times", 15))
            self.label3.adjustSize()
            self.button_3.hide()

    def open_second_form(self):
        self.hide()
        self.second_form.show()
        self.second_form.showFullScreen()
