from machine import Pin

WIDTH  = 128         # oled display width
HEIGHT = 32          # oled display height
TEXT_START_ROW = 8
MINUTE_TEXT_START = 48

oled_sda=Pin(8)   # Data pin
oled_scl=Pin(9)   # Clock pin

rotary_encoder_clk_pin = 2
rotary_encoder_dt_pin = 1
rotary_encoder_sw_pin = 0
