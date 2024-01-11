import pygame
from game.settings.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=position)