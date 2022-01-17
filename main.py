import sys
import os
import sqlite3
import pygame
import random
from random import sample, randrange, choice
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QApplication, QWidget, QInputDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QMovie, QPainter

tile_width = tile_height = 50
pygame.font.init()
FPS = 60
all_sprites = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
person_group = pygame.sprite.Group()
all_sprites1 = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

strix_group = pygame.sprite.Group()
player = None
screen_rect = (0, 0, 500, 500)

st = 0
d = ['en.png', 'enn.png', 'ennn.png']


def load_level(filename):
    filename = "data/" + filename
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
            elif level[y][x] == '$':
                Tile('star', x, y)
            elif level[y][x] == '!':
                Tile('enemy', x, y)
            elif level[y][x] == ')':
                Tile('door', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


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
        super().__init__(tiles_group, all_sprites1)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites1)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, event):
        global st
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
        if event == 5:
            over_game()
        if event == 7:
            win_game()
        if event == 6:
            st += 1
            for el in tiles_group:
                if el.pos_x == self.pos_x and el.pos_y == self.pos_y:
                    el.image = load_image('grass.png')
                    el.tile_type = 'empty'
            print(st)


def over_game():
    pygame.init()
    size = 900, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 30)
    text_coord = 400
    string_rendered = font.render(str('Вы набрали ' + str(st) + ' баллов'), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 25
    fon = pygame.transform.scale(load_image('win1.png'), (900, 800))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        screen.blit(fon, (0, 0))
        clock.tick(8)
        pygame.display.flip()
        fon.blit(string_rendered, intro_rect)


def win_game():
    pygame.init()
    size = 900, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    info = cur.execute(f"SELECT stars FROM person WHERE name ==? AND age == ?", (n, a))
    if info.fetchone() is None:
        f"INSERT INTO person(stars)"
        f" VALUES('{st}')"
    else:
        cur.execute(f'UPDATE person SET stars=? WHERE name=? AND age=?', (st, n, a))
    con.commit()
    running = True
    fon = pygame.transform.scale(load_image('win.png'), (900, 800))
    font = pygame.font.Font(None, 30)
    text_coord = 600
    string_rendered = font.render(str('Вы набрали ' + str(st) + ' баллов'), 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 600
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        screen.blit(fon, (0, 0))
        fon.blit(string_rendered, intro_rect)
        clock.tick(8)
        pygame.display.flip()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_width = tile_height = 50
tile_images = {'wall': load_image('box1.png'), 'empty': load_image('grass.png'), \
               'enemy': load_image(random.choice(d)), 'door': load_image('door.png'),
               'star': load_image('star.png')}
player_image = load_image('mar2.png')
FPS = 50
WIDTH = 900
HEIGHT = 900
STEP = 10


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


class Heroes(pygame.sprite.Sprite):
    def __init__(self, sheet, image1, columns, rows, x, y):
        super().__init__(all_sprites, all_sprites1)
        self.image1 = image1
        self.z = 1
        self.frames = []
        self.sheet = sheet
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame != len(self.frames) - 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(20, 0)
        else:
            self.z += 0.2
            if self.z >= 3:
                self.image = load_image('njump1.png')
                self.image = pygame.transform.scale(self.image, (78 * 3, 197 * 3))
            else:
                self.image = load_image('njump1.png')
                self.image = pygame.transform.scale(self.image, (78 * self.z, 197 * self.z))

    def update1(self, player):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if  pygame.sprite.collide_mask(self, player):
            over_game()

def create_particles(position, image):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers), image)


def ti(b, r=False):
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    if b and r:
        fon = pygame.transform.scale(load_image('victory.png'), (500, 500))
    else:
        fon = pygame.transform.scale(load_image('game_over.png'), (500, 500))
    font = pygame.font.Font(None, 30)
    text_coord = 400
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    info = cur.execute(f"SELECT fruit FROM person WHERE name ==? AND age == ?", (n, a))
    if info.fetchone() is None:
        f"INSERT INTO person(fruit)"
        f" VALUES('{b}')"
    else:
        cur.execute(f'UPDATE person SET fruit=? WHERE name=? AND age=?', (b, n, a))
    con.commit()
    string_rendered = font.render(str('Вы набрали ' + str(b) + ' баллов'), 1, pygame.Color('white'))
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
        fon.blit(string_rendered, intro_rect)
        clock.tick(8)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


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
        self.v0 = randrange(-500, -350)
        self.v1 = abs(self.v0)
        self.image = pygame.transform.scale(load_image(image, None), (100, 100))
        self.rect = self.image.get_rect().move(
            pos_x, 500)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_x = pos_x
        self.x0 = 500
        self.z = 0
        self.k = False
        self.d = False
        self.pos_y = 0

    def update(self, t):
        if self.z >= 499 and self.k:
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
                self.pos_x, 600)
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
    size = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('les.png'), (500, 500))

    nindja = Heroes(load_image("njump.png"), 'nudar.png', 9, 1, 50, 50)
    running = True
    t = 0
    f = open('18.txt', encoding="utf8")
    fu = f.readlines()
    hero = 'Ниндзя'
    number = 0
    for el in fu:
        if el == hero:
            number = fu.index(el)
    font = pygame.font.Font(None, 30)
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
    pygame.quit()

    pygame.init()
    screen = pygame.display.set_mode(size)
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
        Fruit(el, randrange(0, 400), z2[g], str(el[:-4] + '1' + el[-4:]))
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
        if lifes <= 0:
            ti(s, False)
            running = False
        elif t >= 3000:
            ti(s, True)
            running = False
        if running == True:
            pygame.display.flip()
        clock.tick(100)
    pygame.quit()


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
        self.setWindowTitle('Сказочная долина')
        self.label = QLabel(self)
        self.label.setText('Сказочная долина')
        self.label.setFont(QtGui.QFont("Gabriola", 60))
        self.label.adjustSize()
        self.label.move(600, 20)
        self.btn = QPushButton('Играть', self)
        self.btn.move(850, 700)
        self.btn.setStyleSheet('background: rgb(153, 204, 255);')
        self.btn.setFont(QtGui.QFont("Gabriola", 30))
        self.btn.clicked.connect(self.open_sev_form)
        self.btn.adjustSize()
        self.button_1 = QPushButton("Введи свои ФИО", self)
        self.button_1.move(775, 200)
        self.button_1.setStyleSheet('background: rgb(153, 204, 255);')
        self.button_1.setFont(QtGui.QFont("Gabriola", 30))
        self.button_1.adjustSize()
        self.button_1.clicked.connect(self.run1)
        self.button_2 = QPushButton("Введи свой возраст", self)
        self.button_2.move(775, 350)
        self.button_2.setStyleSheet('background: rgb(153, 204, 255);')
        self.button_2.setFont(QtGui.QFont("Gabriola", 30))
        self.button_2.adjustSize()
        self.button_2.clicked.connect(self.run2)
        self.button_2.hide()
        self.button_3 = QPushButton("Введи свою страну проживания", self)
        self.button_3.move(775, 500)
        self.button_3.setStyleSheet('background: rgb(153, 204, 255);')
        self.button_3.setFont(QtGui.QFont("Gabriola", 30))
        self.button_3.adjustSize()
        self.button_3.clicked.connect(self.run3)
        self.button_3.hide()
        self.label1 = QLabel(self)
        self.label1.move(800, 200)
        self.label1.setFont(QtGui.QFont("Gabriola", 30))
        self.label2 = QLabel(self)
        self.label2.move(800, 350)
        self.label2.setFont(QtGui.QFont("Gabriola", 30))
        self.label3 = QLabel(self)
        self.label3.move(800, 500)
        self.label3.setFont(QtGui.QFont("Gabriola", 30))

    def run1(self):  # диалоговое окно для ввода имени
        global sp
        global n
        name, ok_pressed = QInputDialog.getText(self, "ФИО", "Как тебя зовут?")
        if ok_pressed:
            self.label1.setText(name)
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
            self.label3.adjustSize()
            self.button_3.hide()
            sp.append(state)
            s = state
            print(s)
            print(sp)
            con = sqlite3.connect('base.db')
            cur = con.cursor()
            print(cur)
            rez = cur.execute(f'SELECT * FROM person WHERE name=? AND age=? AND state=?', (n, a, s)).fetchall()
            con.commit()
            print(rez)
            if len(rez) == 0:
                cur.execute(f'INSERT INTO person(name, age, state) VALUES(?, ?, ?)', (n, a, s))
            else:
                n1, n2, n3, n4, n5 = rez[0]
                if n4 == None:
                    d = f'Ага, вы тот самый {n}, в прошлый раз вы приготовили салат из {n5} фруктов, ' \
                        f'мы уверены,вы сможете улучшить результат!'
                    QMessageBox.about(self, 'АГА', d)
                if n5 == None:
                    d1 = f'Ага, вы тот самый {n}, в прошлый раз вы собрали {n4} звёзд, ' \
                        f'мы уверены,вы сможете улучшить результат!'
                    QMessageBox.about(self, 'АГА', d1)
                if n4 != None and n5 != None:
                    d2 = f'Ага, вы тот самый {n}, в прошлый раз вы собрали {n4} звёзд, ' \
                         f'и приготовили салат из {n5} фруктов,мы уверены,вы сможете улучшить результат!'
                    QMessageBox.about(self, 'АГА', d2)
                else:
                    d3 = f'Ага, вы тот самый {n}, в прошлый раз вы собрали 0 звёзд, ' \
                         f'и приготовили салат из 0 фруктов,мы уверены,вы сможете улучшить результат!'
                    QMessageBox.about(self, 'АГА', d3)
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

            ninja()
            self.hide()

    def run2(self):
        lablvl, ok_pressed = QInputDialog.getItem(
            self, "Карта", "Выбери сложность карты:",
            ("простая", "средняя", "сложная"),
            1, False)
        if ok_pressed:
            self.label2.setText(lablvl)
            self.label2.setFont(QtGui.QFont("Gabriola", 36, QtGui.QFont.Bold))
            self.label2.adjustSize()

            self.open_second_form()

    def open_second_form(self):
        pygame.init()
        pygame.key.set_repeat(200, 70)

        FPS = 50
        WIDTH = 900
        HEIGHT = 900
        STEP = 10

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        player = None
        tile_width = tile_height = 50
        o = ['map', 'map2']
        player, level_x, level_y = generate_level(load_level(random.choice(o)))
        camera = Camera((level_x, level_y))
        dragon = Heroes(load_image("enemy3.png"), load_image("enemy3.png"), 5, 2, 50, 50)
        dragon1 = Heroes(load_image("enemy3.png"), load_image("enemy3.png"), 5, 2, 340, 50)
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
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                                player.update(5)
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                                player.update(6)
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'door':
                                player.update(7)
                    elif event.key == pygame.K_DOWN:
                        player.update(1)
                        for el in tiles_group:
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                                player.update(2)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                                player.update(5)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                                player.update(6)
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'door':
                                player.update(7)
                    elif event.key == pygame.K_UP:
                        player.update(2)
                        for el in tiles_group:
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                                player.update(1)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                                player.update(5)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                                player.update(6)
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'door':
                                player.update(7)
                    elif event.key == pygame.K_RIGHT:
                        player.update(3)
                        for el in tiles_group:
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                                player.update(4)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                                player.update(5)
                            if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                                player.update(6)
                            elif player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'door':
                                player.update(7)

            camera.update(player)

            for sprite in all_sprites1:
                camera.apply(sprite)
            dragon.update1(player)
            dragon1.update1(player)

            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)

            all_sprites1.draw(screen)
            player_group.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)
        self.hide()
        terminate()


def e(a, b, c):
    sys.__excepthook__(a, b, c)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = e
    ex = Example()
    ex.show()
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("./fondb.png")))
    ex.setPalette(palette)
    sys.exit(app.exec())

