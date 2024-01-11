import pygame

from game.events import WARP
from game.settings.settings import *


class WarpPoint(pygame.sprite.Sprite):
    def __init__(self, position, groups, destination_map, destination_position):
        super().__init__(groups)
        self.rect = pygame.rect.Rect((position[0], position[1], TILESIZE, TILESIZE))
        self.destination_map = destination_map
        self.destination_position = destination_position

    def warp_points_update(self, player):
        if player.hitbox.colliderect(self.rect):
            pygame.event.post(pygame.event.Event(WARP, {"destination map": self.destination_map,
                                                        "destination position": self.destination_position}))
