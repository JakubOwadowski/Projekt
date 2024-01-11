import math
import random

import pygame.time

from game.settings.settings import *
import game.sprites.entities.entity
from game.sprites.attacks.enemy.slash_attack_enemy import SlashAttackEnemy


class Enemy(game.sprites.entities.entity.Entity):
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
        self.attack_time = 0
        self.sprite_type = "enemy"
        self.attacking = False
        self.playing_attack_anim = False
        self.attack_cooldown = 500
        self.idle_cooldown = 200
        self.idle_time = 0
        self.idle_wait_cooldown = 2000
        self.idle_wait_time = 0
        self.idle_wait = False
        self.invulnerable_cooldown = 300
        self.invulnerable_time = 0
        self.invulnerable = False
        self.visible_sprites = visible_sprites
        self.idle_animation_speed = 0
        self.idle_frame = 0
        self.moving_animation_speed = 0.10
        self.moving_frame = 0
        self.attack_animation_speed = 0.2
        self.attack_frame = 0
        self.groups = groups

        self.exp = data["exp"]
        self.ai = data["ai"]
        self.attack_range = data["attack range"]
        self.aggro_range = data["aggro range"]
        self.hit_direction = None
        self.state = "idle"

    def attack(self):
        self.attacking = True
        self.playing_attack_anim = True
        self.attack_time = pygame.time.get_ticks()
        if self.facing == "up":
            SlashAttackEnemy((self.rect.topleft[0], self.rect.topleft[1] - 64), self.facing, self.groups, self.visible_sprites, self.strength)
        elif self.facing == "down":
            SlashAttackEnemy((self.rect.topleft[0], self.rect.topleft[1] + 64), self.facing, self.groups, self.visible_sprites, self.strength)
        elif self.facing == "left":
            SlashAttackEnemy((self.rect.topleft[0] - 64, self.rect.topleft[1]), self.facing, self.groups, self.visible_sprites, self.strength)
        elif self.facing == "right":
            SlashAttackEnemy((self.rect.topleft[0] + 64, self.rect.topleft[1]), self.facing, self.groups, self.visible_sprites, self.strength)

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

    def decide_action(self, player):
        self_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - self_vector).magnitude()
        if distance > 0:
            direction = (player_vector - self_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        if distance <= self.attack_range:
            self.state = "attack"
            if not self.attacking:
                self.attack()
        elif distance <= self.aggro_range and self.ai == "Rush":
            self.direction = direction
            self.get_facing()
            self.state = "aggro"
        else:
            self.state = "idle"

    def get_facing(self):
        if self.direction.y < 0:
            self.facing = "up"
        elif self.direction.y > 0:
            self.facing = "down"
        if self.direction.x > 0.75:
            self.facing = "right"
        elif self.direction.x < -0.75:
            self.facing = "left"

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and not self.state == "attack":
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if current_time - self.idle_time >= self.idle_cooldown and self.idle_wait:
            self.idle_wait_time = current_time
            self.direction = pygame.math.Vector2()
            self.idle_wait = False
        elif current_time - self.idle_wait_time >= self.idle_wait_cooldown and not self.idle_wait and self.state == "idle":
            self.idle_time = current_time
            self.direction = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
            self.get_facing()
            self.idle_wait = True

        if current_time - self.invulnerable_time >= self.invulnerable_cooldown and self.invulnerable:
            self.invulnerable = False

    def damage(self, attacker_strength, hit_direction, player):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
            attack_strength = (attacker_strength - self.defence)
            if attack_strength > 0:
                self.current_health -= attack_strength
            self.hit_direction = hit_direction
            player.current_fury += 10
            if player.current_fury > player.max_fury:
                player.current_fury = player.max_fury

    def player_collision(self, player):
        if player.hitbox.colliderect(self.hitbox) and not player.invulnerable:
            player.damage(self.strength // 2, self.facing)

    def die(self, player):
        player.grant_exp(self.exp)
        self.alive = False

    def update(self):
        self.cooldowns()
        if self.alive:
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
                if not self.idle_wait and self.state == "idle":
                    self.direction = pygame.Vector2()
                self.move(self.speed)
        self.update_frames()
        self.set_image()

    def enemy_update(self, player):
        if self.alive:
            self.decide_action(player)
        if self.current_health <= 0 and self.alive:
            self.die(player)
        if self.alive:
            self.player_collision(player)
