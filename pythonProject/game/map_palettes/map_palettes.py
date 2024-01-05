from game.generic.palette import Palette


class MapPalettes():
    def __init__(self):
        self.forest_palette = Palette(
            ground_palette={
                (0, 255, 0): "game/graphics/ground_tiles/grass_tile_1.png",
                (255, 0, 0): "game/graphics/ground_tiles/grass_tile_2.png",
                (0, 0, 255): "game/graphics/ground_tiles/grass_tile_3.png",
                (255, 255, 0): "game/graphics/ground_tiles/grass_tile_4.png",
                (255, 0, 255): "game/graphics/ground_tiles/grass_tile_5.png",
            },
            objects_palette={
                (0, 255, 0): "game/graphics/map_objects_tiles/tree.png"
            }
        )

        self.entity_palette = Palette(
            entities_palette={
                (0, 255, 0): "game/graphics/map_objects_tiles/dummy.png"
            }
        )

        self.blocking_palette = Palette(
            blocking_palette={
                (255, 0, 0): "game/graphics/misc/tile_hitbox.png"
            }
        )

