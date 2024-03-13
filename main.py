import pygame
from Level.Level import Level
from Sprites import tiles_group, characters_group, tile_width, tile_height, all_sprites, Camera, setInformation










pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size, flags=pygame.SRCALPHA)
surf = pygame.Surface((220, 100))
surf.fill(pygame.Color("black"))
surf.set_alpha(180)
level = Level()
level.load_level("Level1")
level.generateLevel()
x = 0
y = 0

# board.set_view(10, 10, 100)
running = True
camera = Camera(width, height, level.character)
while running:
    # print(f"Character = {level.character.rect}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            level.tick("shot", x, y)
        if event.type == pygame.MOUSEMOTION:
            y = (event.pos[1] - camera.y) // tile_height
            x = (event.pos[0] - camera.x) // tile_width
            level.hover(x, y)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d:
                level.tick("right")
            elif event.key == pygame.K_w:
                level.tick("up")
            elif event.key == pygame.K_s:
                level.tick("down")
            elif event.key == pygame.K_a:
                level.tick("left")
            elif event.key == pygame.K_h:
                print(x, y)
                print(camera.x, camera.y)

    setInformation(surf, level.character)
    screen.fill("sienna")
    tiles_group.draw(screen)
    camera.update()
    for sprite in all_sprites:
        camera.apply(sprite)
    characters_group.draw(screen)
    screen.blit(surf, (10, 10))
    pygame.display.flip()
    pygame.time.delay(10)
