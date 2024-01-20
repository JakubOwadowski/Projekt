import math
from PIL import Image, ImageDraw
import random
from game.settings.settings import TILESIZE, WIDTH, HEIGHT
from game.utils.map_reader import read_map


# Checks if a position is adjacent to already occupied space - so that rooms don't overlap
def touching_other_room(xy, occupied_space):
    x = xy[0]
    y = xy[1]
    if (
            (x - 1, y - 1) in occupied_space or
            (x - 1, y) in occupied_space or
            (x - 1, y + 1) in occupied_space or
            (x, y - 1) in occupied_space or
            (x, y + 1) in occupied_space or
            (x + 1, y - 1) in occupied_space or
            (x + 1, y) in occupied_space or
            (x + 1, y + 1) in occupied_space
    ):
        return True
    return False


# Finds space for a new room so that it connects to these already exiting
def find_space_for_new_room(occupied_space, room_borders, width, height, vertical_connections, horizontal_connections):
    if vertical_connections > horizontal_connections:
        direction = "vertical"
    elif vertical_connections < horizontal_connections:
        direction = "horizontal"
    else:
        direction = random.choice(["horizontal", "vertical"])
    while True:
        (x, y) = random.choice(room_borders)
        space_found = True
        if ((x + 1, y) not in occupied_space
                and (x + 1, y + 1) not in occupied_space
                and (x, y + 1) in occupied_space
                and direction == "horizontal"):
            offset = random.randint(-height + 2, -1)
            for X in range(0, width):
                for Y in range(offset, height):
                    if (x + 1 + X, y + Y) in occupied_space:
                        space_found = False
                        break
            if space_found:
                return ((x + 1, y), (x + 1, y + 1)), (x + 2, y + offset), direction
        if ((x, y + 1) not in occupied_space
                and (x + 1, y + 1) not in occupied_space
                and (x + 1, y) in occupied_space
                and direction == "vertical"):
            offset = random.randint(-width + 2, -1)
            for Y in range(0, height):
                for X in range(offset, height):
                    if (x + X, y + 1 + Y) in occupied_space:
                        space_found = False
                        break
            if space_found:
                return [(x, y + 1), (x + 1, y + 1)], (x + offset, y + 2), direction


# Crops the bitmaps so that the image is as small as possible but still fits on the screen
def crop(ground_bitmap, objects_bitmap, blocking_bitmap, width, height):
    found = False
    bottom = None
    top = None
    right = None
    left = None
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            if ground_bitmap.getpixel((x, y)) == (0, 0, 0):
                left = x
                found = True
                break
        if found:
            break
    found = False
    for x in range(width - 1, 0, -1):
        for y in range(0, height - 1):
            if ground_bitmap.getpixel((x, y)) == (0, 0, 0):
                right = x
                found = True
                break
        if found:
            break
    found = False
    for y in range(0, height - 1):
        for x in range(0, width - 1):
            if ground_bitmap.getpixel((x, y)) == (0, 0, 0):
                top = y
                found = True
                break
        if found:
            break
    found = False
    for y in range(height - 1, 0, -1):
        for x in range(0, width - 1):
            if ground_bitmap.getpixel((x, y)) == (0, 0, 0):
                bottom = y
                found = True
                break
        if found:
            break
    if (bottom + 2) - (top - 1) < HEIGHT // TILESIZE:
        bottom = top + HEIGHT // TILESIZE + 1
    if (right + 2) - (left - 1) < WIDTH // TILESIZE:
        right = left + WIDTH // TILESIZE + 1
    ground_bitmap = ground_bitmap.crop((left - 2, top - 2, right + 2, bottom + 2))
    objects_bitmap = objects_bitmap.crop((left - 2, top - 2, right + 2, bottom + 2))
    blocking_bitmap = blocking_bitmap.crop((left - 2, top - 2, right + 2, bottom + 2))
    return ground_bitmap, objects_bitmap, blocking_bitmap


# Main function to generate a dungeon map. Classy!
def generate_map(
        width=500, height=500, min_size=3, max_size=10, rooms=10, enemies_list=None, map_path="",
        ascend=True, descend=True, map_type="Dungeon", is_random=True):
    if enemies_list is None:
        enemies_list = []
    entities_ref = []
    player_x = 0
    player_y = 0
    if is_random:
        connectors = None
        direction = None
        ground_bitmap = Image.new("RGB", (width, height), (200, 200, 200))
        ground_occupied_space = []
        room_borders = []
        vertical_connections = 0
        horizontal_connections = 0
        ground_draw = ImageDraw.Draw(ground_bitmap)
        first_room = True
        while rooms > 0:
            room_width = random.randint(min_size, max_size)
            room_height = random.randint(min_size, max_size)
            if first_room:
                x = width // 2
                y = height // 2
            else:
                connectors, xy, direction = find_space_for_new_room(ground_occupied_space, room_borders,
                                                                    room_width, room_height, horizontal_connections,
                                                                    vertical_connections)
                x = xy[0]
                y = xy[1]
            if (x, y) not in ground_occupied_space and not touching_other_room((x, y), ground_occupied_space):
                room = []
                for X in range(0, room_width):
                    for Y in range(0, room_height):
                        if ((x + X, y + Y) not in ground_occupied_space
                                and not touching_other_room((x + X, y + Y), ground_occupied_space)
                                and (x + X) < width - 1
                                and (y + Y) < height - 1):
                            room.append((x + X, y + Y))
                            if (x + X == x or
                            x + X == x + room_width - 1 or
                            y + Y == y or
                            y + Y == y + room_height - 1):
                                room_borders.append((x + X, y + Y))
                if not first_room:
                    for connector in connectors:
                        ground_occupied_space.append(connector)
                        ground_draw.point(connector, 'black')
                for xy in room:
                    ground_occupied_space.append(xy)
                    ground_draw.point(xy, 'black')
                if first_room:
                    while True and ascend:
                        xy = random.choice(room)
                        x = xy[0]
                        y = xy[1]
                        if (ground_bitmap.getpixel((x, y)) != (255, 0, 0)
                                and ground_bitmap.getpixel((x - 1, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x - 1, y)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x - 1, y + 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x, y + 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y + 1)) != (200, 200, 200)
                        ):
                            ground_draw.point((x, y), (50, 100, 150))
                            break
                    first_room = False
                if rooms == 1:
                    while True and descend:
                        xy = random.choice(room)
                        x = xy[0]
                        y = xy[1]
                        if (ground_bitmap.getpixel((x, y)) != (255, 0, 0)
                                and ground_bitmap.getpixel((x - 1, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x - 1, y)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x - 1, y + 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x, y + 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y - 1)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y)) != (200, 200, 200)
                                and ground_bitmap.getpixel((x + 1, y + 1)) != (200, 200, 200)
                        ):
                            ground_draw.point((x, y), (150, 100, 50))
                            break
                if direction == "horizontal":
                    horizontal_connections += 1
                elif direction == "vertical":
                    vertical_connections += 1
                rooms -= 1

        objects_bitmap = Image.new("RGB", ground_bitmap.size, 'white')
        objects_draw = ImageDraw.Draw(objects_bitmap)
        for x in range(0, ground_bitmap.size[0]):
            for y in range(0, ground_bitmap.size[1]):
                if (ground_bitmap.getpixel((x, y)) != (0, 0, 0)
                        and ground_bitmap.getpixel((x, y)) != (50, 100, 150)
                        and ground_bitmap.getpixel((x, y)) != (150, 100, 50)):
                    objects_draw.point((x, y), (255, 0, 0))
                if (ground_bitmap.getpixel((x, y)) == (200, 200, 200)
                        and y < ground_bitmap.size[1] - 1
                        and (ground_bitmap.getpixel((x, y + 1)) == (0, 0, 0)
                             or ground_bitmap.getpixel((x, y + 1)) == (50, 100, 150)
                             or ground_bitmap.getpixel((x, y + 1)) == (150, 100, 50)
                        )):
                    objects_draw.point((x, y), (0, 0, 255))

        blocking_bitmap = Image.new("RGB", ground_bitmap.size, 'white')
        blocking_draw = ImageDraw.Draw(blocking_bitmap)
        for x in range(0, blocking_bitmap.size[0]):
            for y in range(0, blocking_bitmap.size[1]):
                if objects_bitmap.getpixel((x, y)) == (255, 0, 0) or objects_bitmap.getpixel((x, y)) == (0, 0, 255):
                    blocking_draw.point((x, y), (255, 0, 0))

        for x in range(1, ground_bitmap.size[0] - 1):
            for y in range(1, ground_bitmap.size[1] - 1):
                if ground_bitmap.getpixel((x - 1, y)) == (200, 200, 200) and ground_bitmap.getpixel((x, y)) == (
                        0, 0, 0):
                    ground_draw.point((x, y), (255, 0, 0))
                if ((ground_bitmap.getpixel((x, y - 1)) == (200, 200, 200)
                     or ground_bitmap.getpixel((x, y - 1)) == (50, 100, 150))
                        and ground_bitmap.getpixel((x, y)) == (0, 0, 0)):
                    ground_draw.point((x, y), (0, 0, 255))
                if (ground_bitmap.getpixel((x, y - 1)) == (200, 200, 200)
                        and ground_bitmap.getpixel((x - 1, y)) == (200, 200, 200)
                        and ground_bitmap.getpixel((x, y)) == (255, 0, 0)):
                    ground_draw.point((x, y), (0, 255, 0))

        ground_bitmap, objects_bitmap, blocking_bitmap = crop(ground_bitmap, objects_bitmap, blocking_bitmap, width,
                                                              height)

        ground_bitmap.save(f"game/maps/{map_path}/ground.bmp")
        objects_bitmap.save(f"game/maps/{map_path}/objects.bmp")
        blocking_bitmap.save(f"game/maps/{map_path}/blocking.bmp")
    else:
        ground_bitmap_list = read_map(f"game/maps/{map_path}/ground.bmp")
        ground_bitmap = Image.new("RGB", (len(ground_bitmap_list[0]), len(ground_bitmap_list)))
        ground_bitmap_flattened = [pixel for row in ground_bitmap_list for pixel in row]
        ground_bitmap.putdata(ground_bitmap_flattened)
        blocking_bitmap_list = read_map(f"game/maps/{map_path}/blocking.bmp")
        blocking_bitmap = Image.new("RGB", (len(blocking_bitmap_list[0]), len(blocking_bitmap_list)))
        blocking_bitmap_flattened = [pixel for row in blocking_bitmap_list for pixel in row]
        blocking_bitmap.putdata(blocking_bitmap_flattened)

    for x in range(1, ground_bitmap.size[0] - 1):
        for y in range(1, ground_bitmap.size[1] - 1):
            if ground_bitmap.getpixel((x, y)) == (50, 100, 150) and map_type == "Dungeon":
                player_x = x + 1
                player_y = y + 1
                entities_ref.append([(player_x, player_y), "player"])
            if ground_bitmap.getpixel((x, y)) == (150, 100, 50) and map_type == "Tower":
                player_x = x + 1
                player_y = y + 1
                entities_ref.append([(player_x, player_y), "player"])

    for enemy in enemies_list:
        while True:
            x = random.randint(0, blocking_bitmap.size[0] - 1)
            y = random.randint(0, blocking_bitmap.size[1] - 1)
            if (blocking_bitmap.getpixel((x, y)) != (255, 0, 0)
                    and math.dist((x, y), (player_x, player_y)) > (enemy["aggro range"] + 50) // TILESIZE):
                entities_ref.append([(x + 1, y + 1), "enemy", enemy])
                break

    return entities_ref
