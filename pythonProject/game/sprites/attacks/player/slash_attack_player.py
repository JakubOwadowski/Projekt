import math
import game.sprites.attacks.generic_attack


class SlashAttackPlayer(game.sprites.attacks.generic_attack.GenericAttack):
    def __init__(self, position, facing, groups, visible_sprites, player):
        super().__init__(position, "game/graphics/attacks/slash_attack.png", facing, groups, visible_sprites)
        self.player = player

    def hit(self):
        enemy_sprites = [sprite for sprite in self.visible_sprites if
                         hasattr(sprite, "sprite_type")
                         and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            if enemy.hitbox.colliderect(self.hitbox):
                enemy.damage(self.player.strength + self.player.strength * self.player.current_fury / 100, self.facing,
                             self.player)
