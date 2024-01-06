import pygame.sprite
from game.utils.image_splitter import ImageSplitter

class SlashBlur(pygame.sprite.Sprite):
    def __init__(self, position, facing, groups):
        super().__init__(groups)
        self.frames = ImageSplitter().split("game/graphics/misc/slash_blur.png", 7, ["Down", "Up", "Left", "Right"])
        self.prev_frame = 0
        self.next_frame = 15
        self.frame = 0
        self.facing = facing
        self.image = pygame.transform.scale(pygame.image.fromstring(
            self.frames["Up"][self.frame].tobytes(),
            self.frames["Up"][self.frame].size,
            self.frames["Up"][self.frame].mode).convert_alpha(),
                                            (64, 64))
        self.rect = self.image.get_rect(topleft=position)

    def set_image(self):
        if self.facing == "up":
            image = self.frames["Up"][self.frame]
        elif self.facing == "down":
            image = self.frames["Down"][self.frame]
        elif self.facing == "left":
            image = self.frames["Left"][self.frame]
        elif self.facing == "right":
            image = self.frames["Right"][self.frame]
        self.image = pygame.transform.scale(pygame.image.fromstring(
            image.tobytes(),
            image.size,
            image.mode).convert_alpha(),
                                            (64, 64))

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.prev_frame >= self.next_frame:
            self.prev_frame = current_time
            self.frame += 1
            if self.frame >= 7:
                self.kill()

    def update(self):
        self.set_image()
        self.cooldowns()

