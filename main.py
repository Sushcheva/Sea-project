import pygame
import sys
import os
from random import sample, randrange, choice
import sqlite3

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, \
     QInputDialog, QLabel, QMessageBox
from PyQt5 import QtGui  # для измениения шрифта
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QInputDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QMovie, QPainter

pygame.font.init()
FPS = 60
all_sprites = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
person_group = pygame.sprite.Group()
strix_group = pygame.sprite.Group()
player = None
screen_rect = (0, 0, 500, 500)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, image, r=0):
        fire = [load_image(image)]
        for scale in (15, 20, 25, 25, 50):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        super().__init__(strix_group)
        if r == 0:
            self.image = choice(fire)
        else:
            self.image = pygame.transform.scale(fire[0], (r, r))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, image1, columns, rows, x, y):
        super().__init__(all_sprites)
        self.image1 = image1
        self.z = 1
        self.frames = []
        self.sheet = sheet
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Heroes(AnimatedSprite):
    def __init__(self, sheet, image1, columns, rows, x, y):
        super().__init__(sheet, image1, columns, rows, x, y)

    def update(self):
        if self.cur_frame != len(self.frames) - 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(20, 0)
        else:
            self.z += 0.2
            if self.z >= 6:
                self.image = load_image('njump1.png')
                self.image = pygame.transform.scale(self.image, (78 * 3, 197 * 3))
            else:
                self.image = load_image('njump1.png')
                self.image = pygame.transform.scale(self.image, (78 * self.z, 197 * self.z))


def create_particles(position, image):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers), image)


def ti(b):
    pygame.init()
    size = 1000, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    if b:
        fon = pygame.transform.scale(load_image('victory.png'), (500, 500))
    else:
        fon = pygame.transform.scale(load_image('game_over.png'), (500, 500))
    font = pygame.font.Font(None, 30)
    text_coord = 400
    string_rendered = font.render(str('Вы набрали '+ str(b) +' баллов'), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 25
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ninja()
        screen.blit(fon, (0, 0))
        fon.blit(string_rendered,intro_rect)
        clock.tick(8)
        pygame.display.flip()


tile_images = {
    'wall': load_image('box.png', None),
    'empty': load_image('grass.png', None)
}
player_image = load_image('mar.png', None)

tile_width = tile_height = 50


class Strix(pygame.sprite.Sprite):
    def __init__(self, image, pos, time):
        super().__init__(strix_group, all_sprites)
        self.time = time
        self.t = 200
        self.image = pygame.transform.scale(load_image(image, None), (100, 100))
        self.rect = self.image.get_rect().move(
            pos[0] - 50, pos[1] - 50)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Fruit(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, time, image1):
        super().__init__(fruit_group)
        self.image1 = image1
        if image != 'bomb.png':
            self.type = 'Fruit'
        else:
            self.type = 'Bomb'
        self.time = time
        self.v0 = randrange(-1000, -700)
        self.v1 = abs(self.v0)
        self.image = pygame.transform.scale(load_image(image, None), (100, 100))
        self.rect = self.image.get_rect().move(
            pos_x, 1000)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_x = pos_x
        self.x0 = 1000
        self.z = 0
        self.k = False
        self.d = False
        self.pos_y = 0

    def update(self, t):
        if self.z >= 999 and self.k:
            self.d = True

        if self.time <= t and not self.d:
            t1 = t / 100 - self.time / 100
            if self.v0 < 0:
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.x0 + self.v0 * t1 + 0.6 * (t1 ** 2))
                self.pos_y = self.x0 + self.v0 * t1 + 0.6 * (t1 ** 2)
                self.z += self.x0 + self.v0 * t1 + 0.6 * (t1 ** 2)
                self.v0 += 1.2
            else:
                self.k = True
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.x0 - self.v0 * t1 + 0.6 * (t1 ** 2))
                self.pos_y = self.x0 - self.v0 * t1 + 0.6 * (t1 ** 2)
                self.z += self.x0 - self.v0 * t1 + 0.6 * (t1 ** 2)
                self.v0 -= 1.2

        elif self.d and self.type == 'Fruit':
            self.image = pygame.transform.scale(load_image('w.png', None), (10, 10))
            self.rect = self.image.get_rect().move(
                self.pos_x, 1100)
            self.type = 'F'
            self.mask = pygame.mask.from_surface(self.image)

    def update2(self, el1):
        if self.pos_x <= el1[0] <= self.pos_x + 75 and self.pos_y <= el1[1] <= self.pos_y + 100:
            self.image = pygame.transform.scale(load_image('w.png', None), (100, 100))
            if self.type == 'Fruit':
                Strix('br.png', el1, 1)
                create_particles(el1, 'b.png')
                Particle(el1, -1, -3, self.image1, 75)
                Particle(el1, 1, -3, self.image1, 75)
                self.type = 'Cut'
            elif self.type == 'Bomb':
                Strix('bu.png', el1, 1)
                create_particles(el1, 'fire.png')
                self.image = pygame.transform.scale(load_image('boom1.png', None), (100, 100))
                self.type = 'Bombed'


def ninja():
    pygame.init()
    size = 200, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('les.png'), (1000, 1000))

    nindja = Heroes(load_image("njump.png"), 'nudar.png', 9, 1, 100, 100)
    running = True
    t = 0
    f = open('18.txt', encoding="utf8")
    fu = f.readlines()
    hero = 'Ниндзя'
    number = 0
    for el in fu:
        if el == hero:
            number = fu.index(el)
    font = pygame.font.Font(None, 40)
    text_coord = 15
    string_rendered = font.render('', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                number += 1
                if number < len(fu):
                    print(fu[t])
                    string_rendered = font.render(fu[number], 1, pygame.Color('white'))
                else:
                    string_rendered = font.render('', 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = text_coord
                intro_rect.x = 25
                text_coord += intro_rect.height
        screen.blit(fon, (0, 0))
        fon.blit(string_rendered, intro_rect)
        all_sprites.update()
        clock.tick(8)
        all_sprites.draw(screen)
        person_group.draw(screen)
        pygame.display.flip()
    running = True
    z = ['bomb.png', 'apple.png', 'apple.png', 'apple.png', 'mango.png', 'mango.png', 'banana.png', 'banana.png',
         'coconut.png',
         'coconut.png', 'granat.png', 'granat.png', 'granat.png', 'granat.png', 'pear.png', 'pear.png', 'pear.png',
         'pear.png', 'pineapple.png', 'pineapple.png', 'pineapple.png', 'strawberry.png',
         'strawberry.png', 'strawberry.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png',
         'bomb.png', 'apple.png', 'apple.png', 'apple.png', 'mango.png', 'mango.png', 'banana.png', 'banana.png',
         'coconut.png',
         'coconut.png', 'granat.png', 'granat.png', 'granat.png', 'granat.png', 'pear.png', 'pear.png', 'pear.png',
         'pear.png', 'pineapple.png', 'pineapple.png', 'pineapple.png', 'strawberry.png',
         'strawberry.png', 'strawberry.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png', 'bomb.png']
    t = 0
    f.close()
    z1 = sample(z, 50)
    g = 0
    z2 = []
    fon = pygame.transform.scale(load_image('les.png'), (500, 500))
    for i in range(50):
        z2.append(randrange(100, 2500))
    for el in z1:
        Fruit(el, randrange(0, 900), z2[g], str(el[:-4] + '1' + el[-4:]))
        g += 1
    while running:
        lifes = 5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Strix('pt.png', event.pos, t)
                for el in fruit_group:
                    el.update2(event.pos)
        t += 1
        z = 0
        s = 0
        screen.blit(fon, (0, 0))
        for el in fruit_group:
            el.update(t)
            if el.type == 'Bombed' or el.type == 'F':
                lifes -= 1
            if el.type == 'Cut':
                s += 1
        strix_group.update()
        strix_group.draw(screen)
        fruit_group.draw(screen)
        x = 100
        for i in range(lifes):
            pygame.draw.ellipse(screen, (255, 0, 0), (x, 10, 50, 50), 0)
            x += 75
        if lifes <= 0 or t >= 3000:
            ti(s)
            running = False
        pygame.display.flip()
        clock.tick(100)



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
        self.btn.clicked.connect(self.open_sev_form)
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
                d = f'Ага, вы тот самый {n}, ваш прошлый результат был равен, мы уверены,вы сможете его улучшить!'
                QMessageBox.about(self, 'АГА', d)
            con.commit()

    def open_sev_form(self):
        self.thorth_form = Exa()
        self.hide()
        self.thorth_form.show()
        self.thorth_form.showFullScreen()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./fon.jpg")))
        self.thorth_form.setPalette(palette)

class Exa(QWidget):
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
            ninja()

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
    sys.exit(app.exec())

