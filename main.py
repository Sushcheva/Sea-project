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
