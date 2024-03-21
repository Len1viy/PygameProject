import os
import random
import sys
import pygame
from math import sqrt
from Level import Level

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
characters_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
cellItems_group = pygame.sprite.Group()
inventoryItems_group = pygame.sprite.Group()
activeWeapon_group = pygame.sprite.Group()
textMenu_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data/imgs', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_info = {
    'tile': [load_image('simple_tile.png'), all_sprites, tiles_group],
    'wall': [load_image('wall.png'), all_sprites, tiles_group, borders_group],
    'tile_underAttack': [load_image('tileUnderAttack.png'), all_sprites, tiles_group],
    'mark': [load_image('mark.png'), all_sprites, tiles_group],
}

character_images = {
    "oper": load_image('operative.png'),
    "enemy": load_image('zombie_wild.png')
}

item_images = {
    "pistol": load_image('pistol.png'),
    "selected_pistol": load_image('selected_pistol.png')
}

menu_images = {
    "start": load_image("start.png"),
    "exit": load_image("exit.png"),
    "selected_start": load_image("selected_start.png"),
    "selected_exit": load_image("selected_exit.png")
}

tile_width = tile_height = 32


def setInformation(surface, player):
    surface.fill((0, 0, 0))

    font = pygame.font.Font(None, 30)
    text = font.render(f"HP: {player.health}", True, (255, 255, 255))
    surface.blit(text, (10, 10))
    surface.blit(player.activeWeapon.image, (10, 30))
    text = font.render(
        f'{player.activeWeapon.type.capitalize()}: {player.activeWeapon.bullets} / {player.activeWeapon.maxBullets}',
        True,
        (255, 255, 255))
    surface.blit(text, (70, 40))


def inventoryDraw(surface: pygame.Surface, level):
    widthEdge, heightEdge = 240, 500
    widthMiddle, heightMiddle = 160, 500
    cellItemsSur = pygame.Surface((widthEdge, heightEdge))
    activeWeaponSur = pygame.Surface((widthMiddle, heightMiddle))
    inventorySur = pygame.Surface((widthEdge, heightEdge))
    cellItemsText, inventoryText, activeWeaponText = f"Items on the Cell", f"Inventory", f"Active Weapon"
    widthTexture, heightTexture, fontSize, maxItemsInARow = 48, 46, 30, 5
    font = pygame.font.Font(None, fontSize)
    text = font.render(cellItemsText, True, (255, 255, 255))
    cellItemsSur.blit(text, (widthEdge // 2 - text.get_width() // 2, 20))

    text = font.render(activeWeaponText, True, (255, 255, 255))
    activeWeaponSur.blit(text, (widthMiddle // 2 - text.get_width() // 2, 20))

    text = font.render(inventoryText, True, (255, 255, 255))
    inventorySur.blit(text, (widthEdge // 2 - text.get_width() // 2, 20))
    items = level.getItems(level.character.y, level.character.x)
    if len(items):
        print(len(items))
    dy = 50
    dx = 0
    cntCols = 0
    cntRows = 0
    for i in range(len(items)):
        item = items[i]
        cellItems_group.add(item)
        items_group.add(item)
        # print(widthTexture * cntCols + dx, end=" ")
        item.static(widthTexture * cntCols + dx, cntRows * heightTexture + dy)
        cntCols += 1
        cntRows += cntCols // 5
        cntCols = cntCols % 5
    cellItems_group.draw(cellItemsSur)
    items = level.character.inventory.items
    cntCols = 0
    cntRows = 0
    for i in range(len(items)):
        item = items[i]
        inventoryItems_group.add(item)
        items_group.add(item)
        item.static(widthTexture * cntCols + dx, cntRows * heightTexture + dy)
        cntCols += 1
        cntRows += cntCols // 5
        cntCols = cntCols % 5
    inventoryItems_group.draw(inventorySur)

    img = item_images[level.character.activeWeapon.type]
    activeWeaponSur.blit(img, (widthMiddle // 2 - widthTexture // 2, 300))

    surface.blit(inventorySur, (widthEdge + widthMiddle, 0))
    surface.blit(activeWeaponSur, (widthEdge, 0))
    surface.blit(cellItemsSur, (0, 0))


def menuDraw(surface: pygame.Surface):
    fontSize = 30
    font = pygame.font.Font(None, fontSize)
    if len(textMenu_group) != 2:
        start = Text("start")
        exit = Text("exit")
    textMenu_group.draw(surface)


class Camera:
    def __init__(self, width, height, target):
        self.width = width
        self.height = height
        self.target = target
        self.dx = -(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.dy = -(self.target.rect.y + self.target.rect.h // 2 - self.height // 2)
        self.x = -(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.y = -(self.target.rect.y + self.target.rect.h // 2 - self.height // 2)
        self.changeX = 0
        self.changeY = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, dt):
        if obj != self.target:
            if obj not in bullet_group:
                obj.update(self.x, self.y)
            else:
                obj.static(self.changeX, self.changeY)
        else:
            if self.dx != 0 or self.dy != 0:
                obj.update(self.x, self.y)

    # позиционировать камеру на объекте target
    def update(self):
        # if self.dx != 0 or self.dy != 0:
        #     print(f'self.dx = {self.dx}; self.dy = {self.dy}')
        # else:
        #     print(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.dx = -(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.dy = -(self.target.rect.y + self.target.rect.h // 2 - self.height // 2)
        # print(self.dx, self.dy, self.x, self.y)
        if self.dx != 0:
            self.changeX = self.dx - self.x
            self.x += self.dx - self.x
            print(f'self.dx = {self.dx}; self.dy = {self.dy}; self.changeX = {self.changeX}')
        else:
            self.changeX = 0
        if self.dy != 0:
            self.changeY = self.dy - self.y
            self.y += self.dy - self.y
            # print(f'self.x = {self.x}; self.y = {self.y}')
        else:
            self.changeY = 0

    def printData(self):
        for i in tiles_group:
            print(f"Sprite {i}. Rect: {i.rect}")
        print(len(tiles_group))


class Cell(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):

        super().__init__(*(tile_info[tile_type][1:]))
        self.x = pos_x
        self.y = pos_y
        self.tileType = tile_type.lower()
        self.image = tile_info[tile_type][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.items = []

    def canMove(self):
        if self.tileType == "wall":
            return False
        return True

    def changeType(self, newType):
        self.image = tile_info.get(newType, False)[0]
        if not self.image:
            print(f"Ничего не найдено. Типа {newType} не существует")
            sys.exit()
        # self.rect = self.image.get_rect().move(
        #     self.rect.x, self.rect.y)
        self.tileType = newType

    def update(self, dx, dy):
        if len(self.items) and self.tileType != "mark":
            self.changeType("mark")
        elif not len(self.items) and self.tileType == "mark":
            self.changeType("tile")
        self.rect.x = tile_width * self.x + dx
        self.rect.y = tile_height * self.y + dy

    def addItemToCell(self, item):
        self.items.append(item)

    def deleteItemFromCell(self, item):
        self.items.remove(item)
        cellItems_group.remove(item)
        return item


class Operative(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon="pistol"):
        super().__init__(characters_group, all_sprites)
        self.image = character_images["oper"]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 100
        self.activeWeapon = Weapon(weapon)
        self.inventory = Inventory()

    def move(self, direction, map):
        if direction == "left" and map[self.y][self.x - 1].canMove():
            self.x -= 1
        elif direction == "right" and map[self.y][self.x + 1].canMove():
            self.x += 1
        elif direction == "down" and map[self.y + 1][self.x].canMove():
            self.y += 1
        elif direction == "up" and map[self.y - 1][self.x].canMove():
            self.y -= 1
        # self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)
        self.rect.x = tile_width * self.x
        self.rect.y = tile_height * self.y
        # print(f'Players position: {self.rect.x}, {self.rect.y}')

    def shot(self, x, y, levelMap):
        if self.activeWeapon.bullets == 0 or x == self.x and y == self.y:
            return
        else:
            if 0 < x < len(levelMap[0]):
                if 0 < y < len(levelMap):
                    self.activeWeapon.bullets -= 1
                    Bullet(self.rect.x, self.rect.y, levelMap[y][x].rect.x, levelMap[y][x].rect.y,
                           self.activeWeapon.damage)

    def update(self, dx, dy):
        self.rect.x = tile_width * self.x + dx
        self.rect.y = tile_height * self.y + dy

    def takeItem(self, item):
        self.inventory.addItem(item)

    def dropItem(self, item):
        self.inventory.deleteItem(item)
        inventoryItems_group.remove(item)
        return item

    def use(self, item):
        self.inventory.addItem(self.activeWeapon)
        self.activeWeapon = item


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = load_image('zombie_wild.png')
        self.x = pos_x
        self.y = pos_y
        self.hp = 100
        pygame.draw.line(self.image, pygame.Color("green"), (0, 0), (self.image.get_width(), 0), width=4)
        if self.hp:
            pygame.draw.line(self.image, pygame.Color("blue"), (0, 0), (self.image.get_width() / 100 * self.hp, 0),
                             width=4)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dx, dy):
        pygame.draw.line(self.image, pygame.Color("green"), (0, 0), (self.image.get_width(), 0), width=4)
        if self.hp:
            pygame.draw.line(self.image, pygame.Color("blue"), (0, 0), (self.image.get_width() / 100 * self.hp, 0),
                             width=4)
        self.rect.x = tile_width * self.x + dx
        self.rect.y = tile_height * self.y + dy

    def move(self, map):
        vars = (map[self.y - 1][self.x], map[self.y + 1][self.x], map[self.y][self.x + 1], map[self.y][self.x - 1])
        choice = random.choice(vars)
        while not choice.canMove():
            choice = random.choice(vars)
        self.x = choice.x
        self.y = choice.y
        # print(self.x, self.y)

    def damage(self, dmg):
        if self.hp < dmg:
            self.hp = 0
        else:
            self.hp -= dmg

        if not self.hp:
            all_sprites.remove(self)
            enemies_group.remove(self)
            del self
            return


class Inventory:
    def __init__(self):
        self.items = []
        self.currentWeight = 0
        self.maxWeight = 1000

    def addItem(self, item):
        if self.currentWeight + item.weight <= self.maxWeight:
            self.items.append(item)
            self.currentWeight += item.weight
            inventoryItems_group.add(item)

        else:
            return

    def deleteItem(self, item):
        self.items.remove(item)
        inventoryItems_group.remove(item)
        cellItems_group.add(item)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, type="pistol", *group):
        super().__init__(*group)
        self.type = type
        self.hover = item_images.get(f'selected_{self.type}')
        self.notHover = item_images.get(self.type, False)
        self.image = self.notHover
        self.rect = self.image.get_rect().move(-10000, -10000)

        if self.image:
            if type == "pistol":
                self.bullets = 100
                self.maxBullets = 100
                self.weight = 15
                self.damage = 10
            elif type == "awp":
                self.bullets = 5
                self.maxBullets = 5
                self.weight = 25
                self.damage = 20

    def static(self, x, y):
        self.rect = self.image.get_rect().move(x, y)

    def update(self, *args):
        if not args:
            self.image = self.notHover
        elif args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.hover
        elif args and args[0].type == pygame.MOUSEMOTION and not \
                self.rect.collidepoint(args[0].pos):
            self.image = self.notHover
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if args[0].button == 1:
                print("left")
            elif args[0].button == 3:
                print("right")
            return self

    def use(self, player):
        pass

    def reload(self):
        self.bullets = self.maxBullets


class Bullet(pygame.sprite.Sprite):
    bullet = load_image("bullet.png")

    def __init__(self, start_posX, start_posY, end_posX, end_posY, damage):
        if start_posX == end_posX and start_posY == end_posY:
            return
        super().__init__(all_sprites, bullet_group)
        self.x = start_posX
        self.y = start_posY
        self.goalX, self.goalY = end_posX, end_posY
        self.image = self.bullet
        self.rect = self.image.get_rect().move(
            self.x, self.y)
        self.speed = 250
        self.damage = damage
        self.cos = (self.goalX - self.x) / (sqrt((self.goalY - self.y) ** 2 + (self.goalX - self.x) ** 2))
        self.sin = sqrt(1 - self.cos ** 2)
        self.k = 0
        self.b = 0
        if round(self.sin, 3) == 1 and self.cos < 0:
            self.cos = -1
            self.sin = 0
            # self.k = (self.y - self.goalY) / (self.x - self.goalX)
            self.k = self.sin / self.cos
            self.b = self.goalY - self.k * self.goalX
        elif round(self.sin, 3) == 1 and self.cos > 0:
            self.cos = 1
            self.sin = 0
            # self.k = (self.y - self.goalY) / (self.x - self.goalX)
            self.k = self.sin / self.cos

            self.b = self.goalY - self.k * self.goalX
        elif round(self.sin, 3) == 1 and self.cos == 0:
            if self.goalY > self.y:
                self.sin = 1
            else:
                self.sin = -1
        else:
            if self.goalY > self.y:
                self.sin = -self.sin
            self.k = self.sin / self.cos
            self.b = self.goalY - self.k * self.goalX
        #
        # print(self.x, self.y)
        #
        # print(f"self.speed * self.cos = {self.speed * self.cos}; self.speed * self.sin = {self.speed * self.sin} self.k = {self.k}")
        #

    def static(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.goalX += dx
        self.goalY += dy
        self.x += dx
        self.y += dy
        self.cos = (self.goalX - self.x) / (sqrt((self.goalY - self.y) ** 2 + (self.goalX - self.x) ** 2))
        self.sin = sqrt(1 - self.cos ** 2)
        self.k = 0
        self.b = 0
        if round(self.sin, 3) == 1 and self.cos < 0:
            self.cos = -1
            self.sin = 0
            # self.k = (self.y - self.goalY) / (self.x - self.goalX)
            self.k = self.sin / self.cos
            self.b = self.goalY - self.k * self.goalX
        elif round(self.sin, 3) == 1 and self.cos > 0:
            self.cos = 1
            self.sin = 0
            # self.k = (self.y - self.goalY) / (self.x - self.goalX)
            self.k = self.sin / self.cos

            self.b = self.goalY - self.k * self.goalX
        elif round(self.sin, 3) == 1 and self.cos == 0:
            if self.goalY > self.y:
                self.sin = 1
            else:
                self.sin = -1
        else:
            if self.goalY < self.y:
                self.sin = -self.sin
            self.k = self.sin / self.cos
            self.b = self.goalY - self.k * self.goalX

    def update(self, dt):
        if pygame.sprite.spritecollideany(self, borders_group):
            all_sprites.remove(self)
            bullet_group.remove(self)
            del self
            return
        if pygame.sprite.spritecollideany(self, enemies_group):
            pygame.sprite.spritecollideany(self, enemies_group).damage(self.damage)
            all_sprites.remove(self)
            bullet_group.remove(self)
            del self
            return
        # print(f"BULLET HERE: {self.rect.x}, {self.rect.y}")
        # print(f"self.speed * self.cos = {self.speed * self.cos}; self.speed * self.sin = {self.speed * self.sin}")

        if self.cos == 0:
            self.rect.y += self.speed * self.sin * dt
        elif self.cos == 1:
            self.rect.x += self.speed * self.cos * dt
        else:
            self.rect.x += self.speed * self.cos * dt
            self.rect.y = self.rect.x * self.k + self.b


class Text(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__(textMenu_group)
        self.text = text
        self.notHover = menu_images[text]
        self.image = self.notHover

        if text.lower() == "start":
            self.rect = self.image.get_rect().move(200, 100)
            self.hover = menu_images["selected_start"]
        elif text.lower() == "exit":
            self.rect = self.image.get_rect().move(200, 200)
            self.hover = menu_images["selected_exit"]

    def update(self, *args):
        if not args:
            return
        elif args and args[0].type == pygame.MOUSEMOTION and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.hover

        elif args and args[0].type == pygame.MOUSEMOTION and not \
                self.rect.collidepoint(args[0].pos):
            self.image = self.notHover

        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print("clicked")
            return self
        print(f"{self.text}: self.image == self.hover {self.image == self.hover}")
