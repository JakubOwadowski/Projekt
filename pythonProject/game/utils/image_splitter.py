from PIL import Image


class ImageSplitter():
    def __init__(self):
        pass

    def split(self, path_to_image):
        cols = 4
        rows = [
            "Idle down",
            "Idle up",
            "Idle left",
            "Idle right",
            "Moving down",
            "Moving up",
            "Moving left",
            "Moving right",
            "Attack down",
            "Attack up",
            "Attack left",
            "Attack right"
        ]
        result = dict()
        with Image.open(path_to_image) as sheet:
            frame_width = sheet.width // cols
            frame_height = sheet.height // len(rows)

            for row in range(len(rows)):
                result[rows[row]] = []
                for col in range(cols):
                    left = col * frame_width
                    top = row * frame_height
                    right = left + frame_width
                    bottom = top + frame_height
                    frame = sheet.crop((left, top, right, bottom))
                    result[rows[row]].append(frame)
        return result
