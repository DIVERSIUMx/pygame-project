import pygame

all_sprites = pygame.sprite.Group()
item_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()
end_screen_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

global froze
froze = False
