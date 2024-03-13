import os
import sys
import pygame

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
characters_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()


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
    "oper": load_image('operative.png')
}

tile_width = tile_height = 32


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
            tile_width * self.x, tile_height * self.y)
        self.tileType = newType


class Operative(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(characters_group, all_sprites)
        self.image = character_images["oper"]
        self.x = pos_x
        self.y = pos_y
        self.timePoints = 50
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, direction, map):
        if direction == "left" and map[self.y][self.x - 1].canMove():
            self.x -= 1
        elif direction == "right" and map[self.y][self.x + 1].canMove():
            self.x += 1
        elif direction == "down" and map[self.y + 1][self.x].canMove():
            self.y += 1
        elif direction == "up" and map[self.y - 1][self.x].canMove():
            self.y -= 1
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)
