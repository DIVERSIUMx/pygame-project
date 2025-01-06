import pygame
from tric import Item, Rule, MainBoard


class MegaItems(Item):  # лень менять в другом файле
    def __init__(self, board: MainBoard):
        super().__init__(board)
        self.colide_type = 0
        self.stop = False
        self.death = False
        self.push = False
        self.sink = False
        self.win = False
        self.weak = False

    def set_death(self, act: bool):
        self.death = act

    def set_stop(self, act: bool):
        self.stop = act

    def set_sink(self, act: bool):
        self.sink = act

    def set_push(self, act: bool):
        self.push = act

    def set_win(self, act: bool):
        self.win = act

    def get_colide_type(self):
        if self.stop:
            return 100
        elif self.push:
            return 90
        elif self.death:
            return 20
        elif self.win:
            return 1
        else:
            return 0

    def get_rules(self):
        return (self.stop, self.death, self.push, self.sink, self.win, self.weak)


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
    color = "orange"
    rule = Rule()


class Water(MegaItems):
    name = "Water"
    color = (0, 0, 255)
    rule = Rule()


board = MainBoard(16, 10, 80)
wall = Wall(board)
box = Box(board)
rock = Rock(board)
print(wall.get_rules(), 222)
