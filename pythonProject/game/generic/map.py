from game.utils.map_reader import MapReader
from game.settings.settings import *

class Map:
    def __init__(self, name=None,
                 ground_bitmap=None,
                 objects_bitmap=None,
                 entities_bitmap=None,
                 blocking_bitmap=None,
                 ground_palette=None,
                 objects_palette=None,
                 entities_palette=None,
                 blocking_palette=None):
        self.name = name
        self.ground_bitmap = ground_bitmap
        self.objects_bitmap = objects_bitmap
        self.entities_bitmap = entities_bitmap
        self.blocking_bitmap = blocking_bitmap
        self.ground_palette = ground_palette
        self.objects_palette = objects_palette
        self.entities_palette = entities_palette
        self.blocking_palette = blocking_palette
        self.map_reader = MapReader()

    def get_layer(self, map):
        if map == 'ground':
            return self.map_reader.read(self.ground_bitmap)
        elif map == 'objects':
            return self.map_reader.read(self.objects_bitmap)
        elif map == 'entities':
            return self.map_reader.read(self.entities_bitmap)
        elif map == 'blocking':
            return self.map_reader.read(self.blocking_bitmap)
        else:
            return None

    def width(self):
        return len(self.get_layer('ground')[0])*TILESIZE

    def height(self):
        return len(self.get_layer('ground')) * TILESIZE
