from functools import lru_cache

import pygame.image


@lru_cache
def img_load(path):
    return pygame.image.load(path).convert_alpha()
