import pygame
from Level.Level import Level
from Sprites import tiles_group, characters_group, tile_width, tile_height, all_sprites, Camera, setInformation, \
    bullet_group, enemies_group, inventoryDraw, Weapon, cellItems_group, inventoryItems_group, activeWeapon_group, menuDraw

WINDOWS = ("game", "inventory", "main-menu")
opened = WINDOWS[2]

pygame.init()
size = width, height = 640, 500
screen = pygame.display.set_mode(size, flags=pygame.SRCALPHA)
surf = pygame.Surface((220, 100))
surf.fill(pygame.Color("black"))
surf.set_alpha(180)
inventorySurf = pygame.Surface((width, height))
inventorySurf.fill(pygame.Color("black"))
inventorySurf.set_alpha(220)

menuSurf = pygame.Surface((width, height))
menuSurf.fill(pygame.Color((0, 178, 255)))

level = Level()
level.load_level("Level1")
level.generateLevel()
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.map[1][1].addItemToCell(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())
level.character.inventory.addItem(Weapon())


x = 0
y = 0

clock = pygame.time.Clock()
dt = 0
FPS = 60
# board.set_view(10, 10, 100)
running = True
camera = Camera(width, height, level.character)


while running:
    # print(f"Character = {level.character.rect}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if opened == WINDOWS[0]:
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
                elif event.key == pygame.K_TAB:
                    opened = WINDOWS[1]
        elif opened == WINDOWS[1]:
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] <= 240:
                    cellItems_group.update(event)
                    inventoryItems_group.update()
                elif event.pos[0] >= 400:
                    cellItems_group.update()
                    event.pos = (event.pos[0] - 400, event.pos[1])
                    inventoryItems_group.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    choise = ""
                    if event.pos[0] <= 240:
                        for elem in cellItems_group.sprites():
                            choise = elem.update(event)
                            if choise:
                                break
                        if choise:
                            level.tick("take", choise)
                    elif event.pos[0] >= 400:
                        event.pos = (event.pos[0] - 400, event.pos[1])
                        for elem in inventoryItems_group.sprites():
                            choise = elem.update(event)
                            if choise:
                                break
                        if choise:
                            level.tick("drop", choise)

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        opened = WINDOWS[0]
    screen.fill("sienna")
    tiles_group.draw(screen)
    tick = clock.tick(FPS) / 1000
    if opened == WINDOWS[0]:
        setInformation(surf, level.character)
        dt += tick
        if dt >= 1:
            dt = 0
            level.moveEnemy()

        camera.update()
        for sprite in all_sprites:
            camera.apply(sprite, tick)
        if bullet_group:
            bullet_group.update(tick)
        screen.blit(surf, (10, 10))
        characters_group.draw(screen)
        enemies_group.draw(screen)
        bullet_group.draw(screen)
    elif opened == WINDOWS[1]:
        inventoryDraw(inventorySurf, level)
        screen.blit(inventorySurf, (0, 0))
        characters_group.draw(screen)
        enemies_group.draw(screen)
        bullet_group.draw(screen)
    elif opened == WINDOWS[2]:
        menuDraw(menuSurf)
        screen.blit(menuSurf, (0, 0))


    pygame.display.flip()
    pygame.time.delay(10)
