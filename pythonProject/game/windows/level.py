import pygame

from game.map_data.warp_points import warp_points
from game.sprite_groups.ground_sprite_group import GroundSpriteGroup
from game.sprite_groups.warp_points_sprite_group import WarpPointsSpriteGroup
from game.sprite_groups.y_sort_sprite_group import YSortSpriteGroup
from game.sprites.entities.enemy import Enemy
from game.sprites.misc.hitbox import Hitbox
from game.sprites.misc.warp_point import WarpPoint
from game.mobs.player import mob_player
from game.settings.settings import *
from game.sprites.tiles.tile import Tile
from game.sprites.entities.player import Player
from game.maps.maps import *
from game.ui.ui import UI


class Level:
    def __init__(self, level_map, player_position=None):
        # fields
        self.display_surface = pygame.display.get_surface()
        self.player_position = player_position
        self.player = None
        self.map = None
        self.ui = None
        self.init_time = pygame.time.get_ticks()
        self.text_fade_start_time = 500
        self.text_fade_in_time = 1500
        self.text_fade_out_time = 2500
        self.text_time = 3500

        # sprite groups
        self.ground_sprites = GroundSpriteGroup()
        self.visible_sprites = YSortSpriteGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.warp_points = WarpPointsSpriteGroup()

        # load map
        self.load_map(level_map)

    def load_map(self, map):
        # draw loading text
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("LOADING...", True, 'white')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(text_surface, text_rect)
        pygame.display.flip()

        # set fields
        self.map = map
        self.draw_map()
        self.ui = UI()

        pygame.display.flip()

    def draw_map(self):
        ground_map = self.map.get_layer('ground')
        objects_map = self.map.get_layer('objects')
        blocking_map = self.map.get_layer('blocking')

        # draw ground
        for row_index, row in enumerate(ground_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Tile(self.map.ground_palette[col], (x, y), [self.ground_sprites])

        # draw objects
        for row_index, row in enumerate(objects_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Tile(self.map.objects_palette[col], (x, y), [self.visible_sprites])

        # draw blocking
        for row_index, row in enumerate(blocking_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != (255, 255, 255):
                    Hitbox((x, y), [self.obstacle_sprites])

        # draw entities
        for i in range(0, len(self.map.entities)):
            x = (self.map.entities[i][0][0] - 1) * TILESIZE
            y = (self.map.entities[i][0][1] - 1) * TILESIZE
            if self.map.entities[i][1] == "enemy":
                Enemy((x, y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites,
                      self.map.entities[i][2])

        # draw player
        if self.player_position is not None:
            x = (self.player_position[0] - 1) * TILESIZE
            y = (self.player_position[1] - 1) * TILESIZE
            self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites,
                                 mob_player)
        for i in range(0, len(self.map.entities)):
            x = (self.map.entities[i][0][0] - 1) * TILESIZE
            y = (self.map.entities[i][0][1] - 1) * TILESIZE
            if self.map.entities[i][1] == "player" and self.player_position is None:
                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.visible_sprites,
                                     mob_player)

        # draw warp points
        for i in range(0, len(warp_points)):
            if self.map == warp_points[i][0]:
                x = (warp_points[i][1][0] - 1) * TILESIZE
                y = (warp_points[i][1][1] - 1) * TILESIZE
                WarpPoint((x, y), [self.warp_points], warp_points[i][2], warp_points[i][3])

    def draw_location_name(self):
        current_time = pygame.time.get_ticks() - self.init_time
        if current_time < self.text_time:
            font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
            text_surface = font.render(self.map.name, True, 'white')
            bg_surface = pygame.Surface((self.display_surface.get_width(), text_surface.get_height() + 16))
            bg_surface.fill('black')
            if current_time <= self.text_fade_start_time:
                alpha = 0
            elif current_time <= self.text_fade_in_time:
                alpha = 255 * (current_time - self.text_fade_start_time) / 1000
            elif current_time >= self.text_fade_out_time:
                alpha = 255 - 255 * (current_time - self.text_fade_out_time) / 1000
            else:
                alpha = 255
            bg_surface.set_alpha(alpha)
            bg_surface.blit(text_surface, (bg_surface.get_width() // 2 - text_surface.get_width() // 2, bg_surface.get_height() // 2 - 24))
            self.display_surface.blit(bg_surface, (self.display_surface.get_width() // 2 - bg_surface.get_width() // 2, 64 - bg_surface.get_height() // 2))

    def run(self):
        self.ground_sprites.custom_draw(self.player, self.map)
        self.visible_sprites.custom_draw(self.player, self.map)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.warp_points.warp_points_update(self.player)
        self.draw_location_name()
        self.ui.draw(self.player)

