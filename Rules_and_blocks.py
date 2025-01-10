from tric import Item
from items import MegaItems, wall, rock, box, board

colors = {
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
    'weak': 'grey'
}


class ActiveRulesClass:
    def __init__(self):
        self.rules = list()
        # [(start cord, is_cord, finish_cord, [name_start, is, name_finish])]

    def append(self, new_rule):
        self.rules.append(new_rule)

    def __delitem__(self, key):
        del self.rules[self.rules.index(key)]

    def get_rules(self):
        return self.rules


ActiveRules = ActiveRulesClass()


class ActiveBlocks(MegaItems):
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
        self.stop = False
        self.death = False
        self.push = True
        self.sink = False
        self.win = False
        self.weak = False

    def __str__(self):
        return self.name


class ActiveBlocksIS(ActiveBlocks):
    def __init__(self, board):
        super().__init__('white', 'IS', board)
        self.__class__.__name__ = 'IS'


class ActiveBlocksObject(ActiveBlocks):
    def __init__(self, name, board):
        super().__init__(colors[name], name, board, activity='OBJECT')
        self.__class__.__name__ = 'OBJECT'


class ActiveBlocksAction(ActiveBlocks):
    def __init__(self, name, board):
        super().__init__(colors[name], name, board, activity='OBJECT')
        self.__class__.__name__ = 'ACTION'


def new_rule(
        first_cord: (int, int), first_name: str, is_cord: (int, int), finish_cord: (int, int), finish_name,
        is_name='IS', object_object=False
):
    if object_object:  # Изменение объектов (пример: wall is box)
        for x in range(board.width):
            for y in range(board.height):
                if board.board[y][x]:
                    if board.board[y][x][0].name == first_name.capitalize():
                        print(board.board[y][x][0].name)
                        print(111111111111)
                        board.board[y][x][0] = globals()[f"{finish_name}"]
                        print(board.board[y][x], 'log 3')

    else:
        print(first_name, finish_name)
        exec(compile(f"globals()['{first_name}'].set_{finish_name}(True)", str(), 'exec'))
        print(globals()[first_name].get_rules())
    ActiveRules.append((first_cord, is_cord, finish_cord, (first_name, is_name, finish_name, object_object)))


new_rule(first_cord=(1, 1), first_name='wall', is_cord=(2, 1), finish_cord=(3, 1), finish_name='push')
print(ActiveRules.get_rules(), 1)


# Функция проверяет на существование старых правил
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
        elif board[element[0][1]][element[0][0]][0].name != element[-1][0] \
                or board[element[1][1]][element[1][0]][0].name != element[-1][1] \
                or board[element[2][1]][element[2][0]][0].name != element[-1][2]:
            print(
                board[element[0][1]][element[0][0]][0].name, element[-1][0], '\n',
                board[element[1][1]][element[1][0]][0].name, element[-1][1]
            )
            if element[-1][-1] is True:
                del ActiveRules[element]
                continue
            del ActiveRules[element]
            exec(compile(f"globals()['{element[3][0]}'].set_{element[3][2]}(False)", str(), 'exec'))
        # изменение правил элемента в процессе
    print(ActiveRules.get_rules(), 2)


# Функция получает список всех элементов (аткивных блоков) сдвинутых за ход
def search_for_rules(intereaction, board):
    checking_for_rule_existence(board)

    for element in intereaction:

        if isinstance(element[0], ActiveBlocksAction):
            cord = x, y = element[1]
            print(board[y][x - 1], board[y][x - 2])
            if x >= 2:  # проверка новых правил по x
                if board[y][x - 1] and board[y][x - 2]:
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x - 2][0].__class__,
                            ActiveBlocksObject
                    ):
                        first_name = board[y][x - 2][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x - 2, y), first_name=first_name, is_cord=(x - 1, y), finish_cord=cord,
                            finish_name=finish_name
                        )
            if y >= 2:  # проверка новых правил по y
                if board[y - 1][x] and board[y - 2][x]:
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y - 2][x][0].__class__,
                            ActiveBlocksObject
                    ):
                        first_name = board[y - 2][x][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x, y - 2), first_name=first_name, is_cord=(x, y - 1), finish_cord=cord,
                            finish_name=finish_name
                        )

        elif isinstance(element[0], ActiveBlocksIS):
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
                    ):
                        print(1)
                        first_name = board[y][x - 1][0].name
                        finish_name = board[y][x + 1][0].name
                        new_rule(
                            first_cord=(x - 1, y), first_name=first_name, is_cord=cord, finish_cord=(x + 1, y),
                            finish_name=finish_name
                        )
                        print(ActiveRules.get_rules())
                    elif issubclass(board[y][x - 1][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y][x + 1][0].__class__,
                            ActiveBlocksObject
                    ):
                        first_name = board[y][x - 1][0].name
                        finish_name = board[y][x + 1][0].name
                        new_rule(
                            first_cord=(x - 1, y), first_name=first_name, is_cord=cord, finish_cord=(x + 1, y),
                            finish_name=finish_name, object_object=True
                        )
            if 1 <= y < 9:  # проверка новых правил по y
                if board[y - 1][x] and board[y + 1][x]:
                    print(board[y - 1][x], board[y + 1][x])
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y + 1][x][0].__class__, ActiveBlocksAction
                    ):
                        first_name = board[y - 1][x][0].name
                        finish_name = board[y + 1][x][0].name
                        new_rule(
                            first_cord=(x, y - 1), first_name=first_name, is_cord=cord, finish_cord=(x, y + 1),
                            finish_name=finish_name
                        )
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksObject) and issubclass(
                            board[y + 1][x][0].__class__,
                            ActiveBlocksObject
                    ):
                        finish_name = board[y - 1][x][0].name
                        first_name = board[y + 1][x][0].name
                        new_rule(
                            first_cord=(x, y - 1), first_name=first_name, is_cord=cord, finish_cord=(x, y + 1),
                            finish_name=finish_name, object_object=True
                        )
        elif isinstance(element[0], ActiveBlocksObject):
            cord = x, y = element[1]
            print('log Object')
            if x >= 2:  # проверка новых правил по x (блок объект находится справо)
                if board[y][x - 1] and board[y][x - 2]:
                    if issubclass(board[y][x - 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x - 2][0].__class__,
                            ActiveBlocksObject
                    ):
                        first_name = board[y][x - 2][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x - 2, y), first_name=first_name, is_cord=(x - 1, y), finish_cord=cord,
                            finish_name=finish_name, object_object=True
                        )
            if y >= 2:  # проверка новых правил по y (блок объект находится снизу)
                if board[y - 1][x] and board[y - 2][x]:
                    if issubclass(board[y - 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y - 2][x][0].__class__,
                            ActiveBlocksObject
                    ):
                        first_name = board[y - 2][x][0].name
                        finish_name = board[y][x][0].name
                        new_rule(
                            first_cord=(x, y - 2), first_name=first_name, is_cord=(x, y - 1), finish_cord=cord,
                            finish_name=finish_name, object_object=True
                        )

            if x < 13:  # проверка новых правил по x (блок объект находится слево)
                if board[y][x + 1] and board[y][x + 2]:
                    if issubclass(board[y][x + 1][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y][x + 2][0].__class__,
                            ActiveBlocksAction
                    ):
                        finish_name = board[y][x + 2][0].name
                        first_name = board[y][x][0].name
                        new_rule(
                            first_cord=cord, first_name=first_name, is_cord=(x + 1, y), finish_cord=(x + 2, y),
                            finish_name=finish_name
                        )
            if y < 7:  # проверка новых правил по y (блок объект находится сверху)
                if board[y + 1][x] and board[y + 2][x]:
                    if issubclass(board[y + 1][x][0].__class__, ActiveBlocksIS) and issubclass(
                            board[y + 2][x][0].__class__,
                            ActiveBlocksAction
                    ):
                        finish_name = board[y + 2][x][0].name
                        first_name = board[y][x][0].name
                        new_rule(
                            first_cord=cord, first_name=first_name, is_cord=(x, y + 1), finish_cord=(x, y + 2),
                            finish_name=finish_name
                        )
    checking_for_rule_existence(board)
    print(ActiveRules.get_rules())


'''item = globals()['wall']
item.set_deth(True)'''

'''x = compile("globals()['wall'].set_deth(True)", str(), 'eval')
exec(x)'''

'''WallActObj = ActiveBlocksObject('wall')
a = globals()[WallActObj.name]
a.set_deth(True)'''
