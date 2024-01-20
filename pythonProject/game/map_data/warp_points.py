from game.maps.maps import Maps

# Hardcoded. Add new warp points in ONLY these arrays!
warp_points = [
    [Maps["Forest West"], (41, 13), Maps["Forest East"], (1, 14)],
    [Maps["Forest West"], (41, 15), Maps["Forest East"], (1, 15)],
    [Maps["Forest West"], (41, 16), Maps["Forest East"], (1, 16)],
    [Maps["Forest West"], (41, 16), Maps["Forest East"], (1, 16)],
    [Maps["Forest West"], (41, 17), Maps["Forest East"], (1, 16)],
    [Maps["Forest East"], (-1, 13), Maps["Forest West"], (39, 14)],
    [Maps["Forest East"], (-1, 14), Maps["Forest West"], (39, 14)],
    [Maps["Forest East"], (-1, 15), Maps["Forest West"], (39, 15)],
    [Maps["Forest East"], (-1, 16), Maps["Forest West"], (39, 16)],
    [Maps["Forest East"], (-1, 17), Maps["Forest West"], (39, 16)],

    [Maps["Birchwood"], (10, 14), Maps["Birchwood Graveyard"], (7, 1)],
    [Maps["Birchwood"], (11, 14), Maps["Birchwood Graveyard"], (8, 1)],
    [Maps["Birchwood"], (12, 14), Maps["Birchwood Graveyard"], (9, 1)],
    [Maps["Birchwood Graveyard"], (7, -1), Maps["Birchwood"], (10, 13)],
    [Maps["Birchwood Graveyard"], (8, -1), Maps["Birchwood"], (11, 13)],
    [Maps["Birchwood Graveyard"], (9, -1), Maps["Birchwood"], (12, 13)],

    [Maps["Birchwood"], (10, -1), Maps["Wilderness"], (39, 50)],
    [Maps["Birchwood"], (11, -1), Maps["Wilderness"], (40, 50)],
    [Maps["Wilderness"], (39, 51), Maps["Birchwood"], (10, 1)],
    [Maps["Wilderness"], (40, 51), Maps["Birchwood"], (11, 1)]
]

stairs_down = [
    [Maps["Birchwood Graveyard"], (11, 7), Maps["Graveyard Underground Level 1"]],
    [Maps["Birchwood"], (11, 7), Maps["Birchwood Underground Level 1"]]
]

stairs_up = [

]

stairs_random = [
    [Maps["Graveyard Underground Level 1"], Maps["Graveyard Underground Level 2"]],
    [Maps["Graveyard Underground Level 2"], Maps["Graveyard Underground Level 3"]],
    [Maps["Graveyard Underground Level 3"], Maps["Catacombs of Urgash"]],
    [Maps["Catacombs of Urgash"], Maps["Royal Tomb"]],

    [Maps["Birchwood Underground Level 1"], Maps["Birchwood Underground Level 2"]],
    [Maps["Birchwood Underground Level 2"], Maps["Hidden Dungeon Level 1"]],
    [Maps["Hidden Dungeon Level 1"], Maps["Hidden Dungeon Level 2"]],
    [Maps["Hidden Dungeon Level 2"], Maps["Cyclops Lair"]],
]
