import pygame


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # RENDER YOUR GAME HERE

        pygame.display.flip()

        clock.tick(60)
    pygame.quit()
