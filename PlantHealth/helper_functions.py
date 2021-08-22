def get_colour(temperature, minimum, maximum):
    if temperature < minimum or temperature > maximum:  # outside max and min red
        return 200, 0, 0
    elif temperature < minimum + 1 or temperature > maximum - 1:  # close to max and min orange
        return 200, 128, 0
    else:  # else green
        return 0, 200, 0


def get_neopixel_number(soil_moisture, neopixel_number, minimum, maximum):
    range = (maximum - minimum)
    return int(round((soil_moisture - minimum) / range * neopixel_number))
