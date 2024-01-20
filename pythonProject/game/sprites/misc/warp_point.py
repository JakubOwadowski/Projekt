from game.events.events import WARP
from game.events.events import RANDOMWARP
from game.settings.settings import *


class WarpPoint(pygame.sprite.Sprite):
    def __init__(self, position, groups, destination_map, destination_position):
        super().__init__(groups)
        self.rect = pygame.rect.Rect((position[0], position[1], TILESIZE, TILESIZE))
        self.destination_map = destination_map
        self.destination_position = destination_position

    def warp_point_update(self, player):
        if player.hitbox.colliderect(self.rect):
            pygame.event.post(pygame.event.Event(WARP, {"destination map": self.destination_map,
                                                        "destination position": self.destination_position}))


class StairsRandom(pygame.sprite.Sprite):
    def __init__(self, position, groups, destination_map, ascend=False):
        super().__init__(groups)
        self.rect = pygame.rect.Rect((position[0], position[1], TILESIZE, TILESIZE))
        self.destination_map = destination_map
        self.ascend = ascend
        self.colliding = True

    def warp_point_update(self, player):
        key = pygame.key.get_pressed()
        if player.hitbox.colliderect(self.rect) and key[KEY_INTERACT] and not self.colliding:
            self.colliding = True
            pygame.event.post(pygame.event.Event(RANDOMWARP,
                                                 {"destination map": self.destination_map, "ascend": self.ascend}))
        elif not player.hitbox.colliderect(self.rect):
            self.colliding = False


class Stairs(pygame.sprite.Sprite):
    def __init__(self, position, groups, destination_map, destination_position):
        super().__init__(groups)
        self.destination_position = destination_position
        self.rect = pygame.rect.Rect((position[0], position[1], TILESIZE, TILESIZE))
        self.destination_map = destination_map
        self.colliding = True

    def warp_point_update(self, player):
        key = pygame.key.get_pressed()
        if player.hitbox.colliderect(self.rect) and key[KEY_INTERACT] and not self.colliding:
            self.colliding = True
            pygame.event.post(pygame.event.Event(WARP, {"destination map": self.destination_map,
                                                        "destination position": self.destination_position}))
        elif not player.hitbox.colliderect(self.rect):
            self.colliding = False
            