import pygame
from game.settings.settings import *


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.rect = pygame.rect.Rect((position[0], position[1], TILESIZE, TILESIZE))
        self.hitbox = self.rect.inflate(-10, -10)
