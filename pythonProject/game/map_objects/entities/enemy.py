import math
import random

from game.settings.settings import *
import game.map_objects.entities.entity


class Enemy(game.map_objects.entities.entity.Entity):
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
        self.sprite_type = "enemy"
        self.attacking = False
        self.playing_attack_anim = False
        self.attack_cooldown = 300
        self.idle_cooldown = 200
        self.idle_time = 0
        self.idle_wait_cooldown = 2000
        self.idle_wait_time = 0
        self.idle_wait = False

        self.idle_animation_speed = 0
        self.idle_frame = 0
        self.moving_animation_speed = 0.10
        self.moving_frame = 0
        self.attack_animation_speed = 0.2
        self.attack_frame = 0

        self.base_stats = {
            "name": "Evil Dummy",
            "health": 30,
            "strength": 10,
            "exp": 10,
            "speed": 3,
            "attack range": 100,
            "aggro range": 400
        }
        self.current_stats = self.base_stats

        self.groups = groups

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

    def decide_action(self, player):
        self_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - self_vector).magnitude()
        if distance > 0:
            direction = (player_vector - self_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        if distance <= self.base_stats["attack range"]:
            print("attack")
        elif distance <= self.base_stats["aggro range"]:
            self.direction = direction
            self.get_facing()

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

        if current_time - self.idle_time >= self.idle_cooldown and self.idle_wait:
            self.idle_wait_time = current_time
            self.direction = pygame.math.Vector2()
            self.idle_wait = False
        elif current_time - self.idle_wait_time >= self.idle_wait_cooldown and not self.idle_wait:
            self.idle_time = current_time
            self.direction = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
            self.get_facing()
            self.idle_wait = True

    def update(self):
        self.cooldowns()
        self.update_frames()
        self.set_image()
        if not self.playing_attack_anim:
            self.move(self.base_stats["speed"])

    def enemy_update(self, player):
        self.decide_action(player)