import math

import pygame.event

import game.sprites.entities.entity
from game.events import GAMEOVER
from game.memory import memory
from game.sprites.attacks.player.slash_attack_player import SlashAttackPlayer
from game.settings.settings import *


class Player(game.sprites.entities.entity.Entity):
    def __init__(self, position, groups, obstacle_sprites, visible_sprites, data):
        super().__init__(position, groups, obstacle_sprites, [
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
        ], data)
        self.dying_frame = 0
        self.invulnerable_cooldown = 300
        self.hit_direction = None
        self.invulnerable_time = 0
        self.invulnerable = False
        self.sprite_type = "player"
        self.attack_time = 0
        self.attacking = False
        self.playing_attack_anim = False
        self.attack_cooldown = 300
        self.visible_sprites = visible_sprites
        self.idle_animation_speed = 0
        self.idle_frame = 0
        self.moving_animation_speed = 0.10
        self.moving_frame = 0
        self.attack_animation_speed = 0.2
        self.attack_frame = 0

        self.groups = groups
        self.current_fury = memory["player"]["fury"]
        self.max_fury = data["max fury"]
        self.level = memory["player"]["lvl"]
        self.exp = memory["player"]["exp"]
        self.next_level = memory["player"]["next lvl"]
        self.current_health = memory["player"]["hp"]
        self.base_health = memory["player"]["base hp"]

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
            self.attack()

    def attack(self):
        self.attacking = True
        self.playing_attack_anim = True
        self.attack_time = pygame.time.get_ticks()
        if self.facing == "up":
            SlashAttackPlayer((self.rect.topleft[0], self.rect.topleft[1] - 64), self.facing, self.groups,
                              self.visible_sprites, self)
        elif self.facing == "down":
            SlashAttackPlayer((self.rect.topleft[0], self.rect.topleft[1] + 64), self.facing, self.groups,
                              self.visible_sprites, self)
        elif self.facing == "left":
            SlashAttackPlayer((self.rect.topleft[0] - 64, self.rect.topleft[1]), self.facing, self.groups,
                              self.visible_sprites, self)
        elif self.facing == "right":
            SlashAttackPlayer((self.rect.topleft[0] + 64, self.rect.topleft[1]), self.facing, self.groups,
                              self.visible_sprites, self)

    def damage(self, enemy_strength, hit_direction):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
            attack_strength = (enemy_strength - self.defence)
            if attack_strength > 0:
                self.current_health -= attack_strength
            self.hit_direction = hit_direction

    def die(self):
        self.alive = False

    def grant_exp(self, exp):
        self.exp += exp

        # level up
        if self.exp >= self.next_level:
            self.level += 1
            self.exp = 0
            self.base_health *= 1.5
            self.current_health = self.base_health
            self.next_level *= 1.7
            self.strength += 2

    def update_frames(self):
        if self.alive:
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
        elif self.dying_frame <= 3:
            self.dying_frame += 0.2
        elif self.dying_frame > 3:
            pygame.event.post(pygame.event.Event(GAMEOVER))

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and not pygame.key.get_pressed()[KEY_ATTACK]:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        if current_time - self.invulnerable_time >= self.invulnerable_cooldown and self.invulnerable:
            self.invulnerable = False

    def set_image(self):
        if self.alive:
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
        else:
            image = self.frames["Dying"][math.floor(self.dying_frame)]
        self.image = pygame.transform.scale(pygame.image.fromstring(
            image.tobytes(),
            image.size,
            image.mode).convert_alpha(),
                                            (64, 64))

    def update(self):
        if self.current_health <= 0 and self.alive:
            self.die()
        if self.alive:
            self.input()
            self.cooldowns()
            if self.invulnerable:
                if self.hit_direction == "right":
                    self.direction = pygame.Vector2(1, 0)
                elif self.hit_direction == "left":
                    self.direction = pygame.Vector2(-1, 0)
                elif self.hit_direction == "up":
                    self.direction = pygame.Vector2(0, -1)
                elif self.hit_direction == "down":
                    self.direction = pygame.Vector2(0, 1)
                self.move(5)
            if not self.playing_attack_anim and not self.invulnerable:
                self.move(self.speed)
            self.current_fury -= self.data["fury decay"]
            if self.current_fury < 0:
                self.current_fury = 0
        self.update_frames()
        self.set_image()
