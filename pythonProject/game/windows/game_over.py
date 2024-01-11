import pygame

from game.events import NEWGAME
from game.settings.settings import KEY_ATTACK


class GameOver:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.display_surface.fill('black')
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("YOU DIED", True, 'yellow')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self):
        keys = pygame.key.get_pressed()
        if keys[KEY_ATTACK]:
            pygame.event.post(pygame.event.Event(NEWGAME))