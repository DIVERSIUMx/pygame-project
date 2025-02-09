import pygame
import os
from sprites import SelectSprite, clock, all_sprites_to_level
from items import board
from main import main

fps = 8


def load_image(*filename):
    path = os.path.join("data", "sprite", "select-level", *filename)
    return pygame.image.load(path)


class LevelBoard:  # Доска для выбора уровня
    def __init__(self, margin):
        self.height = 5
        self.width = 9
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.pos_now = (0, 0)
        # Все "Картинки" для выбора уровня
        self.board[0][0] = 'level-1.png'
        self.board[0][1] = 'level-2.png'
        self.board[0][2] = 'level-3.png'
        self.board[0][3] = 'level-4.png'
        self.board[0][4] = 'level-5.png'
        self.board[0][5] = 'level-6.png'
        self.board[0][6] = 'level-7.png'
        self.board[0][7] = 'level-8.png'

        # print(self.board)
        self.margin = margin

    def render(self):
        stop = False

        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] is None:
                    # в случаи если уровни закончились
                    stop = True
                    break
                # Каждая картинка - спрайт
                now = pygame.sprite.Sprite(all_sprites_to_level)
                now.image = load_image(self.board[y][x])
                now.rect = now.image.get_rect()
                now.rect.x = self.margin * (x + 1)
                now.rect.y = self.margin * (y + 1)
            if stop:
                break

    def step(self, delta):  # Изменение позиции при перемещении
        if 0 <= delta[0] + self.pos_now[0] < self.width and 0 <= delta[1] + self.pos_now[1] < self.height:
            if not self.board[self.pos_now[1] + delta[1]][self.pos_now[0] + delta[0]] is None:
                self.pos_now = (self.pos_now[0] + delta[0], self.pos_now[1] + delta[1])


class OutlineRect:  # Обводка, указывающая на текущее местоположение
    def __init__(self, margin):
        self.color = 'white'
        self.counter = 1
        self.cell = 2
        self.margin = margin
        self.x = margin - self.cell
        self.y = margin - self.cell

    def change_cell(self, pos):  # Изменение положения
        x, y = pos
        self.x = self.margin * (x + 1) - self.cell
        self.y = self.margin * (y + 1) - self.cell

    def update(self, surf):  # Используется для мигания
        if self.counter == 1:
            pygame.draw.rect(surf, self.color, ((self.x, self.y), (80 + self.cell, 80 + self.cell)), self.cell)
        else:
            pygame.draw.rect(surf, 'black', ((self.x, self.y), (80 + self.cell, 80 + self.cell)), self.cell)
        self.counter = 0 if self.counter == 1 else 1


def main_select():  # Для прямого запуска
    pygame.init()
    screen_size = width, height = board.get_screen_size()
    screen = pygame.display.set_mode(screen_size)
    margin = 130
    level_board = LevelBoard(margin)
    level_board.render()
    running = True
    outline = OutlineRect(margin)
    outline.update(screen)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    level_board.step((1, 0))
                    outline.change_cell(level_board.pos_now)
                if event.key == pygame.K_a:
                    level_board.step((-1, 0))
                    outline.change_cell(level_board.pos_now)
                if event.key == pygame.K_w:
                    level_board.step((0, -1))
                    outline.change_cell(level_board.pos_now)
                if event.key == pygame.K_s:
                    level_board.step((0, 1))
                    outline.change_cell(level_board.pos_now)
                if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                    x, y = pos = level_board.pos_now
                    level = (x + 1) + y * level_board.width
                    main(f'level-{level}')
        screen.fill((0, 0, 0))
        outline.update(screen)
        clock.tick(fps)
        all_sprites_to_level.update()
        all_sprites_to_level.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    start = None
