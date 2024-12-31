
import time
from machine import Pin, I2C, ADC
import array
import neopixel
from math import pi

from ToddlerTimer.oled import init_oled, clear_screen, write_large, plot_hour_glass
from helper_functions.rotary_encoder import RotaryIRQ

from ToddlerTimer.config import *

def setup():
    # Setup OLED Screen
    oled = init_oled(oled_sda, oled_scl, WIDTH, HEIGHT)

    # Setup Rotary Encoder
    rotary_encoder = RotaryIRQ(rotary_encoder_clk_pin, rotary_encoder_dt_pin)
    rotary_encoder_sw = Pin(rotary_encoder_sw_pin, Pin.IN, Pin.PULL_UP)

    # Setup neopixels
    p = Pin(3)
    np = neopixel.NeoPixel(p, 10, timing=1)

    return oled, rotary_encoder, rotary_encoder_sw, np



# Set the timer value
def pick_time(oled, rotary_encoder, rotary_encoder_sw):
    val_old = 0
    rotary_encoder.set(1)
    write_large(oled, 'MIN', TEXT_START_ROW, MINUTE_TEXT_START, False)
    plot_hour_glass(oled, (110, 16), 0)
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
            seconds_to_countdown = minutes_to_countdown * 60
            start_time = time.time()
            end_time = start_time + seconds_to_countdown
            break
    return minutes_to_countdown, seconds_to_countdown, start_time, end_time


def run_timer(oled, np, seconds_to_countdown, end_time):
    rotation = 0
    while True:
        clear_screen(oled)
        rotation += pi / 20
        plot_hour_glass(oled, (110, 16), rotation)
        seconds_left = end_time - time.time()
        if seconds_left < 0:
            break
        elif seconds_left < 60:
            colour = low_time_led_colour
            flash = True
        else:
            colour = base_led_colour
            flash = False
        leds_to_light = round((seconds_left  / seconds_to_countdown) * number_of_leds)
        minutes_left = seconds_left // 60
        seconds_left = seconds_left % 60
        write_large(oled,
                    f'{minutes_left}:{seconds_left:02d}',
                    TEXT_START_ROW,
                    20,
                    False)
        if flash:
            for n in range(number_of_leds):
                np[n] = (0, 0, 0)
            np.write()
            time.sleep(0.1)
        for n in range(number_of_leds):
            if n < leds_to_light:
                np[n] = colour
            else:
                np[n] = (0, 0, 0)
        np.write()
        time.sleep(0.2)

def main():
    oled, rotary_encoder, rotary_encoder_sw, np = setup()
    while True:
        minutes_to_countdown, seconds_to_countdown, start_time, end_time = (
            pick_time(oled, rotary_encoder, rotary_encoder_sw))
        run_timer(oled, np, seconds_to_countdown, end_time)


if __name__ == "__main__":
    main()
