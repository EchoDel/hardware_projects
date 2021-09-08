def update_neopixels(neopixel_number, number, colour, np):
    print(neopixel_number, number, colour)
    for n in range(neopixel_number):
        if n > number:
            colour = (0, 0, 0)
        np[n] = colour
    np.write()
