from PlantMonitor.helper_functions import get_colour, get_neopixel_number
from PlantMonitor.pixels import update_neopixels
from PlantMonitor.webpages import setup_tinyweb_soil_moisture
from helper_functions.io import load_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import connect_wifi, setup_access_point, \
    setup_tinyweb_wifi
import network
import uasyncio
import machine
import neopixel


wifi_config_file = 'configs/wireless_network.json'
plant_config_file = 'PlantMonitor/config.json'
neopixel_number = 10
connect_wifi(2, wifi_config_file)


import tinyweb

# Setup the neopixel strip
np = neopixel.NeoPixel(machine.Pin(5), neopixel_number)


# setup own wifi network if not connected
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    setup_access_point(wifi_config_file)

# Setup the tinyweb app
webserver = tinyweb.server.webserver()
# Add the update wifi settings to the app
setup_tinyweb_wifi(webserver, wifi_config_file)

# Setup the webpages to update the config of the soil sensor
setup_tinyweb_soil_moisture(webserver, plant_config_file)


# define the main loop of the application
async def my_app():
    while True:
        plant_config = load_json_settings(plant_config_file)
        adc_raw, soil_moisture_perc = get_soil_moisture(
            **plant_config['soil_moisture_calibration'])  # get SMD
        number = get_neopixel_number(soil_moisture_perc, neopixel_number,
                                     **plant_config['soil_moisture'])
        if number > neopixel_number:
            colour = (200, 0, 200)
            number = neopixel_number
        else:
            temp = get_temperature()
            colour = get_colour(temp, **plant_config['temperature'])  # calculate colour
        update_neopixels(neopixel_number, number, colour, np)
        await uasyncio.sleep(60)

webserver.loop.create_task(my_app())

print('loaded')

# Run the app
webserver.run(host='0.0.0.0', port=80)
