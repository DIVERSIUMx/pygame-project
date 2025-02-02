#!/bin/python3
import os

import pygame
from tric import MainBoard
import items
import Rules_and_blocks
import sys
from items import board
from Initialization_levels import start_level
from sprites import ItemSprite, FROZE, load_image, BlockSprite, SlideSprite, ResultShowSprite, TimeCounterSprite, \
    all_sprites_to_level
from config import clock, all_sprites, end_screen_sprites, item_sprites
import level_selection

fps = 60


def terminate():
    pygame.quit()
    sys.exit()


def end_screen(end_img, time, move_count, undo_count):
    Rules_and_blocks.checking_for_rule_existence(board.board)
    screen.fill(0)
    fps = 60
    transparent_val = 1
    end_image = pygame.Surface(screen_size)
    state = 0
    screen_filter = pygame.Surface(screen_size)
    screen_filter.fill((0, 0, 0))
    screen_filter.set_alpha(transparent_val)
    img = pygame.transform.scale(
        load_image("you_win.png"), (600, 300)
    )
    rect = img.get_size()
    slide = SlideSprite(
        img, (width, height // 2 -
              rect[1] // 2), (width // 2 - rect[1] // 2, height // 2 - rect[1] // 2), 0.5
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                state += 1
                break
            elif event.type == pygame.KEYDOWN:
                state += 1
                break
        if state == 0:
            end_screen_sprites.update()
            if slide.cur_time >= slide.end_time:
                state = 1
        elif state == 1:
            slide.rect.x, slide.rect.y = slide.end_pos
            check_counter = ResultShowSprite(
                pygame.Rect(200, height / 4, 500, 200), 5
            )
            state = 2
        elif state == 2:
            check_counter.set_value(
                check_counter.value + int((pygame.time.get_ticks() % 3) == 0)
            )
            if check_counter.value == move_count:
                state = 3
        elif state == 3:
            true_check_counter = ResultShowSprite(
                pygame.Rect(200, height / 4 * 2, 500, 200), 5
            )
            state = 4
        elif state == 4:
            true_check_counter.set_value(
                true_check_counter.value +
                int((pygame.time.get_ticks() % 3) == 0)
            )
            if true_check_counter.value == move_count + undo_count:
                state = 5
        elif state == 5:
            time_counter = TimeCounterSprite(
                pygame.Rect(200, height / 4 * 3, 500, 200)
            )
            state = 6
        elif state == 6:
            time_counter.set_value(
                time_counter.value + int((pygame.time.get_ticks() % 3) == 0)
            )
            if time_counter.value >= time:
                state = 8
        elif state != 8:
            for sprite in end_screen_sprites.sprites():
                sprite.kill()
            for sprite in item_sprites.sprites():
                sprite.kill()
            board.clear()
            main_exit()
            return None

        item_sprites.update()
        screen.fill((0, 0, 0))
        board.render(screen)
        item_sprites.draw(screen)
        screen.blit(screen_filter, (0, 0))
        if transparent_val < 255:
            transparent_val += 3
        else:
            transparent_val = 255
        screen_filter.set_alpha(transparent_val)
        end_screen_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        '''print(time)'''


def test(self: MainBoard):
    """В эту функцию пихать все для тестов"""
    self.board[4][4] = [items.moris]
    # self.rules[items.Moris].weak = False

    self.board[6][5] = [items.flag]
    self.board[4][5] = [items.skull]
    self.board[5][5] = [items.box]
    # self.rules[items.Box].weak = True

    self.board[5][8] = [items.rock]
    self.board[1][1] = [Rules_and_blocks.ActiveBlocksObject("flag", self)]
    self.board[1][2] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[1][3] = [Rules_and_blocks.ActiveBlocksAction("win", self)]
    self.board[2][8] = [Rules_and_blocks.ActiveBlocksObject("box", self)]
    self.board[2][9] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[3][10] = [Rules_and_blocks.ActiveBlocksAction("death", self)]
    self.board[4][8] = [Rules_and_blocks.ActiveBlocksAction("stop", self)]
    self.board[5][10] = [Rules_and_blocks.ActiveBlocksAction("stop", self)]
    self.board[2][3] = [Rules_and_blocks.ActiveBlocksObject("moris", self)]
    self.board[2][4] = [Rules_and_blocks.ActiveBlocksIS(self)]
    self.board[3][5] = [Rules_and_blocks.ActiveBlocksObject("box", self)]
    self.board[5][10] = [items.Water(self)]
    # self.rules[items.Water].silk = True
    print(issubclass(items.Box(self).__class__, items.MegaItems))
    print(self.board)


def main(level: str):
    board.clear()
    Rules_and_blocks.clear_rules()
    Rules_and_blocks.checking_for_rule_existence(board.board)
    fps = 60
    start_level(level)
    Rules_and_blocks.get_rules()
    Rules_and_blocks.checking_for_rule_existence(board.board)
    print(board.board)
    # Rules_and_blocks.get_rules()
    print(board.board)

    time = 0
    undo_count = 0
    running = True
    BlockSprite((0, height), width)
    test(board)

    board.generate_sprites()
    end_image = pygame.Surface(screen_size)
    end_image.blit(screen, (0, 0))
    while True:
        for event in pygame.event.get():
            Rules_and_blocks.get_rules()
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_select()
                    return None
            if not FROZE[0] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    board.undo()
                    undo_count += 1
                else:
                    if board.you_go(event.key):
                        print("YOU WIN")
                        running = False
                        end_image.blit(screen, (0, 0))
        if not running:
            break
        screen.fill((0, 0, 0))
        board.render(screen)

        time += clock.tick(fps) / 1000
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

    end_screen(end_image, int(time), len(board.history_items), undo_count)


def main_select():  # Выбор уровня
    fps = 8
    margin = 130  # Отступы
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
                if event.key == pygame.K_ESCAPE:
                    # Уход на уровень выше ( стартовое окно )
                    main_start()
                    return None
                # Перемещение по меню
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
                    # запуск уровня
                    main(f'level-{level}')
                    return None
        screen.fill((0, 0, 0))
        outline.update(screen)
        clock.tick(fps)
        all_sprites_to_level.update()  # мигание обводки
        all_sprites_to_level.draw(screen)
        pygame.display.flip()

    pygame.quit()
    exit()


def main_start():  # Функция открывающая стартовое окно
    Rules_and_blocks.clear_rules()  # Отчистка всего, что могло остаться
    Rules_and_blocks.checking_for_rule_existence(board.board)
    fps = 3
    running = True
    screen.fill((0, 0, 0))
    font_title = pygame.font.Font(os.path.join(
        "data", "font", "NEOPIXEL.otf"), 100)
    text_title = font_title.render("Жизнь для правил", True, 'white')
    text_x = width // 2 - text_title.get_width() // 2
    screen.blit(text_title, (text_x, 200))
    fonr_start = pygame.font.Font(
        os.path.join("data", "font", "NEOPIXEL.otf"), 30)
    test_start = fonr_start.render(
        "нажмите любую кнопку, чтобы продолжить", True, 'white')
    show = True
    while running:
        # Мигание текста
        if show:
            screen.blit(test_start, (text_x + 100, 700))
            show = False
        else:
            show = True
            pygame.draw.rect(
                screen, 'black', ((text_x, 600), (text_x + 700, 1000)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Выход из программы
                    return None
                # Открывает уровень ниже ( выбор уровня )
                main_select()
                return None

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


def main_exit():  # Функция конечного экрана
    Rules_and_blocks.clear_rules()
    Rules_and_blocks.checking_for_rule_existence(board.board)
    fps = 3
    running = True
    screen.fill((0, 0, 0))
    font_title = pygame.font.Font(os.path.join(
        "data", "font", "NEOPIXEL.otf"), 100)
    text_title = font_title.render("Хотите продолжить?", True, 'white')
    text_1 = font_title.render("esc - выход", True, 'white')
    text_x = width // 2 - text_title.get_width() // 2
    screen.blit(text_title, (text_x, 200))
    screen.blit(text_1, (text_x + 100, 300))
    fonr_start = pygame.font.Font(
        os.path.join("data", "font", "NEOPIXEL.otf"), 30)
    test_start = fonr_start.render(
        "Чтобы продолжить, нажмите любую кнопку", True, 'white')
    show = True
    while running:
        # Отвечает за мигание текста
        if show:
            screen.blit(test_start, (text_x + 100, 700))
            show = False
        else:
            show = True
            pygame.draw.rect(
                screen, 'black', ((text_x, 600), (text_x + 700, 1000)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Выход из программы
                    return None
                # Открывает выбор уровня
                main_select()
                return None

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    fps = 60
    pygame.init()
    screen_size = width, height = board.get_screen_size()
    screen = pygame.display.set_mode(screen_size)
    main_start()
