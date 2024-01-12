import pygame

from game.events import NEWGAME


class GameOver:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.restart_button = None

    def run(self):
        self.display_surface.fill('black')
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("YOU DIED", True, 'yellow')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        self.display_surface.blit(text_surface, text_rect)
        self.restart_button = pygame.transform.scale(pygame.image.load("game/graphics/ui/button.png").convert_alpha(),
                                                     (256, 64))
        button_rect = self.restart_button.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 50))
        text_surface = font.render("PLAY AGAIN", True, 'white')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 50))
        click_pos = pygame.mouse.get_pos()
        if button_rect.topleft[0] < click_pos[0] < button_rect.topleft[0] + button_rect.width and button_rect.topleft[
            1] < click_pos[1] < button_rect.topleft[1] + button_rect.height:
            self.restart_button.set_alpha(100)
            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(NEWGAME))
        self.display_surface.blit(self.restart_button, button_rect)
        self.display_surface.blit(text_surface, text_rect)
        pygame.display.flip()
