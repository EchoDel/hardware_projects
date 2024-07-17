from pathlib import Path

import PySimpleGUI as sg
from PIL import Image, ExifTags, ImageOps
from PIL.TiffTags import TAGS
import PIL
import io
import base64

from pillow_heif import register_heif_opener

G_SIZE = (1920, 1080)          # Size of the Graph in pixels. Using a 1 to 1 mapping of pixels to pixels

sg.theme('black')
register_heif_opener()


def normalise_rotation_tiff(image: Image.Image):
    meta_dict = {TAGS[key]: image.tag[key] for key in image.tag.keys() if key in TAGS}
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)

    return image


def normalise_rotation(image: Image.Image):
    # if image.format == 'TIFF':
    #     image = normalise_rotation_tiff(image)
    # else:
    image = ImageOps.exif_transpose(image)
    return image


def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (str | bytes)
    :param resize:  optional new size
    :type resize: ((int, int) | None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))

    img = normalise_rotation(img)
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)))
        output_folder = Path('picture_frame/test/')
        # img.save((output_folder / file_or_bytes.split('\\')[-1]).with_suffix(".png"))

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    img_width, img_height = img.size
    del img
    return bio.getvalue(), img_width, img_height


graph = sg.Graph(canvas_size=G_SIZE,
                 graph_bottom_left=(0, 0),
                 graph_top_right=G_SIZE,
                 enable_events=True,
                 key='-GRAPH-',
                 pad=(0, 0))

layout = [[graph]]

window = sg.Window('Scrolling Image Viewer',
                   layout,
                   margins=(0, 0),
                   use_default_focus=False,
                   finalize=True,
                   no_titlebar=True)

window.Maximize()
window.bind("<Escape>", "-ESCAPE-")
