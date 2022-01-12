import pygame
import sys
import os
from random import sample, randrange, choice

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
        for scale in (15, 20, 25, 25, 50, 75, 100):
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


def create_particles(position, image):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers), image)


tile_images = {
    'wall': load_image('box.png', None),
    'empty': load_image('grass.png', None)
}
player_image = load_image('mar.png', None)

tile_width = tile_height = 50


class CloudsText(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__(person_group, all_sprites)
        f = open('18.txt')
        f = f.readlines()
        self.f = f
        self.hero = hero
        for el in f:
            if el == hero:
                self.number = self.f.index(el) + 1
        self.image = load_image('cloud.png', None)
        self.rect = self.image.get_rect().move(
            400, 400)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,n):
        self.f[n]


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
        super().__init__(fruit_group, all_sprites)
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

    def update(self, t):
        if self.time <= t:
            t1 = t / 100 - self.time / 100
            if self.v0 < 0:
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.x0 + self.v0 * t1 + 0.8 * (t1 ** 2))

                self.z = self.x0 + self.v0 * t1 + 0.8 * (t1 ** 2)
                self.v0 += 1.6
            else:
                self.rect = self.image.get_rect().move(
                    self.pos_x, self.x0 - self.v0 * t1 + 0.8 * (t1 ** 2))

                self.z = self.x0 - self.v0 * t1 + 0.8 * (t1 ** 2)
                self.v0 -= 1.6

        elif self.z > 500 or self.v0 == self.v1:
            self.image = pygame.transform.scale(load_image('w.png', None), (10, 10))
            self.rect = self.image.get_rect().move(
                self.pos_x, 600)
            self.mask = pygame.mask.from_surface(self.image)

    def update2(self, el1):
        if self.pos_x <= el1[0] <= self.pos_x + 100 and self.z <= el1[1] <= self.z + 100:
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
    z1 = sample(z, 50)
    g = 0
    z2 = []
    lifes = 3
    for i in range(50):
        z2.append(randrange(100, 2500))
    for el in z1:
        Fruit(el, randrange(0, 400), z2[g], str(el[:-4] + '1' + el[-4:]))
        g += 1
    while running:
        y = False
        x = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Strix('pt.png', event.pos, t)
                for el in fruit_group:
                    el.update2(event.pos)

        t += 1
        screen.blit(fon, (0, 0))

        for el in fruit_group:
            el.update(t)
        strix_group.update()
        strix_group.draw(screen)
        fruit_group.draw(screen)
        pygame.display.flip()
        clock.tick(100)


ninja()
