#!/bin/python3
import pygame
from tric import MainBoard
import items

fps = 60


def test(self: MainBoard):
    """В эту функцию пихать все для тестов"""
    self.board[4][4] = [items.Moris(self)]
    self.rules[items.Moris].add_rule("you")

    self.board[6][5] = [items.Box(self)]
    self.board[4][5] = [items.Box(self)]
    self.board[5][5] = [items.Box(self)]
    self.rules[items.Box].set_colide_type(50)

    self.board[5][8] = [items.Wall(self)]
    self.rules[items.Wall].set_colide_type(100)
    print(self.rules)


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
                board.you_go(event.key)

        screen.fill((0, 0, 0))
        board.render(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
