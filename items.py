import pygame
from tric import Item, Rule, MainBoard


class MegaItems(Item):  # лень менять в другом файле
    def __init__(self, board: MainBoard):
        super().__init__(board)
        self.stop = False
        self.deth = False
        self.push = False
        self.silk = False
        self.win = False
        self.weak = False

    def set_deth(self, act: bool):
        self.deth = act

    def set_stop(self, act: bool):
        self.stop = act

    def set_silk(self, act: bool):
        self.silk = act

    def set_push(self, act: bool):
        self.push = act

    def set_win(self, act: bool):
        self.win = act


    def get_rules(self):
        return (self.stop,
                self.deth,
                self.push,
                self.silk,
                self.win,
                self.weak)


class Moris(MegaItems):
    name = "Moris"
    color = (50, 250, 255)
    rule = Rule()


class Box(MegaItems):
    name = "Box"
    color = (150, 150, 0)
    rule = Rule()


class Wall(MegaItems):
    name = "Wall"
    color = (50, 50, 255)
    rule = Rule()


class Rock(MegaItems):
    name = "Rock"
    color = 'orange'
    rule = Rule()


class Water(MegaItems):
    name = "Water"
    color = (0, 0, 255)
    rule = Rule()


wall = Wall(MainBoard)
box = Box(MainBoard)
rock = Rock(MainBoard)
print(wall.get_rules(), 222)
