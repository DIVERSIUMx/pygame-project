#!/bin/python3
import pygame
from tric import MainBoard
import items
import Rules_and_blocks

fps = 60


def test(self: MainBoard):
    """В эту функцию пихать все для тестов"""
    self.board[4][4] = [items.Moris(self)]
    self.rules[items.Moris].you = True
    self.rules[items.Moris].weak = False

    self.board[6][5] = [items.Box(self)]
    self.board[4][5] = [items.Box(self)]
    self.board[5][5] = [items.Box(self)]
    self.rules[items.Box].set_colide_type(90)
    self.rules[items.Box].weak = True

    self.board[5][8] = [items.Wall(self)]
    self.rules[items.Wall].set_colide_type(100)
    self.board[1][1] = [Rules_and_blocks.ActiveBlocksObject('wall', self)]
    self.board[1][2] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[1][3] = [Rules_and_blocks.ActiveBlocksAction('push', self)]
    self.board[2][8] = [Rules_and_blocks.ActiveBlocksObject('box', self)]
    self.board[2][9] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[3][10] = [Rules_and_blocks.ActiveBlocksAction('silk', self)]
    self.board[4][8] = [Rules_and_blocks.ActiveBlocksAction('stop', self)]
    self.board[5][10] = [Rules_and_blocks.ActiveBlocksAction('stop', self)]
    self.rules[Rules_and_blocks.ActiveBlocksObject].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksObject].push = True
    self.rules[Rules_and_blocks.ActiveBlocksIS].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksIS].push = True
    self.rules[Rules_and_blocks.ActiveBlocksAction].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksAction].push = True
    self.board[5][10] = [items.Water(self)]
    # self.rules[items.Water].silk = True
    self.rules[items.Wall].set_colide_type(100)
    print(issubclass(items.Box(self).__class__, items.MegaItems))
    print(self.board)


if __name__ == "__main__":

    pygame.init()
    board = MainBoard(16, 10, 80)
    test(board)

    screen_size = width, height = board.get_screen_size()
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(items.wall.get_rules(), 'wall', '\n', items.box.get_rules(), 'box', '\n', items.rock.get_rules(), 'rock')
                board.you_go(event.key)

        screen.fill((0, 0, 0))
        board.render(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
