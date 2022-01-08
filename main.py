import pygame
import sys
import os
import sqlite3

from PyQt5.QtWidgets import QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout, QWidget, \
    QTableWidget, QTableWidgetItem, QCheckBox, QInputDialog, QTextBrowser, QLabel, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui # для измениения шрифта
from PyQt5.QtGui import QPixmap


sp = []
n = ' '
a = ' '
s = ' '


pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 400
HEIGHT = 300
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data1', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data1/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, event):
        if event == 1:
            self.rect = self.rect.move(0, 50)
            self.pos_y += 1
        if event == 2:
            self.rect = self.rect.move(0, -50)
            self.pos_y -= 1
        if event == 3:
            self.rect = self.rect.move(50, 0)
            self.pos_x += 1
        if event == 4:
            self.rect = self.rect.move(-50, 0)
            self.pos_x -= 1



class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)



player, level_x, level_y = generate_level(load_level('map'))
camera = Camera((level_x, level_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.update(4)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(3)
            elif event.key == pygame.K_DOWN:
                player.update(1)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(2)
            elif event.key == pygame.K_UP:
                player.update(2)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(1)
            elif event.key == pygame.K_RIGHT:
                player.update(3)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(4)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)


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
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            rez = cur.execute(f'SELECT * FROM people WHERE name=? AND age=? AND state=?', (n, a, s,)).fetchall()
            con.commit()
            print(rez)
            if rez is None:
                pass
            else:
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



