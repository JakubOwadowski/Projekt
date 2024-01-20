from PIL import Image


def read_map(path_to_map):
    with Image.open(path_to_map) as bitmap:
        bitmap = bitmap.convert("RGB")
        pixel_data = list(bitmap.getdata())
        width, height = bitmap.size
        map = [pixel_data[i * width:(i + 1) * width] for i in range(height)]
    return map

