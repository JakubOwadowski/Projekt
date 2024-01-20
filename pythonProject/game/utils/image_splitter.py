from PIL import Image


def split(path_to_image, number_of_frames, frame_sets):
    result = dict()
    with Image.open(path_to_image) as sheet:
        frame_width = sheet.width // number_of_frames
        frame_height = sheet.height // len(frame_sets)

        for frame_set_idx in range(len(frame_sets)):
            result[frame_sets[frame_set_idx]] = []
            for frame_idx in range(number_of_frames):
                left = frame_idx * frame_width
                top = frame_set_idx * frame_height
                right = left + frame_width
                bottom = top + frame_height
                frame_idx = sheet.crop((left, top, right, bottom))
                result[frame_sets[frame_set_idx]].append(frame_idx)
    return result
