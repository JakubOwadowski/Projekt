import pygame
from game.settings.settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT_STYLE, UI_FONT_SIZE)

        self.health_bar_rect = pygame.Rect(0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT)
        self.fury_bar_rect = pygame.Rect(UI_BAR_WIDTH, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT)
        self.exp_bar_rect = pygame.Rect(0, UI_BAR_HEIGHT, UI_EXP_BAR_WIDTH, UI_BAR_WIDTH)
    def draw(self, player):
        self.draw_bar(player.current_stats["health"], player.base_stats["health"], self.health_bar_rect, UI_HP_BAR_COLOUR, "vertical")
        self.draw_bar(player.current_stats["fury"], player.base_stats["max fury"], self.fury_bar_rect, UI_FURY_BAR_COLOUR, "vertical")
        self.draw_bar(player.current_stats["experience"], player.base_stats["next level"], self.exp_bar_rect, UI_MANA_BAR_COLOUR, "horizontal")

    def draw_bar(self, current, max, bg, colour, direction):
        pygame.draw.rect(self.display_surface, UI_BAR_BG_COLOUR, bg)
        if direction == "vertical":
            current_height = bg.height * current / max
            current_rect = bg.copy()
            current_rect.height = current_height
        elif direction == "horizontal":
            current_width = bg.width * current / max
            current_rect = bg.copy()
            current_rect.width = current_width
        pygame.draw.rect(self.display_surface, colour, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg, 3)
