from array import array
from machine import I2C, Pin
from math import cos, sin

from .config import *
from helper_functions.oled import ssd1306, freesans20
from helper_functions.oled.writer import Writer


def init_oled(oled_sda: Pin, oled_scl: Pin, width: int, height: int):
    i2c = I2C(0, sda=oled_sda, scl=oled_scl, freq=400000)  # Connection controller 0

    oled = ssd1306.SSD1306_I2C(width, height, i2c)
    clear_screen(oled)
    return oled


def clear_screen(oled: ssd1306.SSD1306_I2C):
    oled.fill(0)  # Clear screen to BLACK
    oled.show()


def update_number(oled: ssd1306.SSD1306_I2C, minutes: int):
    square = array('I', [0, 4,
                         63, 4,
                         63, 24,
                         0, 24])
    oled.poly(0,0, square, 0, True)

    x_location = 63 - len(f'{minutes}')*8
    oled.text(f'{minutes}', x_location, 12)
    oled.show()


def write_large(oled: ssd1306.SSD1306_I2C, string: str, row: int, col: int, reverse_col: bool):
    square = array('I', [0, 4,
                         MINUTE_TEXT_START-1, 4,
                         MINUTE_TEXT_START-1, 24,
                         0, 24])
    oled.poly(0,0, square, 0, True)

    font_writer = Writer(oled, freesans20, False)
    if reverse_col:
        col = col - font_writer.stringlen(string)

    font_writer.set_textpos(oled, row, col)
    font_writer.printstring(string, False)
    oled.show()

# Hourglass centered on 0, 0
hour_glass = [[-10,-12], [10,-12],
              [0,0], [10,12],
              [-10,12], [0,0], ] # 6 pairs

def move_array(base_array, center: (int, int)):
    """
    Move a list of lists to a nwe center

    Args:
        base_array (List[List[int, int],]): Array of pairs of points in cartesian space
        center (Tuple[int, int]): The new center to move the points to

    Returns:
        (List[List[int, int],]): The array moved to the new location
    """
    new_array = [[x + center[0], y + center[1]] for x, y in base_array]
    return new_array

def rotate_array(base_array, rotation: int):
    """

    Args:
        base_array:
        rotation:

    Returns:

    """
    rotation_matrix = [[cos(rotation), -sin(rotation)],
                       [sin(rotation), cos(rotation)]]

    new_array = [[x * cos(rotation) - y * sin(rotation),
                  x * sin(rotation) + y * cos(rotation)] for x, y in base_array]

    return new_array


def plot_hour_glass(oled: ssd1306.SSD1306_I2C,
                    center: (int, int) = (0, 0),
                    rotation: int = 0,
                    hour_glass = hour_glass):
    if rotation != 0:
        hour_glass = rotate_array(hour_glass, rotation)
    if center != (0, 0):
        hour_glass = move_array(hour_glass, center)
    hour_glass = array('I', [round(x) for x in hour_glass for x in x])

    oled.poly(0, 0, hour_glass, 1, True)  # Filled
    oled.show()
