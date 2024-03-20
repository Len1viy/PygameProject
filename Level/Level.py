from Sprites import Cell
from Sprites import Operative, Enemy


class Level:
    def __init__(self):
        self.map = []
        self.width, self.height = 0, 0
        self.character = 0
        self.enemies = []
        self.side = "player"

    def load_level(self, directory):
        dir_with_level = "data/ConfigurationsFiles/" + directory
        characters_for_level = dir_with_level + "/Characters"
        items_for_level = dir_with_level + "/Items"
        maps_for_level = dir_with_level + "/Map"
        with open(maps_for_level, 'r') as mapFile:
            self.height = int(mapFile.readline().strip())
            self.width = int(mapFile.readline().strip())
            self.map = [list(line.strip()) for line in mapFile]
        with open(characters_for_level, 'r') as charactersFile:
            size = int(charactersFile.readline().strip())
            for i in range(size):
                if charactersFile.readline().strip() == "Operative":
                    x = int(charactersFile.readline().strip())
                    y = int(charactersFile.readline().strip())
                    self.character = Operative(x, y)
                if charactersFile.readline().strip() == "Wild":
                    x = int(charactersFile.readline().strip())
                    y = int(charactersFile.readline().strip())
                    self.enemies.append(Enemy(x, y))

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

    def tick(self, *instruction):
        if self.side == "player":
            self.movePlayer(instruction)
        else:
            self.moveEnemy()

    def getItems(self, x, y):
        return self.map[y][x].items

    def movePlayer(self, instruction):
        if instruction[0] == "left" and self.character.x > 0:
            self.character.move("left", self.map)
        elif instruction[0] == "right" and self.character.x < self.width - 1:
            self.character.move("right", self.map)
        elif instruction[0] == "up" and self.character.y > 0:
            self.character.move("up", self.map)
        elif instruction[0] == 'down' and self.character.y < self.height - 1:
            self.character.move("down", self.map)
        elif instruction[0] == "shot":
            self.character.shot(instruction[1], instruction[2], self.map)
        elif instruction[0] == "take":
            self.character.takeItem(self.map[self.character.y][self.character.y].deleteItemFromCell(instruction[1]))
        elif instruction[0] == "drop":
            self.map[self.character.y][self.character.y].addItemToCell(self.character.dropItem(instruction[1]))
            # self.map[self.character.y][self.character.y].deleteItemFromCell(instruction[1])

    def hover(self, x, y):
        if 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1:
            if self.map[y][x].tileType == "tile":
                self.map[y][x].changeType("tile_underAttack")
            self.unselectOther(x, y)

    def moveEnemy(self):
        for i in self.enemies:
            i.move(self.map)

    def unselectOther(self, x, y):
        for i in range(self.width):
            for j in range(self.height):
                if self.map[j][i] != self.map[y][x] and self.map[j][i].tileType == "tile_underAttack":
                    self.map[j][i].changeType("tile")
