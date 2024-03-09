from Cell import Cell
class Characteristics:
    def __init__(self):
        pass


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y



class Character:
    def __init__(self, name="", point=Point(0, 0), cell=Cell(0, 0), side="player", type="Operative") :
        self.name = ""
        self.characteristics = Characteristics()
        self.point = point
        self.side = side
        self.cell = cell
        self.type = type

