import time
from machine import Pin, I2C, ADC
import array

from ToddlerTimer.oled import init_oled, clear_screen, update_number, write_large
from helper_functions.rotary_encoder import RotaryIRQ

from ToddlerTimer.config import *

oled = init_oled(oled_sda, oled_scl, WIDTH, HEIGHT)


rotary_encoder = RotaryIRQ(rotary_encoder_clk_pin, rotary_encoder_dt_pin)
rotary_encoder_sw = Pin(rotary_encoder_sw_pin, Pin.IN, Pin.PULL_UP)

# todo move to oled module, add animation
hour_glass = array.array('I',[100,4,
                              120,4,
                              110,16,
                              120,28,
                              100,28,
                              110,16, ]) # 6 pairs
oled.poly(0,0, hour_glass, 1, True) # Filled
oled.show()




# Set the timer value
val_old = rotary_encoder.value()
while True:
    val_new = rotary_encoder.value()
    if val_old != val_new:
        val_old = val_new
        write_large(oled,
                    str(val_old),
                    TEXT_START_ROW,
                    MINUTE_TEXT_START - 4,
                    True)
    if rotary_encoder_sw.value() == 0:
        minutes_to_countdown = val_old
        start_time = time.time()
        end_time = start_time + minutes_to_countdown * 60
        break


while True:
    clear_screen(oled)
    oled.poly(0, 0, hour_glass, 1, True)  # Filled
    # todo draw rotating icon
    seconds_left = end_time - time.time()
    if seconds_left < 0:
        break

    minutes_left = seconds_left // 60
    seconds_left = seconds_left % 60
    write_large(oled,
                f'{minutes_left}:{seconds_left}',
                TEXT_START_ROW,
                20,
                False)
    # todo light up led strip

    time.sleep(1)