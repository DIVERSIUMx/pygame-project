#!/bin/python3
import pygame
from tric import MainBoard

fps = 60

if __name__ == "__main__":
    pygame.init()
    board = MainBoard(16, 10, 80)

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
