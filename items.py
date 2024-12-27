import pygame
from tric import Item, Rule


class Moris(Item):
    name = "Moris"
    color = (50, 250, 255)
    rule = Rule()


class Box(Item):
    name = "Box"
    color = (150, 150, 0)
    rule = Rule()


class Wall(Item):
    name = "Wall"
    color = (50, 50, 255)
    rule = Rule()


class Water(Item):
    name = "Water"
    color = (0, 0, 255)
    rule = Rule()
