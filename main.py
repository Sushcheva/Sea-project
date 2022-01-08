import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QCheckBox, QInputDialog, QTextBrowser, QLabel, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui  # для измениения шрифта
from PyQt5.QtGui import QPixmap


sp = []
n = ' '
a = ' '
s = ' '


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 700, 700, 700)
        self.setWindowTitle('Игра в осьминога')
        self.label = QLabel(self)
        self.label.setText('Игра в осьминога')
        self.label.setFont(QtGui.QFont("Times", 23, QtGui.QFont.Bold))
        self.label.adjustSize()
        self.label.move(800, 50)
        self.pixmap = QPixmap('1.jpg')
        self.image = QLabel(self)
        self.image.move(40, 40)
        self.image.resize(600, 610)
        self.image.setPixmap(self.pixmap)
        self.btn = QPushButton('Играть', self)
        self.btn.move(800, 700)
        self.btn.clicked.connect(self.open_seven_form)
        self.btn.setFont(QtGui.QFont("Times", 19, QtGui.QFont.Bold))
        self.btn.adjustSize()
        self.button_1 = QPushButton("Введи свои ФИО", self)
        self.button_1.move(800, 200)
        self.button_1.setFont(QtGui.QFont("Times", 15))
        self.button_1.adjustSize()
        self.button_1.clicked.connect(self.run1)
        self.button_2 = QPushButton("Введи свой возраст", self)
        self.button_2.move(800, 350)
        self.button_2.setFont(QtGui.QFont("Times", 15))
        self.button_2.adjustSize()
        self.button_2.clicked.connect(self.run2)
        self.button_2.hide()
        self.button_3 = QPushButton("Введи свою страну проживания", self)
        self.button_3.move(800, 500)
        self.button_3.setFont(QtGui.QFont("Times", 15))
        self.button_3.adjustSize()
        self.button_3.clicked.connect(self.run3)
        self.button_3.hide()
        self.label1 = QLabel(self)
        self.label1.move(800, 200)
        self.label2 = QLabel(self)
        self.label2.move(800, 350)
        self.label3 = QLabel(self)
        self.label3.move(800, 500)

    def run1(self):  # диалоговое окно для ввода имени
        global sp
        global n
        name, ok_pressed = QInputDialog.getText(self, "ФИО", "Как тебя зовут?")
        if ok_pressed:
            self.label1.setText(name)
            self.label1.setFont(QtGui.QFont("Times", 15))
            self.label1.adjustSize()
            self.button_1.hide()
            self.button_2.show()
            n = name
            sp.append(name)

    def run2(self):  # диалоговое окно для ввода возраста
        global sp
        global a
        age, ok_pressed = QInputDialog.getItem(
            self, "Возраст", "Сколько тебе лет?",
            ('меньше 13 лет', '13 - 18 лет', '19 - 44 года', '45 - 59 лет', '60 и более лет'), 1, False)
        if ok_pressed:
            self.label2.setText(age)
            self.label2.setFont(QtGui.QFont("Times", 15))
            self.label2.adjustSize()
            self.button_2.hide()
            self.button_3.show()
            sp.append(age)
            a = age

    def run3(self):  # диалоговое окно для ввода страны проживания
        global sp
        global s
        global n
        global a
        state, ok_pressed = QInputDialog.getItem(
            self, "Страна проживания", "В какой стране ты живёшь?",
            ("Бразилия", "Россия", "Австралия", "Австрия", "Финляндия", "Япония", "Норвегия", "Эстония", "Латвия",
             "Литва", "Польша", "Белоруссия", "Украина", "Абхазия", "Грузия", "Южная Осетия", "Азербайджан",
             "Казахстан", "Китай", "Монголия", "Северная Корея", "Германия", "США", "другая страна"),
            1, False)
        if ok_pressed:
            self.label3.setText(state)
            self.label3.setFont(QtGui.QFont("Times", 15))
            self.label3.adjustSize()
            self.button_3.hide()
            sp.append(state)
            s = state
            print(s)
            print(sp)
            con = sqlite3.connect('5base5.db')
            cur = con.cursor()
            print(cur)
            rez = cur.execute(f'SELECT * FROM person WHERE name=? AND age=? AND state=?', (n, a, s))
            con.commit()
            print(rez)
            if rez.fetchone() is None:
                print('uuuuuuuuuuuuuuuuu')
                cur.execute(f'INSERT INTO person(name, age, state) VALUES(?, ?, ?)', (n, a, s))
            else:
                print('aaaaaaaaaaaaaaaa')
                n1, n2, n3 = rez[0]
                d = f'Ага, вы тот самый {n1}, ваш прошлый результат был равен, мы уверены,вы сможете его улучшить!'
                QMessageBox.about(self, 'АГА', d)

    def open_seven_form(self):
        pass


def e(a, b, c):
    sys.__excepthook__(a, b, c)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = e
    ex = Example()
    ex.show()
    sys.exit(app.exec())