import pygame

all_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()

all_sprites_to_level = pygame.sprite.Group()
select_level_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

global froze
froze = False
