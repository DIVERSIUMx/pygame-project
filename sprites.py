import pygame
import os
from config import all_sprites, item_sprites, particle_sprites, block_sprites, end_screen_sprites, clock, froze, \
    select_level_sprites, all_sprites_to_level, move_sound, destroy_sound
import random

pygame.init()
FROZE = [False]


def load_image(*filename):
    path = os.path.join("data", "sprite", *filename)
    if os.path.isfile(path):
        return pygame.image.load(path)
    else:
        return pygame.image.load(os.path.join("data", "sprite", "ohno.png"))


class SlideSprite(pygame.sprite.Sprite):  # Спрайт для плавного сдвига
    def __init__(self, image, start_pos, end_pos, time):
        super().__init__(all_sprites, end_screen_sprites)
        self.end_pos = end_pos
        self.image: pygame.Surface = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = start_pos
        self.dx = (end_pos[0] - start_pos[0]) / (60 * time)
        self.dy = (end_pos[1] - start_pos[1]) / (60 * time)
        self.end_time = time * 60
        self.cur_time = 0

    def update(self):
        if self.cur_time < self.end_time:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_time += 1


# Спрайт для отображения времени в формате мм:сс
class TimeCounterSprite(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        super().__init__(all_sprites, end_screen_sprites)
        self.rect = rect
        self.font = pygame.font.Font(os.path.join(
            "data", "font", "NEOPIXEL.otf"), self.rect.width // 5)
        self.value = 0
        self.image = self.font.render(
            str(self.value // 60).rjust(
                2, "0"
            ) + ":" + str(self.value % 60).rjust(2, "0"), 1, (255, 255, 255)
        )

    def set_value(self, value):
        self.value = value
        self.image = self.font.render(
            str(self.value // 60).rjust(
                2, "0"
            ) + ":" + str(self.value % 60).rjust(2, "0"), 1, (255, 255, 255)
        )


class ResultShowSprite(pygame.sprite.Sprite):  # Спрайт отображения результата
    def __init__(self, rect: pygame.Rect, nums_count):
        super().__init__(all_sprites, end_screen_sprites)
        self.nums_count = nums_count
        self.rect = rect
        self.font = pygame.font.Font(os.path.join(
            "data", "font", "NEOPIXEL.otf"), self.rect.width // nums_count)
        self.value = 0
        self.image = self.font.render(
            str(self.value).rjust(
                self.nums_count, "0"
            ), 1, (255, 255, 255)
        )

    def set_value(self, value):
        self.value = value
        self.image = self.font.render(
            str(self.value).rjust(
                self.nums_count, "0"
            ), 1, (255, 255, 255)
        )


class BlockSprite(pygame.sprite.Sprite):  # Спрайт блокировки частиц
    def __init__(self, pos, width):
        super().__init__(all_sprites, block_sprites)
        self.image = pygame.Surface((width, 30))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class ItemSprite(pygame.sprite.Sprite):  # Спрайт объекта
    def __init__(self, filename, file, colums=1, rows=1):
        self.die_soon = False
        self.moving = False
        self.move_stage = 0
        self.target = (0, 0)
        self.filename = filename
        self.colums = colums
        self.rows = rows
        super().__init__(all_sprites, item_sprites)
        self.im = file
        if colums == rows == 1:
            self.frames = [pygame.transform.scale(self.im, (80, 80))]
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
        else:
            self.im = pygame.transform.scale(self.im, (80 * colums, 80 * rows))
            self.frames = tuple(
                self.im.subsurface(x * 80, y * 80, 80, 80)
                for x in range(colums) for y in range(rows)
            )
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
        self.rect.x = -100

    def update(self):
        global FROZE
        self.image = self.frames[pygame.time.get_ticks() // 240 %
                                 len(self.frames)]
        if self.moving:
            self.rect.x += self.delta_x
            self.rect.y += self.delta_y
            self.move_stage += 1
            if self.move_stage >= 7:
                self.rect.x = self.target[0]
                self.rect.y = self.target[1]
                self.moving = False
                self.move_stage = 0
                FROZE[0] = False
                if self.die_soon:
                    self.die_soon = False
                    self.die()

    def copy(self):
        return ItemSprite(self.filename, self.im, self.colums, self.rows)

    def move(self, pos):  # Задаётся позиция для перемешения
        global FROZE
        self.move_stage = 0
        self.target = pos
        self.delta_x = (pos[0] - self.rect.x) / 7
        self.delta_y = (pos[1] - self.rect.y) / 7
        FROZE[0] = True
        self.moving = True
        # move_sound.play()

    def die(self):  # Смерть, спрайт "Рассыпается"
        if self.moving:
            self.die_soon = True
        else:
            for x in range(8):
                for y in range(8):
                    ParticleSprite(
                        self.image.subsurface(
                            x * 10, y * 10, 10, 10
                        ), x * 10 + self.rect.x, y * 10 + self.rect.y, random.randint(-10, 10),
                        random.randint(-10, 10),
                        180
                    )
            FROZE[0] = False
            destroy_sound.play()
            self.kill()


class ParticleSprite(pygame.sprite.Sprite):  # Спрайт частици
    def __init__(self, image, x, y, vecx, vecy, live_time):
        super().__init__(all_sprites, particle_sprites)
        self.collided = False
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = vecx
        self.dy = vecy
        self.live_time = live_time

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)
        if self.dy < 10:
            self.dy += 0.4

        # Частица может отпрыгнуть с шансом 50% если ещё не отпрагнула
        if not self.collided and pygame.sprite.spritecollideany(self, block_sprites) and self.dy > 0:
            if random.randint(0, 1):
                self.dy = -self.dy
            self.collided = True
        if self.live_time <= 0:
            self.kill()
        else:
            self.live_time -= 1


class SelectSprite(pygame.sprite.Sprite):  # спрайты для выбора уровня
    def __init__(self, file):
        super().__init__(all_sprites_to_level, select_level_sprites)
        self.file = file
        self.rect = self.file.get_rect()
