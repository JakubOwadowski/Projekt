import pygame.sprite
import game.sprites.attacks.generic_attack


class SlashAttackEnemy(game.sprites.attacks.generic_attack.GenericAttack):
    def __init__(self, position, facing, groups, visible_sprites, enemy_strength):
        super().__init__(position, "game/graphics/attacks/slash_attack.png", facing, groups, visible_sprites)
        self.enemy_strength = enemy_strength

    def hit(self):
        player = [sprite for sprite in self.visible_sprites if
                  hasattr(sprite, "sprite_type")
                  and sprite.sprite_type == "player"][0]
        if player.hitbox.colliderect(self.rect):
            player.damage(self.enemy_strength, self.facing)
