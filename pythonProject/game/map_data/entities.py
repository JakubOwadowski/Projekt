from game.mobs.hostiles import *

# Player is hardcoded to ALWAYS use mob_player!

forest_entities = [
    [(3, 3), "player"],
    [(28, 3), "enemy", mob_hostile_evil_dummy],
    [(12, 7), "enemy", mob_hostile_evil_dummy],
    [(16, 12), "enemy", mob_hostile_evil_dummy],
    [(7, 17), "enemy", mob_hostile_evil_dummy],
    [(33, 17), "enemy", mob_hostile_evil_dummy],
    [(15, 15), "enemy", mob_hostile_super_evil_dummy],

]

forest_2_entities = [
    [(3, 3), "player"],
    [(15, 15), "enemy", mob_hostile_super_evil_dummy],
    [(16, 15), "enemy", mob_hostile_super_evil_dummy],
    [(17, 15), "enemy", mob_hostile_super_evil_dummy],
]