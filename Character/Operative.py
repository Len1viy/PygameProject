from Cell import Cell
from Character.Character import Character, Point
from Inventory import Inventory
from Inventory.Weapon import Weapon

class Operative(Character):
    def __init__(self, name="", point=Point(0, 0), cell=Cell(0, 0), side="player", type="Operative", strength=0, accuracy=0, inventory=Inventory(), weapon=Weapon()):
        Character.__init__(self)
        self.name = "Operative"
        self.strength = strength
        self.accuracy = accuracy
        self.point = point
        self.cell = cell
        self.inventory = inventory
        self.weapon = weapon