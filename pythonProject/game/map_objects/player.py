import pygame
from game.settings.settings import *
from game.utils.image_splitter import ImageSplitter


class Player(pygame.sprite.Sprite):
    def __init__(self, image, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.frames = ImageSplitter().split(image)
        self.image = pygame.transform.scale(
            pygame.image.fromstring(self.frames["Idle left"][0].tobytes(), self.frames["Idle left"][0].size,
                                    self.frames["Idle left"][0].mode).convert_alpha(),
            (64, 64))
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()
        self.facing = "down"
        self.obstacle_sprites = obstacle_sprites
        self.attacking = False
        self.playing_attack_anim = False
        self.attack_time = 0
        self.attack_cooldown = 300
        self.idle_prev_frame = 0
        self.idle_next_frame = 500
        self.idle_frame = 0
        self.moving_prev_frame = 0
        self.moving_next_frame = 100
        self.moving_frame = 0
        self.attack_prev_frame = 0
        self.attack_next_frame = 50
        self.attack_frame = 0
        self.hits = 0

    def input(self):
        keys = pygame.key.get_pressed()
        pygame.key.set_repeat(0)

        if keys[KEY_LEFT]:
            self.direction.x = -1
            self.facing = "left"
        elif keys[KEY_RIGHT]:
            self.direction.x = 1
            self.facing = "right"
        else:
            self.direction.x = 0
        if keys[KEY_UP]:
            self.direction.y = -1
            self.facing = "up"
        elif keys[KEY_DOWN]:
            self.direction.y = 1
            self.facing = "down"
        else:
            self.direction.y = 0

        if keys[KEY_ATTACK] and not self.attacking:
            self.attacking = True
            self.playing_attack_anim = True
            self.attack_time = pygame.time.get_ticks()


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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and not pygame.key.get_pressed()[KEY_ATTACK]:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if current_time - self.idle_prev_frame >= self.idle_next_frame:
            self.idle_prev_frame = current_time
            self.idle_frame += 1
            if self.idle_frame >= 4:
                self.idle_frame = 0
        if current_time - self.moving_prev_frame >= self.moving_next_frame:
            self.moving_prev_frame = current_time
            self.moving_frame += 1
            if self.moving_frame >= 4:
                self.moving_frame = 0
        if current_time - self.attack_prev_frame >= self.attack_next_frame and self.playing_attack_anim:
            self.attack_prev_frame = current_time
            self.attack_frame += 1
            if self.attack_frame >= 4:
                self.playing_attack_anim = False
                self.attack_frame = 0

    def set_image(self):
        if self.attacking and self.playing_attack_anim:  # Attacking
            if self.facing == "up":
                image = self.frames["Attack up"][self.attack_frame]
            elif self.facing == "down":
                image = self.frames["Attack down"][self.attack_frame]
            elif self.facing == "left":
                image = self.frames["Attack left"][self.attack_frame]
            elif self.facing == "right":
                image = self.frames["Attack right"][self.attack_frame]
        elif self.direction.x == 0 and self.direction.y == 0:  # Idle
            if self.facing == "up":
                image = self.frames["Idle up"][self.idle_frame]
            elif self.facing == "down":
                image = self.frames["Idle down"][self.idle_frame]
            elif self.facing == "left":
                image = self.frames["Idle left"][self.idle_frame]
            elif self.facing == "right":
                image = self.frames["Idle right"][self.idle_frame]
        elif self.direction.x != 0 or self.direction.y != 0:  # Moving
            if self.facing == "up":
                image = self.frames["Moving up"][self.moving_frame]
            elif self.facing == "down":
                image = self.frames["Moving down"][self.moving_frame]
            elif self.facing == "left":
                image = self.frames["Moving left"][self.moving_frame]
            elif self.facing == "right":
                image = self.frames["Moving right"][self.moving_frame]
        self.image = pygame.transform.scale(pygame.image.fromstring(
            image.tobytes(),
            image.size,
            image.mode).convert_alpha(),
                                            (64, 64))

    def update(self):
        self.input()
        self.set_image()
        self.cooldowns()
        self.move(8)
