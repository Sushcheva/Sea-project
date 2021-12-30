import pygame
import sys
import os
pygame.font.init()
FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        for i in range(self.height):
            self.board1 = []
            for j in range(self.width):
                self.board1.append([j, i, 0])
            self.board.append(self.board1)
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or mouse_pos[0] > 500 - self.left or mouse_pos[1] < self.top or mouse_pos[
            1] > self.top + self.cell_size * self.height:
            return None
        else:
            return ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)

    def get_click(self, mouse_pos, screen):
        cell = self.get_cell(mouse_pos)
        print(cell)
        if cell != None:
            self.draw(cell[0], cell[1], screen)
        else:
            self.draw(1000, 1000, screen)


    def draw(self, x1, y1, screen):
        for el in self.board:
            for el1 in el:
                if el1[0] == x1 and el1[1] == y1:
                    if el1[2] == 0:
                        pygame.draw.rect(screen, (255, 0, 0), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 0)
                        z = self.board.index(el)
                        m = el.index(el1)
                        self.board[z][m][2] += 1
                    elif el1[2] == 1:
                        pygame.draw.rect(screen, (0, 0, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 0)
                        pygame.draw.rect(screen, (255, 255, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)
                        z = self.board.index(el)
                        m = el.index(el1)
                        self.board[z][m][2] += 1
                    elif el1[2] == 2:
                        pygame.draw.rect(screen, (0, 0, 0), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 0)
                        pygame.draw.rect(screen, (255, 255, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)
                        z = self.board.index(el)
                        m = el.index(el1)
                        self.board[z][m][2] = 0
                else:
                    if el1[2] == 0:
                        pygame.draw.rect(screen, (255, 255, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)

                    elif el1[2] == 1:
                        pygame.draw.rect(screen, (255, 0, 0), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 0)
                        pygame.draw.rect(screen, (255, 255, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)
                    elif el1[2] == 2:
                        pygame.draw.rect(screen, (0, 0, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 0)
                        pygame.draw.rect(screen, (255, 255, 255), (
                            el1[0] * self.cell_size + self.left, el1[1] * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)


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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    size = WIDTH, HEIGHT = 1000, 500

    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('octopus.png', -1), (327, 200))
    screen.blit(fon, (500, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def fut():
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
                most()
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


def most():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('g')
    board = Board(1, 7)
    board.set_view(100, 100, 50)
    board1 = Board(1, 7)
    board1.set_view(200, 100, 50)
    screen.fill((0, 0, 0))
    board1.render(screen)
    board.render(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                board.render(screen)
                board1.render(screen)
                board.get_click(event.pos, screen)
                board1.get_click(event.pos, screen)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

start_screen()