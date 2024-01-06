from game.generic.map import Map
from game.map_palettes.map_palettes import *

test_forest_map = Map(name="Test Forest",
                      ground_bitmap="game/maps/test_forest/ground.bmp",
                      objects_bitmap="game/maps/test_forest/objects.bmp",
                      blocking_bitmap="game/maps/test_forest/blocking.bmp",
                      entities_bitmap="game/maps/test_forest/entities.bmp",
                      ground_palette=forest_ground_palette,
                      objects_palette=forest_objects_palette,
                      blocking_palette=blocking_palette,
                      entities_palette=entity_palette)
