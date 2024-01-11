import pygame.sprite
from game.utils.image_splitter import ImageSplitter


class SlashAttackEnemy(pygame.sprite.Sprite):
    def __init__(self, position, facing, groups, visible_sprites, enemy_strength):
        super().__init__(groups)
        self.frames = ImageSplitter().split("game/graphics/attacks/slash_attack.png", 7,
                                            ["Down", "Up", "Left", "Right"])
        self.prev_frame = 0
        self.next_frame = 15
        self.frame = 0
        self.facing = facing
        self.visible_sprites = visible_sprites
        self.enemy_strength = enemy_strength
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

    def hit(self):
        player = [sprite for sprite in self.visible_sprites if
                  hasattr(sprite, "sprite_type")
                  and sprite.sprite_type == "player"][0]
        if player.hitbox.colliderect(self.rect):
            player.damage(self.enemy_strength, self.facing)

    def update(self):
        self.set_image()
        self.cooldowns()
        self.hit()
