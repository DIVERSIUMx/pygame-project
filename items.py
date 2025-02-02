import pygame
from sprites import ItemSprite, load_image
from tric import Item, MainBoard


class MegaItems(Item):  # Класс, к которому принадлежат все элементы
    def __init__(self, board: MainBoard):
        super().__init__(board)
        self.colide_type = 0
        self.stop = False
        self.death = False
        self.push = False
        self.sink = False
        self.win = False
        self.weak = False
        self.you = False

    # Все функции отвечающие за изменение правил внутри элемента блока текста
    def set_death(self, act: bool):
        self.death = act

    def set_stop(self, act: bool):
        self.stop = act

    def set_sink(self, act: bool):
        self.sink = act

    def set_weak(self, act: bool):
        self.weak = act

    def set_push(self, act: bool):
        self.push = act

    def set_win(self, act: bool):
        self.win = act

    def set_you(self, act: bool):
        self.you = act

    def get_rules(self):
        return (self.stop,
                self.death,
                self.push,
                self.sink,
                self.win,
                self.weak,
                self.you)

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


class Moris(MegaItems):
    sprite = ItemSprite("moris", load_image("moris.png"), 8)
    name = "Moris"
    color = (50, 250, 255)


class Box(MegaItems):
    sprite = ItemSprite("box", load_image("box.png"))
    name = "Box"
    color = (150, 150, 0)


class Wall(MegaItems):
    sprite = ItemSprite("wall", load_image("wall.png"))
    name = "Wall"
    color = (50, 50, 255)


class Rock(MegaItems):
    sprite = ItemSprite("water", load_image("rock.png"))
    name = "Rock"
    color = 'orange'


class Water(MegaItems):
    sprite = ItemSprite("water", load_image("water.png"), 6)
    name = "Water"
    color = (0, 0, 255)


class Flag(MegaItems):
    sprite = ItemSprite("flag", load_image("flag.png"), 6)
    name = "Flag"
    color = (0, 0, 255)


class Skull(MegaItems):
    sprite = ItemSprite("skull", load_image("skull.png"), 4)
    name = "Flag"
    color = (0, 0, 255)


# Игровые доски
board = MainBoard(16, 10, 80)
test_board = MainBoard(16, 10, 80)

# Элементы классов
moris = Moris(board)
wall = Wall(board)
flag = Flag(board)
box = Box(board)
rock = Rock(board)
skull = Skull(board)
