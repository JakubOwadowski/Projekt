from game.mobs.hostiles import *

# Player is hardcoded to ALWAYS use mob_player!

birchwood_entities = [
    [(11, 7), "player"]
]

forest_entities = [
    [(3, 3), "player"],
    [(28, 3), "enemy", mob_hostile_evil_dummy],
    [(12, 7), "enemy", mob_hostile_evil_dummy],
    [(16, 12), "enemy", mob_hostile_evil_dummy],
    [(7, 17), "enemy", mob_hostile_evil_dummy],
    [(33, 17), "enemy", mob_hostile_evil_dummy]

]

forest_2_entities = [
    [(3, 3), "player"]
]

wilderness_entities = [
    [(35, 39), "enemy", mob_hostile_bandit],
    [(6, 6), "enemy", mob_hostile_bandit],
    [(46, 10), "enemy", mob_hostile_bandit],
    [(35, 28), "enemy", mob_hostile_bandit],
    [(48, 38), "enemy", mob_hostile_bandit],
    [(16, 38), "enemy", mob_hostile_bandit],
    [(12, 38), "enemy", mob_hostile_bandit],
    [(31, 22), "enemy", mob_hostile_bandit],
    [(31, 22), "enemy", mob_hostile_bandit],
    [(24, 9), "enemy", mob_hostile_bandit],
    [(14, 24), "enemy", mob_hostile_bandit],
    [(41, 25), "enemy", mob_hostile_bandit],
]

graveyard_entities = [
    [(9, 18), "enemy", mob_hostile_skeleton],
    [(8, 10), "enemy", mob_hostile_skeleton],
    [(14, 5), "enemy", mob_hostile_skeleton],
]
