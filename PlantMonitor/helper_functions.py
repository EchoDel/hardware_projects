class MoistureException(Exception):
    pass


def get_colour(temperature, minimum, maximum):
    if temperature < minimum or temperature > maximum:  # outside max and min red
        return 200, 0, 0
    elif temperature < minimum + 1 or temperature > maximum - 1:  # close to max and min orange
        return 200, 100, 0
    else:  # else green
        return 0, 200, 0


def get_neopixel_number(soil_moisture, neopixel_number, minimum, maximum):
    return int(round(c_like_map(soil_moisture, minimum, maximum,
                                0, neopixel_number)))


def c_like_map(value, original_min, original_max, final_min, final_max):
    final_range = final_max - final_min
    original_range = original_max - original_min
    result = (value - original_min) / original_range * final_range + final_min
    return result
