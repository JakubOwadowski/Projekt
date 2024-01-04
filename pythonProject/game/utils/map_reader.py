from PIL import Image


class MapReader:
    def __init__(self):
        pass

    def read(self, path_to_map):
        with Image.open(path_to_map) as bitmap:
            bitmap = bitmap.convert("RGB")
            pixel_data = list(bitmap.getdata())
            width, height = bitmap.size
            map = [pixel_data[i * width:(i + 1) * width] for i in range(height)]

            for i in range(0, height):
                for j in range(0, width):
                    if map[i][j] == (0,0,0):
                        map[i][j] = 'x'
                    elif map[i][j] == (255,255,255):
                        map[i][j] = ' '
                    elif map[i][j] == (34,177,76):
                        map[i][j] = 'p'

        return map
