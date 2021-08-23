def update_neopixels(number, colour, np):
    print(number, colour)
    for n in range(number):
        print(n)
        np[n] = colour
    np.write()
