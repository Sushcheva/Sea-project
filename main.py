import pygame
import sys
import os
from random import sample, randrange, choices

pygame.font.init()
FPS = 60
all_sprites = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
person_group = pygame.sprite.Group()
player = None


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, image1, columns, rows, x, y):
        super().__init__(all_sprites)
        self.image1 = image1
        self.z = 1
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
            if self.z >= 2.5:
                self.image = load_image(self.image1)
                self.image = pygame.transform.scale(self.image, (78 * 3, 197 * 3))
            else:
                self.image = load_image(self.image1)
                self.image = pygame.transform.scale(self.image, (78 * self.z, 197 * self.z))


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


class CloudsText(pygame.sprite.Sprite):
    def __init__(self, hero, number):
        super().__init__(person_group, all_sprites)
        self.hero = player_image
        self.number = number
        self.image = load_image('cloud.jpg', None)
        self.rect = self.image.get_rect().move(
            400, 400)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class Fruit(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, time, image1):
        super().__init__(fruit_group, all_sprites)
        self.image1 = image1
        self.time = time
        self.v0 = randrange(1, 10)
        self.image = pygame.transform.scale(load_image(image, None), (50, 50))
        self.rect = self.image.get_rect().move(
            pos_x, 500)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, t):
        if self.time >= t:
            self.rect = self.image.get_rect().move(
                0, -self.v0 + 0.1)
            self.v0-= 0.1


def ninja():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('les.png'), (500, 500))
    nindja = Heroes(load_image("njump.png"), 'njump1.png', 9, 1, 50, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        screen.blit(fon, (0, 0))
        all_sprites.update()
        clock.tick(8)
        all_sprites.draw(screen)
        pygame.display.flip()
    running = True
    z = ['apple.png', 'apple.png', 'apple.png', 'mango.png', 'mango.png', 'banana.png', 'banana.png', 'coconut.jpg',
         'coconut.jpg','granat.png', 'pear.png', 'pineapple.png', 'pineapple.png', 'pineapple.png', 'strawberry.png',
         'strawberry.png', 'strawberry.png', 'bomb.png', 'bomb.png', 'bomb.png']
    t = 0
    z1 = sample(z, 20)
    g = 0
    z2 = []
    for i in range(20):
        z2.append(randrange(50, 750, 10))
    for el in z1:
        Fruit(el, randrange(10, 450), z2[g], el)
        g += 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        t += 50
        screen.blit(fon, (0, 0))
        fruit_group.update(t)
        clock.tick(50)
        fruit_group.draw(screen)
        pygame.display.flip()


ninja()
