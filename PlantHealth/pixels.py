import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(5), 8)


def update_neopixels(number, colour):
    print(number, colour)
    for n in range(0, number):
        np[n] = colour
    np.write()
