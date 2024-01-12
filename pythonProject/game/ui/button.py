import pygame


class Button:
    def __init__(self, position, text, event):
        font = pygame.font.Font("game/graphics/fonts/Almendra-Bold.otf", 36)
        self.image = pygame.transform.scale(pygame.image.load("game/graphics/ui/button.png").convert_alpha(),(256, 64))
        self.image_rect = self.image.get_rect(center=position)
        self.text = font.render(text, True, 'white')
        self.text_rect = self.text.get_rect(center=position)
        self.event = event
        self.display_surface = pygame.display.get_surface()

    def update(self):
        click_pos = pygame.mouse.get_pos()
        if (self.image_rect.topleft[0] < click_pos[0] < self.image_rect.topleft[0] + self.image_rect.width and
                self.image_rect.topleft[1] < click_pos[1] < self.image_rect.topleft[1] + self.image_rect.height):
            self.image.set_alpha(100)
            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(self.event))
        else:
            self.image.set_alpha(255)
        self.display_surface.blit(self.image, self.image_rect)
        self.display_surface.blit(self.text, self.text_rect)
