import os
import sys

import pygame

from Sprites import Cell
from Sprites import Operative


class Level:
    def __init__(self):
        self.map = []
        self.width, self.height = 0, 0
        self.characters = []
        self.enemies = []

    def load_level(self, directory):
        dir_with_level = "data/ConfigurationsFiles/" + directory
        characters_for_level = dir_with_level + "/Characters"
        items_for_level = dir_with_level + "/Items"
        maps_for_level = dir_with_level + "/Map"
        with open(maps_for_level, 'r') as mapFile:
            self.width = int(mapFile.readline().strip())
            self.height = int(mapFile.readline().strip())
            self.map = [list(line.strip()) for line in mapFile]
        with open(characters_for_level, 'r') as charactersFile:
            size = int(charactersFile.readline().strip())
            for i in range(size):
                if charactersFile.readline().strip() == "Operative":
                    x = int(charactersFile.readline().strip())
                    y = int(charactersFile.readline().strip())
                    print(x, y)
                    self.characters.append(Operative(x, y))

        # return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generateLevel(self):
        # new_player, x, y = None, None, None
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == '0':
                    self.map[y][x] = Cell('wall', x, y)
                # elif self.map[y][x] == 'G':
                #     Cell('wall', x, y)
                elif self.map[y][x] == "-":
                    self.map[y][x] = Cell('tile', x, y)


    def movePlayer(self, instruction):
        if instruction == "left":
            self.characters[0].move("left")
        elif instruction == "right":
            self.characters[0].move("right")
        elif instruction == "up":
            self.characters[0].move("up")
        elif instruction == 'down':
            self.characters[0].move("down")

    def moveEnemy(self):
        pass