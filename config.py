import pygame
import os
pygame.mixer.init()

all_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()
end_screen_sprites = pygame.sprite.Group()

all_sprites_to_level = pygame.sprite.Group()
select_level_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
destroy_sound = pygame.mixer.Sound(
    os.path.join("data", "sound", "destroy.wav"))
move_sound = pygame.mixer.Sound(
    os.path.join("data", "sound", "move.wav"))

global froze
froze = False
