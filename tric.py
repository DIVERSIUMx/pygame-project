# На счет имени пока назвал так, потом поменяем FIXME
import pygame


class Rule:
    def __init__(self):
        self.rules = []
        self.colide_type = 0
        self.weak = False
        self.sink = False
        self.you = False

    def add_rule(self, rule_name: str):
        self.rules.append(rule_name)

    def set_colide_type(self, new):
        if self.colide_type < 50:
            self.colide_type = max(self.colide_type, new)
        elif new > 50:
            self.colide_type = min(self.colide_type, new)


class MainBoard:
    intereaction: list = []  # твой список  WARN:
    rules: dict[type, Rule] = dict()

    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.top = cell_size // 2
        self.left = cell_size // 2

        self.board = [[list()] * width for _ in range(height)]
        """print(self.board)"""

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
        from Rules_and_blocks import search_for_rules

        """Функция для обработки хода"""
        self.intereaction = list()
        self.new_board = [[[c for c in i] for i in r] for r in self.board]
        """print(len(self.new_board[0]), self.width)
        print(len(self.new_board), self.height)"""
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                for item in cell:
                    """print(len(self.new_board[y][x]))"""
                    if item.rule.you:
                        """print("help")"""
                        colide_res = item.try_step(
                            (x, y), (x + you_go_delta[0], y + you_go_delta[1])
                        )
                        if item.weak and not colide_res:
                            item.step_and_die(
                                (x, y), (x + you_go_delta[0], y + you_go_delta[1])
                            )

        self.board = self.new_board
        if self.intereaction:
            search_for_rules(self.intereaction, self.board)


class Item(object):
    color: tuple[int, int, int] = (255, 255, 255)
    name: str

    def __init__(self, board: MainBoard):
        self.board = board
        if type(self) not in self.board.rules.keys():
            self.rule = Rule()
            self.board.rules[type(self)] = self.rule
        else:
            self.rule = self.board.rules[type(self)]

    def try_step_old(self, old, new):  # Не используется  WARN:
        # Для сохранения психологического здоровья настоятельно не рекомендуется изучать дальнейшее
        # содержимое функции, ВАС ПРЕДУПРЕДИЛИ  WARN:
        x = new[0]
        y = new[1]

        x1 = old[0]
        y1 = old[1]

        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            if len(self.board.board[y][x]) == 0:
                self.step(old, new)
                return True
            elif len(self.board.board[y][x]) > 1:
                items_new = sorted(
                    self.board.board[y][x],
                    key=lambda f: f.rule.colide_type,
                    reverse=True,
                )
                for item in items_new:
                    if item.rule.colide_type == 100:
                        return False
                    elif item.rule.colide_type >= 90:  #
                        colide_res = item.try_step(new, (2 * x - x1, 2 * y - y1))
                        if not colide_res and item.rule.weak:
                            item.step_and_die(new, (2 * x - x1, 2 * y - y1))
                            self.step(old, new)
                            return True
                        elif not colide_res:
                            return False
                        else:
                            self.step(old, new)
                            return True
                    elif self.rule.you and item.rule.colide_type == 20:
                        self.step_and_die(old, new)
                    elif self.rule.you and item.rules.colide_type == 1:
                        self.step_and_win(old, new)
                    elif self.rule.weak and item.rule.colide_type == 0:
                        self.step_and_die(old, new)
                        return True
                else:
                    self.step(old, new)
                    return True
            else:
                item = self.board.board[y][x][0]

                if item.rule.colide_type == 100:
                    return False
                elif item.rule.colide_type >= 90:  #
                    colide_res = item.try_step(new, (2 * x - x1, 2 * y - y1))
                    if not colide_res and item.rule.weak:
                        item.step_and_die(new, (2 * x - x1, 2 * y - y1))
                        self.step(old, new)
                        return True
                    elif not colide_res:
                        return False
                    else:
                        self.step(old, new)
                        return True
                elif item.rule.sink:
                    self.step_and_clear(old, new)
                    return True
                elif item.rule.weak:
                    self.clear_and_step(old, new)
                    return True
                elif self.rule.weak and item.rule.colide_type == 0:
                    self.step_and_die(old, new)
                    return True
                else:
                    self.step(old, new)
                    return True

        return False

    def try_step(self, old, new):
        # Для сохранения психологического здоровья настоятельно не рекомендуется изучать дальнейшее
        # содержимое функции, ВАС ПРЕДУПРЕДИЛИ  WARN:
        x = new[0]
        y = new[1]

        x1 = old[0]
        y1 = old[1]

        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            if len(self.board.board[y][x]) == 0:
                self.step(old, new)
                return True
            elif len(self.board.board[y][x]) > 1:
                items_new = sorted(
                    self.board.board[y][x],
                    key=lambda f: f.get_colide_type(),
                    reverse=True,
                )
                for item in items_new:
                    if item.stop and not item.push:
                        return False
                    elif item.push:
                        colide_res = item.try_step(new, (2 * x - x1, 2 * y - y1))
                        if not colide_res and item.weak:
                            item.step_and_die(new, (2 * x - x1, 2 * y - y1))
                            self.step(old, new)
                            return True
                        elif not colide_res:
                            return False
                        else:
                            self.step(old, new)
                            return True
                    elif self.rule.you and item.death:
                        self.step_and_die(old, new)
                    elif self.rule.you and item.win:
                        self.step_and_win(old, new)
                    elif self.weak:
                        self.step_and_die(old, new)
                        return True
                else:
                    self.step(old, new)
                    return True
            else:
                item = self.board.board[y][x][0]

                if item.stop and not item.push:
                    return False
                elif item.push:
                    colide_res = item.try_step(new, (2 * x - x1, 2 * y - y1))
                    if not colide_res and item.weak:
                        item.step_and_die(new, (2 * x - x1, 2 * y - y1))
                        self.step(old, new)
                        return True
                    elif not colide_res:
                        return False
                    else:
                        self.step(old, new)
                        return True
                elif item.sink:
                    self.step_and_clear(old, new)
                    return True
                elif item.weak:
                    self.clear_and_step(old, new)
                    return True
                elif self.weak:
                    self.step_and_die(old, new)
                    return True
                else:
                    self.step(old, new)
                    return True

        return False

    def step(self, old, new):
        from Rules_and_blocks import ActiveBlocks

        if issubclass(self.__class__, ActiveBlocks):
            self.board.intereaction.append((self, new))
        """print(0)"""
        if self.sink and self.board.new_board[new[1]][new[0]] != []:
            self.board.new_board[new[1]][new[0]] = []
            self.board.new_board[old[1]][old[0]].remove(self)
            return
        self.board.new_board[new[1]][new[0]].append(self)
        self.board.new_board[old[1]][old[0]].remove(self)

    def step_and_die(self, old, new):
        self.board.new_board[old[1]][old[0]].remove(self)

    def step_and_clear(self, old, new):
        self.board.new_board[old[1]][old[0]].remove(self)
        self.board.new_board[new[1]][new[0]] = []

    def clear_and_step(self, old, new):
        self.board.new_board[old[1]][old[0]].remove(self)
        self.board.new_board[new[1]][new[0]] = [self]

    def step_and_win(self, old, new):
        if self.sink and self.board.new_board[new[1]][new[0]] != []:
            self.board.new_board[new[1]][new[0]] = []
            self.board.new_board[old[1]][old[0]].remove(self)
            return
        self.board.new_board[new[1]][new[0]].append(self)
        self.board.new_board[old[1]][old[0]].remove(self)
        print("YOU WIN")

    def render(self, surface, rect):
        pygame.draw.rect(surface, self.color, rect)
        text = pygame.font.Font(None, self.board.cell_size // 2).render(
            self.name, True, (0, 0, 0)
        )
        surface.blit(text, rect[:2])
        # self.board.rules

    def __getitem__(self, key):
        return key in self.rule.rules

    # def __repr__(self):
    #     return self.name
    #
    # def __eq__(self, other):
    #     return self.name == other.name
    #
    # def __hash__(self):
    #     return hash(self.name)
