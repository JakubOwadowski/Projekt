import math

import pygame.sprite

from game.settings.settings import TILESIZE
from game.utils.image_splitter import split


class GenericAttack(pygame.sprite.Sprite):
    def __init__(self, position, path_to_image, facing, groups, visible_sprites):
        super().__init__(*groups)
        self.frame = 0
        self.number_of_frames = 7
        self.animation_speed = 1
        self.frames = split(path_to_image, self.number_of_frames, ["Attack"])
        self.facing = facing
        self.visible_sprites = visible_sprites
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.surface.Surface((self.width, self.height))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.copy().inflate(-25, -25)

    def set_image(self):
        image = self.frames["Attack"][math.floor(self.frame)]
        image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()
        if self.facing == "down":
            image = pygame.transform.rotate(image, 180)
        elif self.facing == "left":
            image = pygame.transform.rotate(image, 90)
        elif self.facing == "right":
            image = pygame.transform.rotate(image, 270)
        self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE))

    def update_frames(self):
        self.frame += self.animation_speed
        if self.frame >= self.number_of_frames:
            self.kill()

    def hit(self) -> None: ...

    def update(self):
        self.set_image()
        self.update_frames()
        self.hit()
