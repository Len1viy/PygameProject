import os
import sys
import pygame

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
characters_group = pygame.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join('data/imgs', name)
    print(fullname)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_images = {
    'tile': load_image('tile.png'),
    'wall': load_image('wall_1.png'),
}

character_images = {
    "oper": load_image('operative.png')
}

tile_width = tile_height = 50


class Cell(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)






class Operative(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(characters_group, all_sprites)
        self.image = character_images["oper"]
        self.x = pos_x
        self.y = pos_y
        self.timePoints = 50
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, direction):
        if direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        elif direction == "down":
            self.y += 1
        elif direction == "up":
            self.y -= 1
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)






