import sqlite3
from items import test_board, board
import Rules_and_blocks
import items
from ast import literal_eval
from items import MegaItems, wall, rock, box, board, moris


def start_level(name: str):
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
    print(blocks[0])
    blocks = literal_eval(blocks[0])
    start_rules = literal_eval(start_rules[0])
    for el in blocks:
        x, y = el[1]
        if el[2]:

            board.board[y][x] = [eval(el[0])]
        else:
            board.board[y][x] = [globals()[f'{el[0]}']]
    for el in start_rules:
        Rules_and_blocks.new_rule(el)

    board.rules[items.Moris].you = True


# blocks = [[object, [x, y], False / True (active blocks - True)], ...]
# if object is object (moris, wall...) - items.wall / items.moris //
# if object is text (rules_blocks) - class(name) (Rules_and_blocks.ActiveBlocksIS(name, test_board.board))


def new_level(name: str, blocks: list):
    star_rules = list()
    list_is = list()
    for el in blocks:
        x, y = el[1]
        test_board.board[y][x] = el[0]
        if issubclass(el[0].__class__, Rules_and_blocks.ActiveBlocksIS):
            list_is.append((x, y))
    for el in list_is:
        cord = x, y = el
        if 1 <= x < 15:  # проверка новых правил по x

            if test_board.board[y][x - 1] and test_board.board[y][x + 1]:
                print(
                    issubclass(test_board.board[y][x - 1][0].__class__, Rules_and_blocks.ActiveBlocksObject),
                    issubclass(
                        test_board.board[y][x + 1][0].__class__, Rules_and_blocks.ActiveBlocksAction
                    )
                )
                if issubclass(
                        test_board.board[y][x - 1][0].__class__, Rules_and_blocks.ActiveBlocksObject
                ) and issubclass(
                    test_board.board[y][x + 1][0].__class__, Rules_and_blocks.ActiveBlocksAction
                ):
                    print(1)
                    first_name = test_board.board[y][x - 1][0].name
                    finish_name = test_board.board[y][x + 1][0].name
                    star_rules.append(
                        [(x - 1, y), first_name, cord, (x + 1, y), finish_name, False]
                    )
                    print(Rules_and_blocks.ActiveRules.get_rules())
                elif issubclass(
                        test_board.board[y][x - 1][0].__class__, Rules_and_blocks.ActiveBlocksObject
                ) and issubclass(
                    test_board.board[y][x + 1][0].__class__,
                    Rules_and_blocks.ActiveBlocksObject
                ):
                    first_name = test_board.board[y][x - 1][0].name
                    finish_name = test_board.board[y][x + 1][0].name
                    star_rules.append(
                        [(x - 1, y), first_name, cord, (x + 1, y), finish_name, True]
                    )
        if 1 <= y < 9:  # проверка новых правил по y
            if test_board.board[y - 1][x] and test_board.board[y + 1][x]:
                print(test_board.board[y - 1][x], test_board.board[y + 1][x])
                if issubclass(
                        test_board.board[y - 1][x][0].__class__, Rules_and_blocks.ActiveBlocksObject
                ) and issubclass(
                    test_board.board[y + 1][x][0].__class__, Rules_and_blocks.ActiveBlocksAction
                ):
                    first_name = test_board.board[y - 1][x][0].name
                    finish_name = test_board.board[y + 1][x][0].name
                    star_rules.append(
                        [(x, y - 1), first_name, cord, (x, y + 1), finish_name, False]
                    )
                if issubclass(
                        test_board.board[y - 1][x][0].__class__, Rules_and_blocks.ActiveBlocksObject
                ) and issubclass(
                    test_board.board[y + 1][x][0].__class__,
                    Rules_and_blocks.ActiveBlocksObject
                ):
                    finish_name = test_board.board[y - 1][x][0].name
                    first_name = test_board.board[y + 1][x][0].name
                    star_rules.append(
                        [(x, y - 1), first_name, cord, (x, y + 1), finish_name, True]
                    )
    con = sqlite3.connect('game.sqlite')
    cur = con.cursor()
    print(name)
    print(blocks)
    print(star_rules)
    cur.execute(
        f"""INSERT INTO levels(name, blocks, start_rules) VALUES(?, ?, ?)""", (name, str(blocks), str(star_rules))
    )
    con.commit()


'''new_level(
    'test_second1', [['wall', [3, 5], False], ['moris', [4, 9], False], ['box', [5, 5], False],
                     ['Rules_and_blocks.ActiveBlocksAction("push", board)', [2, 5], True],
                     ['Rules_and_blocks.ActiveBlocksObject("box", board)', [1, 3], True],
                     ['Rules_and_blocks.ActiveBlocksIS(board)', [1, 4], True]]
    )'''
