from game.map_data.palettes import *
from game.map_data.entities import *
from game.utils.dungeon_generator import generate_map

from game.settings.settings import *
from game.utils.map_reader import read_map


class Map:
    def __init__(self, name=None,
                 ground_bitmap=None,
                 objects_bitmap=None,
                 blocking_bitmap=None,
                 ground_palette=None,
                 objects_palette=None,
                 entities=None,
                 random_map=None,
                 random=True
                 ):
        self.name = name
        self.ground_bitmap = ground_bitmap
        self.objects_bitmap = objects_bitmap
        self.blocking_bitmap = blocking_bitmap
        self.ground_palette = ground_palette
        self.objects_palette = objects_palette
        self.entities = entities
        self.random_map = random_map
        self.random = random

    def get_layer(self, bitmap):
        if bitmap == 'ground':
            return read_map(self.ground_bitmap)
        elif bitmap == 'objects':
            return read_map(self.objects_bitmap)
        elif bitmap == 'blocking':
            return read_map(self.blocking_bitmap)
        else:
            return None

    def width(self):
        return len(self.get_layer('ground')[0]) * TILESIZE

    def height(self):
        return len(self.get_layer('ground')) * TILESIZE

    def randomise(self, ascend):
        if self.random_map is not None:
            self.entities = generate_map(min_size=self.random_map[0],
                                         max_size=self.random_map[1],
                                         rooms=self.random_map[2],
                                         enemies_list=self.random_map[3],
                                         map_path=self.random_map[4],
                                         ascend=self.random_map[5],
                                         descend=self.random_map[6],
                                         map_type="Tower" if ascend else "Dungeon",
                                         is_random=self.random)


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

    "Birchwood Graveyard": Map(
        name="Birchwood Graveyard",
        ground_bitmap="game/maps/birchwood graveyard/ground.bmp",
        objects_bitmap="game/maps/birchwood graveyard/objects.bmp",
        blocking_bitmap="game/maps/birchwood graveyard/blocking.bmp",
        ground_palette=forest_ground_palette,
        objects_palette=forest_objects_palette,
        entities=graveyard_entities
    ),

    "Wilderness": Map(
        name="Wilderness",
        ground_bitmap="game/maps/wilderness/ground.bmp",
        objects_bitmap="game/maps/wilderness/objects.bmp",
        blocking_bitmap="game/maps/wilderness/blocking.bmp",
        ground_palette=forest_ground_palette,
        objects_palette=forest_objects_palette,
        entities=wilderness_entities
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
    ),

    "Graveyard Underground Level 1": Map(
        name="Graveyard Underground Level 1",
        ground_bitmap="game/maps/catacombs 1/ground.bmp",
        objects_bitmap="game/maps/catacombs 1/objects.bmp",
        blocking_bitmap="game/maps/catacombs 1/blocking.bmp",
        ground_palette=catacombs_dungeon_ground_palette,
        objects_palette=catacombs_dungeon_objects_palette,
        entities=[],
        random_map=[3, 6, 10,
                    [mob_hostile_skeleton] * 5 + [mob_hostile_skeleton_warrior],
                    "catacombs 1", True, True]
    ),

    "Graveyard Underground Level 2": Map(
        name="Graveyard Underground Level 2",
        ground_bitmap="game/maps/catacombs 2/ground.bmp",
        objects_bitmap="game/maps/catacombs 2/objects.bmp",
        blocking_bitmap="game/maps/catacombs 2/blocking.bmp",
        ground_palette=catacombs_dungeon_ground_palette,
        objects_palette=catacombs_dungeon_objects_palette,
        entities=[],
        random_map=[3, 6, 10,
                    [mob_hostile_skeleton_warrior] * 5 + [mob_hostile_skeleton],
                    "catacombs 2", True, True]
    ),

    "Graveyard Underground Level 3": Map(
        name="Graveyard Underground Level 3",
        ground_bitmap="game/maps/catacombs 3/ground.bmp",
        objects_bitmap="game/maps/catacombs 3/objects.bmp",
        blocking_bitmap="game/maps/catacombs 3/blocking.bmp",
        ground_palette=catacombs_dungeon_ground_palette,
        objects_palette=catacombs_dungeon_objects_palette,
        entities=[],
        random_map=[3, 6, 10,
                    [mob_hostile_skeleton_warrior] * 10,
                    "catacombs 3", True, True]
    ),

    "Catacombs of Urgash": Map(
        name="Catacombs of Urgash",
        ground_bitmap="game/maps/catacombs 4/ground.bmp",
        objects_bitmap="game/maps/catacombs 4/objects.bmp",
        blocking_bitmap="game/maps/catacombs 4/blocking.bmp",
        ground_palette=red_ground_palette,
        objects_palette=red_objects_palette,
        entities=[],
        random_map=[4, 8, 15,
                    [mob_hostile_skeleton_warrior] * 5 + [mob_hostile_skeleton_knight] * 5,
                    "catacombs 4", True, True]
    ),

    "Royal Tomb": Map(
        name="Royal Tomb",
        ground_bitmap="game/maps/catacombs 5/ground.bmp",
        objects_bitmap="game/maps/catacombs 5/objects.bmp",
        blocking_bitmap="game/maps/catacombs 5/blocking.bmp",
        ground_palette=purple_red_ground_palette,
        objects_palette=purple_objects_palette,
        entities=[],
        random_map=[6, 12, 5,
                    [mob_hostile_skeleton_king],
                    "catacombs 5", True, False]
    ),

    "Birchwood Underground Level 1": Map(
        name="Birchwood Underground Level 1",
        ground_bitmap="game/maps/birchwood dungeon 1/ground.bmp",
        objects_bitmap="game/maps/birchwood dungeon 1/objects.bmp",
        blocking_bitmap="game/maps/birchwood dungeon 1/blocking.bmp",
        ground_palette=catacombs_dungeon_ground_palette,
        objects_palette=dirt_dungeon_objects_palette,
        entities=[],
        random_map=[4, 5, 10,
                    [mob_hostile_goblin] * 7,
                    "birchwood dungeon 1", True, True]
    ),
    "Birchwood Underground Level 2": Map(
        name="Birchwood Underground Level 2",
        ground_bitmap="game/maps/birchwood dungeon 2/ground.bmp",
        objects_bitmap="game/maps/birchwood dungeon 2/objects.bmp",
        blocking_bitmap="game/maps/birchwood dungeon 2/blocking.bmp",
        ground_palette=catacombs_dungeon_ground_palette,
        objects_palette=dirt_dungeon_objects_palette,
        entities=[],
        random_map=[4, 5, 10,
                    [mob_hostile_goblin] * 5 + [mob_hostile_imp] * 2,
                    "birchwood dungeon 2", True, True]
    ),
    "Hidden Dungeon Level 1": Map(
        name="Hidden Dungeon Level 1",
        ground_bitmap="game/maps/birchwood dungeon 3/ground.bmp",
        objects_bitmap="game/maps/birchwood dungeon 3/objects.bmp",
        blocking_bitmap="game/maps/birchwood dungeon 3/blocking.bmp",
        ground_palette=blue_ground_palette,
        objects_palette=blue_objects_palette,
        entities=[],
        random_map=[4, 5, 10,
                    [mob_hostile_devil] * 8 + [mob_hostile_imp] * 3 + [mob_hostile_skeleton_knight] * 2,
                    "birchwood dungeon 3", True, True]
    ),

    "Hidden Dungeon Level 2": Map(
        name="Hidden Dungeon Level 2",
        ground_bitmap="game/maps/birchwood dungeon 4/ground.bmp",
        objects_bitmap="game/maps/birchwood dungeon 4/objects.bmp",
        blocking_bitmap="game/maps/birchwood dungeon 4/blocking.bmp",
        ground_palette=blue_ground_palette,
        objects_palette=blue_objects_palette,
        entities=[],
        random_map=[4, 5, 10,
                    [mob_hostile_devil] * 10 + [mob_hostile_skeleton_knight] * 4,
                    "birchwood dungeon 4", True, True]
    ),
    "Cyclops Lair": Map(
        name="Cyclops Lair",
        ground_bitmap="game/maps/birchwood dungeon 5/ground.bmp",
        objects_bitmap="game/maps/birchwood dungeon 5/objects.bmp",
        blocking_bitmap="game/maps/birchwood dungeon 5/blocking.bmp",
        ground_palette=blue_ground_palette,
        objects_palette=dirt_dungeon_objects_palette,
        entities=[],
        random_map=[30, 30, 1,
                    [mob_hostile_cyclops],
                    "birchwood dungeon 5", True, False]
    ),
}
