import pygame

from game.settings.settings import TILESIZE
from game.utils.image_splitter import split


class GenericEntity(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites, visible_sprites, data):
        super().__init__(*groups)
        self.data = data
        self.frame_sets = [
            "Idle down",
            "Idle up",
            "Idle left",
            "Idle right",
            "Moving down",
            "Moving up",
            "Moving left",
            "Moving right",
            "Attack down",
            "Attack up",
            "Attack left",
            "Attack right",
            "Dying"
        ]
        self.number_of_frames = 4
        self.frames = split(data["graphics"], self.number_of_frames, self.frame_sets)
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.surface.Surface((self.width, self.height))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, 0)
        self.direction = pygame.math.Vector2()
        self.facing = "down"
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.name = data["name"]
        self.base_health = data["health"]
        self.current_health = self.base_health
        self.allegiance = data["allegiance"]
        self.strength = data["strength"]
        self.defence = data["defence"]
        self.speed = data["speed"]
        self.alive = True
        self.groups = groups

        self.dying_animation_frame = 0
        self.dying_animation_frames = 4
        self.dying_animation_speed = 0.2

        self.idle_animation_frame = 0
        self.idle_animation_frames = 4
        self.idle_animation_speed = 0.01

        self.moving_animation_frame = 0
        self.moving_animation_frames = 4
        self.moving_animation_speed = 0.10

        self.attack_animation_frame = 0
        self.attack_animation_frames = 4
        self.attack_animation_speed = 0.2

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def die(self, *args):
        self.alive = False
