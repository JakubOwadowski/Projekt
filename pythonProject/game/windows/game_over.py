import pygame

from game.events.events import NEWGAME
from game.ui.button import Button


class GameOver:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.restart_button = Button(
            (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 100),
            "PLAY AGAIN",
            event=pygame.event.post,
            event_args=pygame.event.Event(NEWGAME))

    def run(self):
        self.display_surface.fill('black')
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("YOU DIED", True, 'yellow')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(text_surface, text_rect)
        self.restart_button.update()
        pygame.display.flip()
