def ti():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    fon = pygame.transform.scale(load_image('game_over.png'), (500, 500))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ninja()
        screen.blit(fon, (0, 0))
        clock.tick(8)
        pygame.display.flip()

