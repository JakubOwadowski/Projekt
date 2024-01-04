import pygame
from game.settings.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('game/graphics/tiles/tree.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)