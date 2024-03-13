import os
import sys
import pygame

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
characters_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
interface_group = pygame.sprite.Group()


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
}

character_images = {
    "oper": load_image('operative.png'),
    "enemy": load_image('zombie_wild.png')
}

item_images = {
    "pistol": load_image('pistol.png')
}

tile_width = tile_height = 32


def setInformation(surface, player):
    surface.fill((0, 0, 0))

    font = pygame.font.Font(None, 30)
    text = font.render(f"HP: {player.health}", True, (255, 255, 255))
    surface.blit(text, (10, 10))
    surface.blit(player.activeWeapon.image, (10, 30))
    text = font.render(f'{player.activeWeapon.name.capitalize()}: {player.activeWeapon.bullets} / {player.activeWeapon.maxBullets}', True,
                       (255, 255, 255))
    surface.blit(text, (70, 40))


class Camera:
    def __init__(self, width, height, target):
        self.width = width
        self.height = height
        self.target = target
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

    # def apply(self, obj):
    #     obj.rect.x += self.dx
    #     obj.rect.y += self.dy
    #
    #
    # def update(self):
    #     print(f"target.rect.x = {self.target.rect.x}; target.rect.w = {self.target.rect.w}; self.width // 2 = {self.width // 2}")
    #     print(f"self.dx = {self.dx}; self.dy = {self.dy}")
    #     if -(self.target.rect.x + self.target.rect.w // 2 - self.width // 2 != self.dx):
    #         self.dx = self.dx + (self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
    #     if -(self.target.rect.y + self.target.rect.h // 2 - self.height // 2) != self.dy:
    #         self.dy = self.dy + (self.target.rect.y + self.target.rect.h // 2 - self.height // 2)

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if self.dx != 0 or self.dy != 0:
            if obj != self.target:
                obj.update()
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self):
        # if self.dx != 0 or self.dy != 0:
        #     print(f'self.dx = {self.dx}; self.dy = {self.dy}')
        # else:
        #     print(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.dx = -(self.target.rect.x + self.target.rect.w // 2 - self.width // 2)
        self.dy = -(self.target.rect.y + self.target.rect.h // 2 - self.height // 2)
        if self.dx != 0:
            # print(f'self.dx = {self.dx}; self.dy = {self.dy}')
            self.x += self.dx - self.x
        if self.dy != 0:
            self.y += self.dy - self.y
            # print(f'self.x = {self.x}; self.y = {self.y}')

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

    def canMove(self):
        if self.tileType == "wall":
            return False
        return True

    def changeType(self, newType):
        self.image = tile_info.get(newType, False)[0]
        if not self.image:
            print(f"Ничего не найдено. Типа {newType} не существует")
            sys.exit()
        self.rect = self.image.get_rect().move(
            self.rect.x, self.rect.y)
        self.tileType = newType

    def update(self):
        self.rect.x = tile_width * self.x
        self.rect.y = tile_height * self.y


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
        print(f'Players position: {self.rect.x}, {self.rect.y}')

    def shot(self, x, y, levelMap):
        if self.activeWeapon.bullets == 0:
            return
        else:
            self.activeWeapon.bullets -= 1

    def takeItem(self, item):
        self.inventory.addItem(item)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(characters_group, all_sprites)
        self.image = character_images["enemy"]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        self.rect.x = tile_width * self.x
        self.rect.y = tile_height * self.y

    def move(self):
        pass


class Inventory:
    def __init__(self):
        self.items = []
        self.currentWeight = 0
        self.maxWeight = 1000


    def addItem(self, item):
        if self.currentWeight + item.weight <= self.maxWeight:
            self.items.append(item)
            self.currentWeight += item.weight
        else:
            return

    def deleteItem(self, index):
        dropped = self.items.pop(index)
        self.currentWeight -= dropped.weight
        return dropped



class Item:
    def __init__(self, type="weapon", weight=0):
        self.type = type
        self.weight = weight

    def use(self, player):
        raise NotImplementedError("Subclass must implement abstract method")



class Weapon(Item):
    def __init__(self, type="pistol"):
        super(Weapon, self).__init__("weapon", 0)
        self.name = type
        self.image = item_images.get(type, False)
        if self.image:
            if type == "pistol":
                self.bullets = 12
                self.maxBullets = 12
                self.weight = 15
            elif type == "awp":
                self.bullets = 5
                self.maxBullets = 5
                self.weight = 25

    def use(self, player):
        pass

    def reload(self):
        self.bullets = self.maxBullets
