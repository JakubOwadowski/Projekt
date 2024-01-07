import math

import game.map_objects.entities.entity
from game.map_objects.misc.slash_blur import SlashBlur
from game.settings.settings import *


class Player(game.map_objects.entities.entity.Entity):
    def __init__(self, image, position, groups, obstacle_sprites):
        super().__init__(image, position, groups, obstacle_sprites, [
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
            "Attack right"
        ])
        self.attacking = False
        self.playing_attack_anim = False
        self.attack_cooldown = 300

        self.idle_animation_speed = 0
        self.idle_frame = 0
        self.moving_animation_speed = 0.10
        self.moving_frame = 0
        self.attack_animation_speed = 0.2
        self.attack_frame = 0

        self.groups = groups
        self.base_stats = {
            "health": 100,
            "strength": 10,
            "speed": 10,
            "fury": 0,
            "max fury": 100,
            "level": 1,
            "experience": 0,
            "next level": 100
        }
        self.current_stats = self.base_stats

    def input(self):
        keys = pygame.key.get_pressed()
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
            if self.facing == "up":
                SlashBlur((self.rect.topleft[0], self.rect.topleft[1] - 96), self.facing, self.groups)
            elif self.facing == "down":
                SlashBlur((self.rect.topleft[0], self.rect.topleft[1] + 96), self.facing, self.groups)
            elif self.facing == "left":
                SlashBlur((self.rect.topleft[0] - 96, self.rect.topleft[1]), self.facing, self.groups)
            elif self.facing == "right":
                SlashBlur((self.rect.topleft[0] + 96, self.rect.topleft[1]), self.facing, self.groups)

    def update_frames(self):
        self.idle_frame += self.idle_animation_speed
        if self.idle_frame >= 4:
            self.idle_frame = 0
        self.moving_frame += self.moving_animation_speed
        if self.moving_frame >= 4:
            self.moving_frame = 0
        if self.playing_attack_anim:
            self.attack_frame += self.attack_animation_speed
            if self.attack_frame >= 4:
                self.attack_frame = 0
                self.playing_attack_anim = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and not pygame.key.get_pressed()[KEY_ATTACK]:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    def set_image(self):
        if self.attacking and self.playing_attack_anim:  # Attacking
            if self.facing == "up":
                image = self.frames["Attack up"][math.floor(self.attack_frame)]
            elif self.facing == "down":
                image = self.frames["Attack down"][math.floor(self.attack_frame)]
            elif self.facing == "left":
                image = self.frames["Attack left"][math.floor(self.attack_frame)]
            elif self.facing == "right":
                image = self.frames["Attack right"][math.floor(self.attack_frame)]
        elif self.direction.x == 0 and self.direction.y == 0:  # Idle
            if self.facing == "up":
                image = self.frames["Idle up"][math.floor(self.idle_frame)]
            elif self.facing == "down":
                image = self.frames["Idle down"][math.floor(self.idle_frame)]
            elif self.facing == "left":
                image = self.frames["Idle left"][math.floor(self.idle_frame)]
            elif self.facing == "right":
                image = self.frames["Idle right"][math.floor(self.idle_frame)]
        elif self.direction.x != 0 or self.direction.y != 0:  # Moving
            if self.facing == "up":
                image = self.frames["Moving up"][math.floor(self.moving_frame)]
            elif self.facing == "down":
                image = self.frames["Moving down"][math.floor(self.moving_frame)]
            elif self.facing == "left":
                image = self.frames["Moving left"][math.floor(self.moving_frame)]
            elif self.facing == "right":
                image = self.frames["Moving right"][math.floor(self.moving_frame)]
        self.image = pygame.transform.scale(pygame.image.fromstring(
            image.tobytes(),
            image.size,
            image.mode).convert_alpha(),
                                            (64, 64))

    def update(self):
        self.input()
        self.cooldowns()
        self.update_frames()
        self.set_image()
        if not self.playing_attack_anim:
            self.move(self.base_stats["speed"])
