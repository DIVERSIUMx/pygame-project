import pygame
from tric import Item
from items import MegaItems, wall, rock, box, board, moris, flag, skull
from sprites import ItemSprite, load_image

pygame.init()

colors = {
    # используется для отображения блоков без спрайтов (прямой отрисовкой)
    # 'name': 'color'
    # пример ниже
    'wall': 'white',
    'push': 'yellow',
    'sink': 'red',
    'box': 'grey',
    'rock': 'orange',
    'stop': 'red',
    'death': 'grey',
    'win': 'yellow',
    'weak': 'grey',
    'moris': 'gold',
    'you': 'pink',
    'flag': 'gold'
}


class ActiveRulesClass:  # Класс хранящий в себе все активные правила
    def __init__(self):
        self.rules = list()
        # [(start cord, is_cord, finish_cord, [name_start, is, name_finish])]

    def append(self, new_rule):
        self.rules.append(new_rule)

    def __delitem__(self, key):
        del self.rules[self.rules.index(key)]

    def get_rules(self):
        return self.rules

    def clear(self):
        self.rules = list()


ActiveRules = ActiveRulesClass()


class ActiveBlocks(MegaItems):  # Родительский класс блоков текста (действий)
    def __init__(self, color, name, board, activity='IS'):
        self.colide_type = 90
        self.color = color
        self.name = name
        # activity =
        # 'IS' if it`s a 'IS' block
        # 'OBJECT' if it`s some object active block (wall, box, etc.)
        # 'ACTION' id it`s some action block (push, stop, etc.)
        self.activity = activity
        super().__init__(board)
        # его основные правила со старта
        self.stop = False
        self.death = False
        self.push = True
        self.sink = False
        self.win = False
        self.weak = False

    def __str__(self):
        return self.name


class ActiveBlocksIS(ActiveBlocks):  # Класс - наследник, для блока текста - IS (ЭТО)
    sprite = ItemSprite("is", load_image("is.png"))

    def __init__(self, board):
        super().__init__('white', 'IS', board)
        self.__class__.__name__ = 'IS'


class ActiveBlocksObject(ActiveBlocks):  # Класс - наследник, для блоков текста -  предметов
    def __init__(self, name, board):
        self.sprite = ItemSprite(
            name + "*", load_image("names", f"{name}.png")
        )
        super().__init__(colors[name], name, board, activity='OBJECT')
        self.__class__.__name__ = 'OBJECT'


class ActiveBlocksAction(ActiveBlocks):  # Класс - наследник, для блоков текста -  действиий
    sprite = ItemSprite("ohno", load_image("action.png"))

    def __init__(self, name, board):
        self.sprite = ItemSprite(name, load_image("actions", f"{name}.png"))
        super().__init__(colors[name], name, board, activity='OBJECT')
        self.__class__.__name__ = 'ACTION'


def new_rule(
        first_cord: (int, int), first_name: str, is_cord: (int, int), finish_cord: (int, int), finish_name,
        is_name='IS', object_object=False
):  # создание нового праивла
    flag_moris = True  # НЕ Действует ли это праивило на мориса
    if object_object:  # Действует только при изменении блоков, прмиер: box is wall
        for y, row in enumerate(board.board):
            for x, cell in enumerate(row):
                for i in range(len(cell)):
                    if cell[i].name == first_name.capitalize():
                        board.history_items[-1][0].append((cell[i], x, y))
                        cell[i].die(
                            x * board.cell_size + board.left,
                            y * board.cell_size + board.top
                        )  # Добавляет создания правила в историю ctrl+z
                        cell[i] = globals()[f"{finish_name}"]  # Применяет новое правило на элемент класса в items
                        sprite = cell[i].sprite.copy()
                        sprite.rect.x = x * board.cell_size + board.left
                        sprite.rect.y = y * board.cell_size + board.top
                        board.sprites[cell[i].sprite.filename, x * board.cell_size +
                                                               board.left, y * board.cell_size + board.top] = sprite
                        board.history_items[-1][1].append((cell[i], x, y))
    # elif first_name == 'moris':
    #     flag_moris = False
    #     x, y = finish_cord
    #     if board.board[y][x]:
    #         if issubclass(board.board[y][x][0].__class__, ActiveBlocksAction):
    #             for x in range(board.width):
    #                 for y in range(board.height):
    #                     if board.board[y][x]:
    #                         if board.board[y][x][0].name == finish_name.capitalize():
    #                             print(board.board[y][x][0].name)
    #                             print(111111111111)
    #                             board.board[y][x][0] = globals()[f"{'moris'}"]
    #                             print(board.board[y][x], 'log 3')
    else:  # Применяется во всех иных случаях
        print(first_name, finish_name)
        exec(
            compile(f"globals()['{first_name}'].set_{finish_name}(True)", str(), 'exec')
        )  # Обращаемся к элементу класса в items и даем ему новые параметры
        print(globals()[first_name].get_rules())
    if flag_moris:  # Если праивло не на мориса - добавление в список
        ActiveRules.append(
            (first_cord, is_cord, finish_cord,
             (first_name, is_name, finish_name, object_object))
        )


'''new_rule(first_cord=(2, 8), first_name='moris', is_cord=(2, 9), finish_cord=(2, 10), finish_name='you')
print(ActiveRules.get_rules(), 1)'''


# Функция проверяет на существование старых правил
# Выполняется только в случаи взаимодействия с блоком текста
def checking_for_rule_existence(board):
    rules = ActiveRules.get_rules()
    for element in rules:
        '''print(element)
        print(board[element[0][1]][element[0][0]][0].name, board[element[1][1]][element[1][0]], board[element[2][1]][
            element[2][0]])'''
        '''print(board[element[0][0]][element[0][1]])'''

        if rules.count(element) >= 2:
            del ActiveRules[element]
        elif not (board[element[0][1]][element[0][0]] and board[element[1][1]][element[1][0]] and board[element[2][1]][
            element[2][0]]):
            del ActiveRules[element]
            if element[-1][-1] is not True:
                exec(
                    compile(
                        f"globals()['{element[3][0]}'].set_{element[3][2]}(False)", str(), 'exec'
                    )
                )  # отменяет применные праивла на элемент класса в items
        elif board[element[0][1]][element[0][0]][0].name != element[-1][0] \
                or board[element[1][1]][element[1][0]][0].name != element[-1][1] \
                or board[element[2][1]][element[2][0]][0].name != element[-1][2]:
            # Если в правиле были сдвинуты соседние блоки
            print(
                board[element[0][1]][element[0][0]
                ][0].name, element[-1][0], '\n',
                board[element[1][1]][element[1][0]][0].name, element[-1][1]
            )
            if element[-1][-1] is True:  # Очиста праивла obj is obj (ограничение для ошибок)
                del ActiveRules[element]
                continue
            del ActiveRules[element]
            exec(
                compile(
                    f"globals()['{element[3][0]}'].set_{element[3][2]}(False)", str(), 'exec'
                )
            )# отменяет применные праивла на элемент класса в items
        # изменение правил элемента в процессе
    print(ActiveRules.get_rules(), 2)


# Функция получает список всех элементов (аткивных блоков) сдвинутых за ход
def search_for_rules(intereaction, board):
    checking_for_rule_existence(board)  # Проверяем, что все правила действительны

    for element in intereaction:
        print(element)
        if isinstance(element[0], ActiveBlocksAction):  # Проверяет на то, что блок текста являтся дейсвтием
            cord = x, y = element[1]
            if x >= 2:  # проверка новых правил по x
                if board[y][x - 1] and board[y][x - 2]:
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x - 2][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y][x - 2][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x - 2, y), first_name=first_name, is_cord=(x - 1, y), finish_cord=cord,
                            finish_name=finish_name
                        )  # Создание нового правила
            if y >= 2:  # проверка новых правил по y
                if board[y - 1][x] and board[y - 2][x]:
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y - 2][x][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y - 2][x][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x, y - 2), first_name=first_name, is_cord=(x, y - 1), finish_cord=cord,
                            finish_name=finish_name
                        )  # Создание нового правила

        elif isinstance(element[0], ActiveBlocksIS):  # Проверяет на то, что блок текста являтся IS (это)
            cord = x, y = element[1]
            if 1 <= x < 15:  # проверка новых правил по x

                if board[y][x - 1] and board[y][x + 1]:
                    print(
                        issubclass(board[y][x - 1][0].__class__, ActiveBlocksObject), issubclass(
                            board[y][x + 1][0].__class__, ActiveBlocksAction
                        )
                    )
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y][x + 1][0].__class__, ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило
                        print(1)
                        first_name = board[y][x - 1][0].name
                        finish_name = board[y][x + 1][0].name
                        new_rule(
                            first_cord=(x - 1, y), first_name=first_name, is_cord=cord, finish_cord=(x + 1, y),
                            finish_name=finish_name
                        )  # Создание нового правила
                        print(ActiveRules.get_rules())
                    elif issubclass(board[y][x - 1][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y][x + 1][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y][x - 1][0].name
                        finish_name = board[y][x + 1][0].name
                        new_rule(
                            first_cord=(x - 1, y), first_name=first_name, is_cord=cord, finish_cord=(x + 1, y),
                            finish_name=finish_name, object_object=True
                        )  # Создание нового правила
            if 1 <= y < 9:  # проверка новых правил по y
                if board[y - 1][x] and board[y + 1][x]:
                    print(board[y - 1][x], board[y + 1][x])
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y + 1][x][0].__class__, ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y - 1][x][0].name
                        finish_name = board[y + 1][x][0].name
                        new_rule(
                            first_cord=(x, y - 1), first_name=first_name, is_cord=cord, finish_cord=(x, y + 1),
                            finish_name=finish_name
                        )  # Создание нового правила
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y + 1][x][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        finish_name = board[y - 1][x][0].name
                        first_name = board[y + 1][x][0].name
                        new_rule(
                            first_cord=(x, y - 1), first_name=first_name, is_cord=cord, finish_cord=(x, y + 1),
                            finish_name=finish_name, object_object=True
                        )  # Создание нового правила
        elif isinstance(element[0], ActiveBlocksObject):  # Проверяет на то, что блок текста являтся объектом
            cord = x, y = element[1]
            print('log Object')
            # проверка новых правил по x (блок объект находится справо)
            if x >= 2:    # проверка новых правил по x
                if board[y][x - 1] and board[y][x - 2]:
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x - 2][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y][x - 2][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x - 2, y), first_name=first_name, is_cord=(x - 1, y), finish_cord=cord,
                            finish_name=finish_name, object_object=True
                        )  # Создание нового правила
            # проверка новых правил по y (блок объект находится снизу)
            if y >= 2:    # проверка новых правил по y
                if board[y - 1][x] and board[y - 2][x]:
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y - 2][x][0].__class__,
                            ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = board[y - 2][x][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x, y - 2), first_name=first_name, is_cord=(x, y - 1), finish_cord=cord,
                            finish_name=finish_name, object_object=True
                        )  # Создание нового правила

            # проверка новых правил по x (блок объект находится слево)
            if x < 13:  # проверка новых правил по y
                if board[y][x + 1] and board[y][x + 2]:
                    if issubclass(board[y][x + 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x + 2][0].__class__,
                            ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило
                        finish_name = board[y][x + 2][0].name
                        first_name = board[y][x][0].name
                        new_rule(
                            first_cord=cord, first_name=first_name, is_cord=(x + 1, y), finish_cord=(x + 2, y),
                            finish_name=finish_name
                        )  # Создание нового правила
            # проверка новых правил по y (блок объект находится сверху)
            if y < 7:  # проверка новых правил по y
                if board[y + 1][x] and board[y + 2][x]:
                    if issubclass(board[y + 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y + 2][x][0].__class__,
                            ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило
                        finish_name = board[y + 2][x][0].name
                        first_name = board[y][x][0].name
                        new_rule(
                            first_cord=cord, first_name=first_name, is_cord=(x, y + 1), finish_cord=(x, y + 2),
                            finish_name=finish_name
                        )  # Создание нового правила
    checking_for_rule_existence(board)
    print(ActiveRules.get_rules())


def get_rules():  # Вывод активных блоков
    print(ActiveRules.get_rules())


def clear_rules():  # Отчищение правил
    ActiveRules.clear()


'''item = globals()['wall']
item.set_deth(True)'''

'''x = compile("globals()['wall'].set_deth(True)", str(), 'eval')
exec(x)'''

'''WallActObj = ActiveBlocksObject('wall')
a = globals()[WallActObj.name]
a.set_deth(True)'''
