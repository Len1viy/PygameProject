import pygame
from Level.Level import Level
from Sprites import tiles_group, characters_group, tile_width, tile_height, Cell

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

level = Level()
level.load_level("Level1")
level.generateLevel()

# board.set_view(10, 10, 100)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # board.getClick(event.pos)
            pass
        if event.type == pygame.MOUSEMOTION:
            y = event.pos[1] // tile_height
            x = event.pos[0] // tile_width
            level.hover(x, y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                level.movePlayer("right")
            elif event.key == pygame.K_w:
                level.movePlayer("up")
            elif event.key == pygame.K_s:
                level.movePlayer("down")
            elif event.key == pygame.K_a:
                level.movePlayer("left")

    screen.fill((100, 100, 100))
    tiles_group.draw(screen)
    characters_group.draw(screen)
    pygame.display.flip()
