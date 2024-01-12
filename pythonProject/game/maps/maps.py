from game.map_data.palettes import *
from game.map_data.entities import *

from game.utils.map_reader import MapReader
from game.settings.settings import *


class Map:
    def __init__(self, name=None,
                 ground_bitmap=None,
                 objects_bitmap=None,
                 blocking_bitmap=None,
                 ground_palette=None,
                 objects_palette=None,
                 entities=None,
                 ):
        self.name = name
        self.ground_bitmap = ground_bitmap
        self.objects_bitmap = objects_bitmap
        self.blocking_bitmap = blocking_bitmap
        self.ground_palette = ground_palette
        self.objects_palette = objects_palette
        self.entities = entities
        self.map_reader = MapReader()

    def get_layer(self, bitmap):
        if bitmap == 'ground':
            return self.map_reader.read(self.ground_bitmap)
        elif bitmap == 'objects':
            return self.map_reader.read(self.objects_bitmap)
        elif bitmap == 'blocking':
            return self.map_reader.read(self.blocking_bitmap)
        else:
            return None

    def width(self):
        return len(self.get_layer('ground')[0]) * TILESIZE

    def height(self):
        return len(self.get_layer('ground')) * TILESIZE


# Important - the key and the name must be the same!
Maps = {
    "Birchwood": Map(
        name="Birchwood",
        ground_bitmap="game/maps/birchwood/ground.bmp",
        objects_bitmap="game/maps/birchwood/objects.bmp",
        blocking_bitmap="game/maps/birchwood/blocking.bmp",
        ground_palette=forest_ground_palette,
        objects_palette=forest_objects_palette,
        entities=birchwood_entities
    ),

    "Forest East": Map(
        name="Forest East",
        ground_bitmap="game/maps/test_forest/ground.bmp",
        objects_bitmap="game/maps/test_forest/objects.bmp",
        blocking_bitmap="game/maps/test_forest/blocking.bmp",
        ground_palette=forest_ground_palette,
        objects_palette=forest_objects_palette,
        entities=forest_entities
    ),
    "Forest West": Map(
        name="Forest West",
        ground_bitmap="game/maps/test_forest 2/ground.bmp",
        objects_bitmap="game/maps/test_forest 2/objects.bmp",
        blocking_bitmap="game/maps/test_forest 2/blocking.bmp",
        ground_palette=forest_ground_palette,
        objects_palette=forest_objects_palette,
        entities=forest_2_entities
    )
}
