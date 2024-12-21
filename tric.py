# На счет имени, пока назвал так, потом поменяем FIXME
import pygame
import copy


class Rule:
    def __init__(self, cto):
        self.rules = []
        self.colide_type = 0

    def add_rule(self, rule_name: str):
        self.rules.append(rule_name)

    def set_colide_type(self, type):
        """0 - пусто
        10 - stop
        100 - push"""
        self.colide_type = max(self.colide_type, type)


class MainBoard:
    rules: dict[str, Rule] = dict()

    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.top = cell_size // 2
        self.left = cell_size // 2

        self.board = [[list()] * width for _ in range(height)]
        print(self.board)

        self.test()

    def get_screen_size(self):
        return self.width * self.cell_size + (
            2 * self.left
        ), self.height * self.cell_size + (2 * self.top)

    def render(self, surface):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                rect = (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(surface, (40, 40, 50), rect, 3)
                if cell is not None:
                    for item in cell:
                        item.render(surface, rect)

    def you_go(self, event_key):
        you_go_delta = 0, 0
        if event_key == pygame.K_w:
            you_go_delta = 0, -1
        elif event_key == pygame.K_s:
            you_go_delta = 0, 1
        elif event_key == pygame.K_a:
            you_go_delta = -1, 0
        elif event_key == pygame.K_d:
            you_go_delta = 1, 0
        else:
            return

        self.move(you_go_delta)

    def move(self, you_go_delta):
        """Функция для обработки хода"""
        self.new_board = [[[c for c in i] for i in r] for r in self.board]
        print(len(self.new_board[0]), self.width)
        print(len(self.new_board), self.height)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                for item in cell:
                    print(len(self.new_board[y][x]))
                    if item["you"]:
                        print("help")
                        item.try_step(
                            (x, y), (x + you_go_delta[0], y + you_go_delta[1])
                        )

        self.board = self.new_board

    def test(self):
        """В эту функцию пихать все для тестов"""
        self.board[4][4] = [Item("moris", self)]
        self.rules["moris"].add_rule("you")

        self.board[6][5] = [Item("box", self)]
        self.board[4][5] = [Item("box", self)]
        self.board[5][5] = [Item("box", self)]
        self.rules["box"].set_colide_type(50)

        self.board[5][8] = [Item("wall", self)]
        self.rules["wall"].set_colide_type(100)
        print(self.rules)


class Item:
    def __init__(self, name, board: MainBoard):
        self.name = name
        self.board = board
        if self.name not in self.board.rules.keys():
            self.rule = Rule(name)
            self.board.rules[name] = self.rule
        else:
            self.rule = self.board.rules[name]

    def try_step(self, old, new):
        x = new[0]
        y = new[1]

        x1 = old[0]
        y1 = old[1]

        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            print("tut norm")
            items_new = sorted(
                self.board.board[y][x], key=lambda f: f.rule.colide_type, reverse=True
            )
            for item in items_new:
                if item.rule.colide_type == 100:
                    return False
                elif item.rule.colide_type >= 50:
                    if not item.try_step(new, (2 * x - x1, 2 * y - y1)):
                        return False
            else:
                self.step(old, new)
                return True
        return False

    def step(self, old, new):
        print(0)
        # print(self.board.new_board[new[1]][new[0]])
        # print(self.board.new_board[old[1]][old[0]])
        self.board.new_board[new[1]][new[0]].append(self)
        self.board.new_board[old[1]][old[0]].remove(self)
        # print(self.board.new_board)

    def render(self, surface, rect):
        pygame.draw.rect(surface, (255, 0, 0), rect)
        text = pygame.font.Font(None, self.board.cell_size // 2).render(
            self.name, False, (0, 0, 0)
        )
        surface.blit(text, rect[:2])
        self.board.rules

    def __getitem__(self, key):
        return key in self.rule.rules

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
