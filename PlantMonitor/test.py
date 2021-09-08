import machine
import neopixel

neopixel_number = 10
np = neopixel.NeoPixel(machine.Pin(5), neopixel_number)

for x in range(neopixel_number):
    np[x] = (0, 200, 0)

np[9] = (0, 200, 0)
np.write()

