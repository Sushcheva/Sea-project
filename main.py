import pygame
import sys
import os

pygame.font.init()
FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_images = {
    'wall': load_image('box.png', None),
    'empty': load_image('grass.png', None)
}
player_image = load_image('mar.png', None)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        print(tile_type)


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


def terminate():
    fut()

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

    return new_player, x, y


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open('18.txt', 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def ninja():
    pygame.init()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    player, level_x, level_y = generate_level(load_level('18.txt'))
    clock = pygame.time.Clock()

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

        tiles_group.draw(screen)
        all_sprites.update(event)

        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
