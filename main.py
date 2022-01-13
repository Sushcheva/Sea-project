import sys
import sqlite3
import pygame
import os
import random

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, \
     QInputDialog, QLabel, QMessageBox
from PyQt5 import QtGui  # для измениения шрифта
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QInputDialog, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QMovie, QPainter
st = 0

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 800
HEIGHT = 800
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
        image.set_colorkey((0, 0, 0))
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




def over_game():
    pygame.init()
    size1 = 1000, 1000
    screen1 = pygame.display.set_mode(size1)
    clock1 = pygame.time.Clock()
    fon1 = pygame.transform.scale(load_image('game over.png'), (500, 500))
    exit(screen)
    quit(screen1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                     terminate()



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
            elif level[y][x] == '$':
                Tile('star', x, y)
            elif level[y][x] == '!':
                Tile('enemy', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()

tile_images = {'wall': load_image('box1.png'), 'empty': load_image('grass.png'), 'enemy': load_image('en.png'), \
               'star': load_image('star.png')}
player_image = load_image('mar2.png')

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
        if event == 6:
            st += 1
            el.image
            print(st)


o = ['map', 'map2', 'map3']
player, level_x, level_y = generate_level(load_level(random.choice(o)))

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


camera = Camera((level_x, level_y))


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


dragon = AnimatedSprite(load_image("enemy3.png"), 5, 2, 50, 50)



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
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                        player.update(5)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                        player.update(6)
            elif event.key == pygame.K_DOWN:
                player.update(1)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(2)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                        player.update(5)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                        player.update(6)
            elif event.key == pygame.K_UP:
                player.update(2)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(1)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                        player.update(5)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                        player.update(6)
            elif event.key == pygame.K_RIGHT:
                player.update(3)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'wall':
                        player.update(4)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'enemy':
                        player.update(5)
                for el in tiles_group:
                    if player.pos_x == el.pos_x and player.pos_y == el.pos_y and el.tile_type == 'star':
                        player.update(6)

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)
    dragon.update()

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)

    all_sprites.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)


terminate()