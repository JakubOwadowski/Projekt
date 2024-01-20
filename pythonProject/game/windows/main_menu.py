import pygame

from game.events.events import NEWGAME, LOADGAME
from game.ui.button import Button


class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.load_game_button = Button(
            (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 50),
            "LOAD GAME",
            event=pygame.event.post,
            event_args=pygame.event.Event(LOADGAME))
        self.new_game_button = Button(
            (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 150),
            "NEW GAME",
            event=pygame.event.post,
            event_args=pygame.event.Event(NEWGAME))

    def run(self):
        self.display_surface.fill('black')
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("LEGEND OF SIR NOODLEHEAD", True, 'yellow')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 150))
        self.display_surface.blit(text_surface, text_rect)
        self.new_game_button.update()
        self.load_game_button.update()
        pygame.display.flip()
