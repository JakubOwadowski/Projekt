import pygame
from game.utils.image_splitter import ImageSplitter


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, position, groups, obstacle_sprites, frame_sets):
        super().__init__(groups)
        self.frames = ImageSplitter().split(image, 4, frame_sets)
        self.image = pygame.surface.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()
        self.facing = "down"
        self.obstacle_sprites = obstacle_sprites

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

