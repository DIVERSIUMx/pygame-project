# На счет имени пока назвал так, потом поменяем FIXME
import pygame
from sprites import ItemSprite, load_image, item_sprites, end_screen_sprites, item_sprites


class MainBoard:
    history_items: list[tuple[list, list]] = []  # история изменений

    check_poses: list[tuple[int, int]] = []  # для проверки измененных позиций
    move_sprites: list = []  # для обозначения перемещенных спрайтов
    intereaction: list = []  # для проверки взаимодействия с обектами правил
    sprites: dict[tuple[str, int, int], ItemSprite] = dict()

    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.top = cell_size // 2
        self.left = cell_size // 2

        self.board = [[list()] * width for _ in range(height)]

    # получение размеров экрана для корректного отображения доски
    def get_screen_size(self):
        return self.width * self.cell_size + (
            2 * self.left
        ), self.height * self.cell_size + (2 * self.top)

    def render(self, surface):  # ренрер самой доски
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                rect = (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(surface, (40, 40, 50), rect, 3)
                # if cell is not None:
                #     for item in cell:
                #         item.render(surface, rect)

    def you_go(self, event_key):  # Определение клавиши выбор направления движения персонажей
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

        return self.move(you_go_delta)

    def undo(self):  # Отмена хода
        if len(self.history_items) != 0:
            from Rules_and_blocks import ActiveBlocks, search_for_rules
            self.intereaction = []
            for deleted in self.history_items[-1][0]:
                self.board[deleted[2]][deleted[1]].append(deleted[0])
                if isinstance(deleted[0], ActiveBlocks):
                    self.intereaction.append(
                        (deleted[0], (deleted[1], deleted[2])))
            for added in self.history_items[-1][1]:
                self.board[added[2]][added[1]].remove(added[0])

            if self.intereaction:
                search_for_rules(self.intereaction, self.board)
            self.history_items.pop(-1)
            for sprite in item_sprites:
                sprite.kill()
            self.generate_sprites()

    def clear(self):  # Отчистка доски для перехода между уровнями
        self.board = [[list()] * self.width for _ in range(self.height)]
        self.history_items = []
        self.sprites = {}
        for sprite in item_sprites:
            sprite.kill()
        for sprite in end_screen_sprites:
            sprite.kill()

    def move(self, you_go_delta):  # Функция обработки самого хода
        self.history_items.append(([], []))
        self.move_sprites = []
        self.check_poses = []
        from Rules_and_blocks import search_for_rules

        self.intereaction = list()
        self.new_board = [[[c for c in i] for i in r] for r in self.board]
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                for item in cell:
                    if item.you:
                        item.try_step(
                            (x, y), (x + you_go_delta[0], y + you_go_delta[1])
                        )
        cur_sp = self.sprites.copy()
        for data in self.move_sprites:
            self.sprites[data[0]] = cur_sp[data[1]]
            self.sprites[data[0]].move(data[0][1:])
            if data[1] in self.sprites and data[1] not in list(map(lambda f: f[0], self.move_sprites)):
                self.sprites.pop(data[1])

        if len(self.check_poses) == 0:
            self.history_items.pop(-1)
        else:
            # Проверка измененных клеток и привидение их согласно правилам
            for i, (x, y) in enumerate(self.check_poses):
                exists = set()
                rm_indexes = []
                you_here = False
                win_here = False
                death_here = False
                for item in self.new_board[y][x]:
                    if item not in exists:
                        exists.add(item)
                    else:
                        self.history_items[-1][0].append((item, x, y))
                        rm_indexes.append(i - len(rm_indexes))
                        continue
                    if item.sink and (len(self.new_board[y][x]) > 1):
                        for item in self.new_board[y][x]:
                            if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                                self.history_items[-1][1].remove((item, x, y))
                            else:
                                self.history_items[-1][0].append((item, x, y))
                            item.die(x * self.cell_size + self.left,
                                     y * self.cell_size + self.top)
                        self.new_board[y][x] = []
                        break
                    elif item.weak and len(self.new_board[y][x]) > 1:
                        if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                            self.history_items[-1][1].remove((item, x, y))
                        else:
                            self.history_items[-1][0].append((item, x, y))
                        item.die(x * self.cell_size + self.left,
                                 y * self.cell_size + self.top)
                        rm_indexes.append(i - len(rm_indexes))
                    else:
                        you_here = you_here or item.you
                        win_here = win_here or item.win
                        death_here = death_here or item.death
                else:
                    for i in rm_indexes:
                        self.new_board[y][x].pop(i)
                    if you_here and death_here:
                        for i, item in enumerate(self.new_board[y][x]):
                            if item.you:
                                if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                                    self.history_items[-1][1].remove(
                                        (item, x, y))
                                else:
                                    self.history_items[-1][0].append(
                                        (item, x, y))
                                item.die(x * self.cell_size + self.left,
                                         y * self.cell_size + self.top)
                                self.new_board[y][x].pop(i)
                    elif you_here and win_here:
                        return True

        self.board = self.new_board
        if self.intereaction:
            search_for_rules(self.intereaction, self.board)

        for sprite in item_sprites.sprites():
            if sprite not in self.sprites.values() and not sprite.die_soon:
                sprite.kill()

        if self.intereaction:
            if self.total_check():
                return True

    def total_check(self):  # Полная проверка поля после изменения правил
        for x in range(self.width):
            for y in range(self.height):
                exists = set()
                rm_indexes = []
                you_here = False
                win_here = False
                death_here = False
                for i, item in enumerate(self.board[y][x]):
                    if item not in exists:
                        exists.add(item)
                    else:
                        self.history_items[-1][0].append((item, x, y))
                        rm_indexes.append(i - len(rm_indexes))
                        continue
                    if item.sink and (len(self.board[y][x]) > 1):
                        for item in self.board[y][x]:
                            if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                                self.history_items[-1][1].remove((item, x, y))
                            else:
                                self.history_items[-1][0].append((item, x, y))
                            item.die(x * self.cell_size + self.left,
                                     y * self.cell_size + self.top)
                        self.board[y][x] = []
                        break
                    elif item.weak and len(self.board[y][x]) > 1:
                        if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                            self.history_items[-1][1].remove((item, x, y))
                        else:
                            self.history_items[-1][0].append((item, x, y))
                        item.die(x * self.cell_size + self.left,
                                 y * self.cell_size + self.top)
                        rm_indexes.append(i - len(rm_indexes))
                    else:
                        you_here = you_here or item.you
                        win_here = win_here or item.win
                        death_here = death_here or item.death
                else:
                    for i in rm_indexes:
                        self.board[y][x].pop(i)
                    if you_here and death_here:
                        for i, item in enumerate(self.board[y][x]):
                            if item.you:
                                if item in list(map(lambda f: f[1], self.history_items[-1][1])):
                                    self.history_items[-1][1].remove(
                                        (item, x, y))
                                else:
                                    self.history_items[-1][0].append(
                                        (item, x, y))
                                item.die(x * self.cell_size + self.left,
                                         y * self.cell_size + self.top)
                                self.board[y][x].pop(i)
                    elif you_here and win_here:
                        return True

    def generate_sprites(self):  # Генерация спрайтов согласно положению объектов на доске
        self.sprites = {}
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                for item in cell:
                    sprite = item.sprite.copy()
                    sprite.rect.x = x * self.cell_size + self.left
                    sprite.rect.y = y * self.cell_size + self.top
                    self.sprites[(sprite.filename, sprite.rect.x,
                                  sprite.rect.y)] = sprite


class Item(object):
    color: tuple[int, int, int] = (255, 255, 255)
    name: str

    sprite = ItemSprite("ohno", load_image("ohno.png"))

    def __init__(self, board: MainBoard):
        self.board = board

    def die(self, x, y):  # Смерть предмета, удаление спрайта
        self.board.sprites[self.sprite.filename, x, y].die()
        self.board.sprites.pop((self.sprite.filename, x, y))

    # V3, проверка, может ли предмет передвинуться учитывая правила stop и push
    def try_step(self, old, new):
        x = new[0]
        y = new[1]

        x1 = old[0]
        y1 = old[1]

        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            if len(self.board.board[y][x]) == 0:
                self.step(old, new)
                return True
            items_new = sorted(
                self.board.board[y][x],
                key=lambda f: f.get_colide_type(),
                reverse=True,
            )

            for item in items_new:
                if item.stop and not item.push:
                    return False
                elif item.push:
                    item.try_step(
                        new, (2 * x - x1, 2 * y - y1))
                    continue
            self.step(old, new)
            return True

    def step(self, old, new):  # Перемешение объекта
        self.board.history_items[-1][0].append((self, *old))
        self.board.history_items[-1][1].append((self, *new))
        self.board.check_poses.append(new)
        self.board.move_sprites.append(((self.sprite.filename, new[0] * 80 + self.board.left, new[1] * 80 + self.board.top), (
            self.sprite.filename, old[0] * 80 + self.board.left, old[1] * 80 + self.board.top)))
        from Rules_and_blocks import ActiveBlocks

        if issubclass(self.__class__, ActiveBlocks):
            self.board.intereaction.append((self, new))
        """print(0)"""
        if self in self.board.new_board[old[1]][old[0]]:
            self.board.new_board[new[1]][new[0]].append(self)
            self.board.new_board[old[1]][old[0]].remove(self)

    def render(self, surface, rect):  # Отладочный рендер обекта
        pygame.draw.rect(surface, self.color, rect)
        text = pygame.font.Font(None, self.board.cell_size // 2).render(
            self.name, True, (0, 0, 0)
        )
        surface.blit(text, rect[:2])
