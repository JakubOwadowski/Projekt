import pygame

from game.events import NEWGAME, LOADGAME


class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.new_game_button = None

    def run(self):
        self.display_surface.fill('black')
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.display_surface.fill('black')
        text_surface = font.render("LEGEND OF SIR NOODLEHEAD", True, 'yellow')
        text_rect = text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 150))
        self.display_surface.blit(text_surface, text_rect)

        self.new_game_button = pygame.transform.scale(pygame.image.load("game/graphics/ui/button.png").convert_alpha(),
                                                      (256, 64))
        self.load_game_button = pygame.transform.scale(pygame.image.load("game/graphics/ui/button.png").convert_alpha(),
                                                      (256, 64))

        new_game_button_rect = self.new_game_button.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 200))
        new_game_text_surface = font.render("NEW GAME", True, 'white')
        new_game_text_rect = new_game_text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 200))

        load_game_button_rect = self.load_game_button.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 100))
        load_game_text_surface = font.render("LOAD GAME", True, 'white')
        load_game_text_rect = load_game_text_surface.get_rect(
            center=(self.display_surface.get_width() // 2, text_rect.bottom + 100))

        click_pos = pygame.mouse.get_pos()
        if new_game_button_rect.topleft[0] < click_pos[0] < new_game_button_rect.topleft[0] + new_game_button_rect.width and new_game_button_rect.topleft[
            1] < click_pos[1] < new_game_button_rect.topleft[1] + new_game_button_rect.height:
            self.new_game_button.set_alpha(100)
            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(NEWGAME))

        if load_game_button_rect.topleft[0] < click_pos[0] < load_game_button_rect.topleft[0] + load_game_button_rect.width and load_game_button_rect.topleft[
            1] < click_pos[1] < load_game_button_rect.topleft[1] + load_game_button_rect.height:
            self.load_game_button.set_alpha(100)
            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(LOADGAME))

        self.display_surface.blit(self.new_game_button, new_game_button_rect)
        self.display_surface.blit(self.load_game_button, load_game_button_rect)
        self.display_surface.blit(new_game_text_surface, new_game_text_rect)
        self.display_surface.blit(load_game_text_surface, load_game_text_rect)
        pygame.display.flip()
