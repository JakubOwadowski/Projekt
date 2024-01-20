import pygame


class WarpPointsSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def warp_points_update(self, player):
        warp_points = [warp_point for warp_point in self.sprites()]
        for warp_point in warp_points:
            warp_point.warp_point_update(player)
