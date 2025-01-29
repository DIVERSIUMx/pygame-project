#!/bin/python3
import pygame
from tric import MainBoard
import items
import Rules_and_blocks
from items import board
from Initialization_levels import start_level
from sprites import ItemSprite, FROZE, load_image
from config import clock, all_sprites, all_sprites_to_level
import level_selection

fps = 60


def test(self: MainBoard):
    """В эту функцию пихать все для тестов"""
    self.board[4][4] = [items.moris]
    self.rules[items.Moris].you = True
    # self.rules[items.Moris].weak = False

    self.board[6][5] = [items.box]
    self.board[4][5] = [items.box]
    self.board[5][5] = [items.box]
    self.rules[items.Box].set_colide_type(90)
    # self.rules[items.Box].weak = True

    self.board[5][8] = [items.wall]
    self.board[1][1] = [Rules_and_blocks.ActiveBlocksObject("wall", self)]
    self.board[1][2] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[1][3] = [Rules_and_blocks.ActiveBlocksAction("push", self)]
    self.board[2][8] = [Rules_and_blocks.ActiveBlocksObject("box", self)]
    self.board[2][9] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[3][10] = [Rules_and_blocks.ActiveBlocksAction("sink", self)]
    self.board[4][8] = [Rules_and_blocks.ActiveBlocksAction("stop", self)]
    self.board[5][10] = [Rules_and_blocks.ActiveBlocksAction("stop", self)]
    self.board[2][3] = [Rules_and_blocks.ActiveBlocksObject("moris", self)]
    self.board[2][4] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[3][5] = [Rules_and_blocks.ActiveBlocksObject("box", self)]
    # self.rules[Rules_and_blocks.ActiveBlocksObject].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksObject].push = True
    # self.rules[Rules_and_blocks.ActiveBlocksIS].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksIS].push = True
    # self.rules[Rules_and_blocks.ActiveBlocksAction].set_colide_type(90)
    self.rules[Rules_and_blocks.ActiveBlocksAction].push = True
    self.board[5][10] = [items.Water(self)]
    # self.rules[items.Water].silk = True
    self.rules[items.Wall].set_colide_type(100)
    print(issubclass(items.Box(self).__class__, items.MegaItems))
    print(self.board)


def main(level=0):
    sup = ItemSprite("test", load_image("wall.png"))
    sup.rect.x = 500
    pygame.init()
    start_level(level)
    Rules_and_blocks.get_rules()
    print(board.board)
    screen_size = width, height = board.get_screen_size()
    screen = pygame.display.set_mode(screen_size)

    running = True
    board.generate_sprites()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not FROZE[0] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    sup.die()
                print(
                    items.wall.get_rules(),
                    "wall", "\n",
                    items.box.get_rules(),
                    "box", "\n",
                    items.rock.get_rules(),
                    "rock",
                )
                board.you_go(event.key)

        screen.fill((0, 0, 0))
        board.render(screen)

        clock.tick(fps)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


def main_select():
    fps = 8
    pygame.init()
    screen_size = width, height = board.get_screen_size()
    screen = pygame.display.set_mode(screen_size)
    margin = 130
    level_board = level_selection.LevelBoard(margin)
    level_board.render()
    running = True
    outline = level_selection.OutlineRect(margin)
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
                    return None
        screen.fill((0, 0, 0))
        outline.update(screen)
        clock.tick(fps)
        all_sprites_to_level.update()
        all_sprites_to_level.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main_select()
