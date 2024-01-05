from game.generic.map import Map
from game.map_palettes.map_palettes import MapPalettes


class Maps:
    def __init__(self):
        self.test_forest_map = Map(name="Test Forest",
                                   ground_bitmap="game/maps/test_forest/ground.bmp",
                                   objects_bitmap="game/maps/test_forest/objects.bmp",
                                   blocking_bitmap="game/maps/test_forest/blocking.bmp",
                                   entities_bitmap="game/maps/test_forest/entities.bmp",
                                   ground_palette=MapPalettes().forest_palette.ground_palette,
                                   objects_palette=MapPalettes().forest_palette.objects_palette,
                                   blocking_palette=MapPalettes().blocking_palette.blocking_palette,
                                   entities_palette=MapPalettes().entity_palette.entities_palette)
