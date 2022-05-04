import PySimpleGUI as sg
from PIL import Image
import PIL
import io
import base64

G_SIZE = (1920, 1080)          # Size of the Graph in pixels. Using a 1 to 1 mapping of pixels to pixels

sg.theme('black')


def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (str | bytes)
    :param resize:  optional new size
    :type resize: ((int, int) | None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.LANCZOS)
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
