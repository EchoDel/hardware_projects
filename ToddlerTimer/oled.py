from array import array
from machine import I2C, Pin

from .config import *
from helper_functions.oled import ssd1306, freesans20
from helper_functions.oled.writer import Writer


def init_oled(oled_sda: Pin, oled_scl: Pin, width: int, height: int):
    i2c = I2C(0, sda=oled_sda, scl=oled_scl, freq=400000)  # Connection controller 0

    oled = ssd1306.SSD1306_I2C(width, height, i2c)
    clear_screen(oled)
    write_large(oled, 'MIN', TEXT_START_ROW, MINUTE_TEXT_START, False)
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



