import pygame
from game.settings.settings import *
from game.map_objects.tile import Tile
from game.map_objects.player import Player
from game.debug.debug import debug
from game.maps.maps import Maps


class Level:
    def __init__(self):

        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.map = Maps().test_forest_map
        self.ground_sprites = YSortCameraGroundGroup()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.draw_map()

    def draw_map(self):

        ground_map = self.map.get_layer('ground')
        objects_map = self.map.get_layer('objects')
        entities_map = self.map.get_layer('entities')
        blocking_map = self.map.get_layer('blocking')
        for row_index, row in enumerate(ground_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Tile(self.map.ground_palette[col], (x, y), [self.ground_sprites])
        for row_index, row in enumerate(objects_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Tile(self.map.objects_palette[col], (x, y), [self.visible_sprites])
        for row_index, row in enumerate(blocking_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Tile(self.map.blocking_palette[col], (x, y), [self.obstacle_sprites])
        for row_index, row in enumerate(entities_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    self.player = Player(self.map.entities_palette[col],(x, y), [self.visible_sprites], self.obstacle_sprites)

    def draw(self):
        self.ground_sprites.custom_draw(self.player, self.map)
        self.visible_sprites.custom_draw(self.player, self.map)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
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
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class YSortCameraGroundGroup(pygame.sprite.Group):
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
