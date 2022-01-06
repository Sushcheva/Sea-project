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
