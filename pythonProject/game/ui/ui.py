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
        self.draw_bar(player.current_health, player.base_health, self.health_bar_rect, UI_HP_BAR_COLOUR, "vertical")
        self.draw_bar(player.current_fury, player.max_fury, self.fury_bar_rect, UI_FURY_BAR_COLOUR, "vertical")
        self.draw_bar(player.exp, player.next_level, self.exp_bar_rect, UI_MANA_BAR_COLOUR, "horizontal")
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 28)
        text_surface = font.render(str(player.level), True, 'white')
        text_rect = text_surface.get_rect(
            center=(self.exp_bar_rect.center[0], self.exp_bar_rect.center[1] - 2))
        self.display_surface.blit(text_surface, text_rect)

    def draw_bar(self, current, max, bg, colour, direction):
        pygame.draw.rect(self.display_surface, UI_BAR_BG_COLOUR, bg)
        if direction == "vertical":
            current_height = bg.height * current / max
            current_rect = bg.copy()
            current_rect.height = current_height
            current_rect.top += bg.height - bg.height * current / max
        elif direction == "horizontal":
            current_width = bg.width * current / max
            current_rect = bg.copy()
            current_rect.width = current_width
        pygame.draw.rect(self.display_surface, colour, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg, 3)
