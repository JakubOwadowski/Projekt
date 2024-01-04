import pygame
from game.settings.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('game/graphics/tiles/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)