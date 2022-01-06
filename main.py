import pygame
import sys
import os

pygame.font.init()
FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None


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
    with open('18.txt', 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def ninja():
    pygame.init()
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    screen.fill((0,0,0))
    nindja = AnimatedSprite(load_image("njump.png"), 9, 1, 50, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        tiles_group.draw(screen)
        all_sprites.update()
        clock.tick(4)
        all_sprites.draw(screen)
        pygame.display.flip()
ninja()