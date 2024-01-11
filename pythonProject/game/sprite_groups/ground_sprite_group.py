import pygame

from game.settings.settings import *


class GroundSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, map):
        self.offset.x = player.rect.centerx - self.display_surface.get_size()[0] // 2
        if self.offset.x < 0:
            self.offset.x = 0
        elif self.offset.x > map.width() - WIDTH // 2 - self.display_surface.get_size()[0] // 2:
            self.offset.x = map.width() - WIDTH // 2 - self.display_surface.get_size()[0] // 2
        self.offset.y = player.rect.centery - self.display_surface.get_size()[1] // 2
        if self.offset.y < 0:
            self.offset.y = 0
        elif self.offset.y > map.height() - HEIGHT // 2 - self.display_surface.get_size()[1] // 2:
            self.offset.y = map.height() - HEIGHT // 2 - self.display_surface.get_size()[1] // 2
        for sprite in self.sprites():
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)
