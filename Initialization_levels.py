import sqlite3
from items import test_board, board
import Rules_and_blocks
import items
from ast import literal_eval
from items import MegaItems, wall, rock, box, moris, board, flag, skull, water


def start_level(name: str):  # Открытие уровня из бд
    con = sqlite3.connect('game.sqlite')
    cur = con.cursor()
    blocks = cur.execute(
        f"""SELECT blocks FROM levels
                    WHERE name = ?""", (name,)
    ).fetchall()[0]
    start_rules = cur.execute(
        f"""SELECT start_rules FROM levels
                        WHERE name = ?""", (name,)
    ).fetchall()[0]
    # print(start_rules[0], 'start rules')
    blocks = literal_eval(blocks[0])
    start_rules = literal_eval(start_rules[0])
    for el in blocks:
        x, y = el[1]
        if el[2]:
            board.board[y][x] = [eval(el[0])]
        else:
            board.board[y][x] = [globals()[f'{el[0]}']]
    for el in start_rules:  # Создание стартовых правил
        # print(el[3][3])
        Rules_and_blocks.new_rule(
            first_cord=el[0], is_cord=el[1], finish_cord=el[2], first_name=el[3][0], finish_name=el[3][2],
            object_object=el[3][3]
        )

    # board.rules[items.Moris].you = True


# blocks = [[object, [x, y], False / True (active blocks - True)], ...]
# if object is object (moris, wall...) - items.wall / items.moris //
# if object is text (rules_blocks) - class(name) (Rules_and_blocks.ActiveBlocksIS(name, test_board.board))


def new_level(name: str, blocks: list):  # Создание нового уровня в бд через код
    star_rules = list()
    list_is = list()
    for el in blocks:
        x, y = el[1]
        test_board.board[y][x] = el[0]
        # print(
        #    issubclass(eval(el[0]).__class__, Rules_and_blocks.ActiveBlocksIS), eval(
        #        el[0]
        #    ).__class__, 'log kit'
        # )
        if issubclass(eval(el[0]).__class__, Rules_and_blocks.ActiveBlocksIS):
            list_is.append((x, y))
    # print(test_board.board, 'test board')
    for el in list_is:
        # print(el, 'log el')
        cord = x, y = el
        if 1 <= x < 15:  # проверка новых правил по x
            if test_board.board[y][x - 1] and test_board.board[y][x + 1]:
                # print(
                #    issubclass(
                #        test_board.board[y][x - 1].__class__, Rules_and_blocks.ActiveBlocksObject
                #    ),
                #    issubclass(
                #        test_board.board[y][x +
                #                            1].__class__, Rules_and_blocks.ActiveBlocksAction
                #    )
                # )
                try:
                    if issubclass(
                            eval(
                                test_board.board[y][x - 1]
                            ).__class__, Rules_and_blocks.ActiveBlocksObject
                    ) and issubclass(
                        eval(
                            test_board.board[y][x + 1]
                        ).__class__, Rules_and_blocks.ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило
                        # print(1)
                        first_name = eval(test_board.board[y][x - 1]).name
                        finish_name = eval(test_board.board[y][x + 1]).name
                        star_rules.append(
                            ((x - 1, y), (x, y), (x + 1, y),
                             (first_name, 'IS', finish_name, False))
                        )
                        # print(Rules_and_blocks.ActiveRules.get_rules())
                    elif issubclass(
                            eval(
                                test_board.board[y][x - 1]
                            ).__class__, Rules_and_blocks.ActiveBlocksObject
                    ) and issubclass(
                        eval(test_board.board[y][x + 1]).__class__,
                        Rules_and_blocks.ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        first_name = eval(test_board.board[y][x - 1]).name
                        finish_name = eval(test_board.board[y][x + 1]).name
                        star_rules.append(
                            ((x - 1, y), (x, y), (x + 1, y),
                             (first_name, 'IS', finish_name, True))
                        )
                except NameError as e:
                    print(e)
        if 1 <= y < 9:  # проверка новых правил по y

            if test_board.board[y - 1][x] and test_board.board[y + 1][x]:
                try:
                    if issubclass(
                            eval(
                                test_board.board[y - 1][x]
                            ).__class__, Rules_and_blocks.ActiveBlocksObject
                    ) and issubclass(
                        eval(
                            test_board.board[y + 1][x]
                        ).__class__, Rules_and_blocks.ActiveBlocksAction
                    ):  # проверка, что соседнии блоки составляют правило

                        first_name = eval(test_board.board[y - 1][x]).name
                        finish_name = eval(test_board.board[y + 1][x]).name
                        star_rules.append(
                            ((x, y - 1), (x, y), (x, y + 1),
                             (first_name, 'IS', finish_name, False))
                        )
                    elif issubclass(
                            eval(
                                test_board.board[y - 1][x]
                            ).__class__, Rules_and_blocks.ActiveBlocksObject
                    ) and issubclass(
                        eval(test_board.board[y + 1][x]).__class__,
                        Rules_and_blocks.ActiveBlocksObject
                    ):  # проверка, что соседнии блоки составляют правило
                        finish_name = eval(test_board.board[y - 1][x]).name
                        first_name = eval(test_board.board[y + 1][x]).name
                        star_rules.append(
                            ((x, y - 1), (x, y), (x, y + 1),
                             (first_name, 'IS', finish_name, True))
                        )
                except NameError as e:
                    print(e)
    con = sqlite3.connect('game.sqlite')
    cur = con.cursor()
    # print(name)
    # print(blocks)
    # print(star_rules)
    cur.execute(
        f"""INSERT INTO levels(name, blocks, start_rules) VALUES(?, ?, ?)""", (name, str(
            blocks
        ), str(star_rules))
    )
    con.commit()


def add_new_level():  # Создание новго уровня
    # new_level(
    #     'level-1', [['flag', [3, 5], False], ['moris', [1, 1], False], ['wall', [3, 7], False],
    #                 ['Rules_and_blocks.ActiveBlocksObject("moris", board)', [5, 1], True],
    #                 ['Rules_and_blocks.ActiveBlocksIS(board)', [6, 1], True],
    #                 ['Rules_and_blocks.ActiveBlocksAction("you", board)', [7, 1], True],
    #
    #                 ['Rules_and_blocks.ActiveBlocksObject("flag", board)', [5, 4], True],
    #                 ['Rules_and_blocks.ActiveBlocksIS(board)', [6, 4], True],
    #                 ['Rules_and_blocks.ActiveBlocksAction("win", board)', [7, 4], True]]
    #
    # )

    new_level(
        'level-5', [
            ['water', [9, 4], False], ['water', [10, 4], False], [
                'water', [11, 4], False],
            ['water', [9, 6], False], ['water', [10, 6], False], [
                'water', [11, 6], False],
            ['water', [9, 5], False], ['flag', [10, 5], False], [
                'water', [11, 5], False],
            ['box', [6, 5], False],
            ['Rules_and_blocks.ActiveBlocksObject("moris", board)', [
                0, 2], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [0, 3], True],
            ['Rules_and_blocks.ActiveBlocksAction("weak", board)', [
                0, 4], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [1, 2], True],
            ['Rules_and_blocks.ActiveBlocksAction("you", board)', [
                2, 2], True],
            ['Rules_and_blocks.ActiveBlocksObject("box", board)', [
                0, 7], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [0, 8], True],
            ['Rules_and_blocks.ActiveBlocksAction("push", board)', [
                1, 9], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [1, 8], True],
            ['Rules_and_blocks.ActiveBlocksAction("sink", board)', [
                4, 7], True],
            ['Rules_and_blocks.ActiveBlocksObject("water", board)', [
                9, 7], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [10, 7], True],
            ['Rules_and_blocks.ActiveBlocksAction("stop", board)', [
                11, 7], True],
            ['Rules_and_blocks.ActiveBlocksObject("flag", board)', [
                13, 0], True],
            ['Rules_and_blocks.ActiveBlocksIS(board)', [14, 0], True],
            ['Rules_and_blocks.ActiveBlocksAction("win", board)', [
                15, 0], True],
            ['moris', [6, 5], False], ['box', [6, 7], False]



        ])


if __name__ == "__main__":
    add_new_level()
