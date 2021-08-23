from PlantMonitor.helper_functions import get_colour, get_neopixel_number
from PlantMonitor.pixels import update_neopixels
from PlantMonitor.webpages import setup_tinyweb_soil_moisture
from helper_functions.io import load_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import connect_wifi, setup_access_point, \
    setup_tinyweb_wifi
import tinyweb
import network
import uasyncio
import machine
import neopixel


wifi_config_file = 'configs/wireless_network.json'
plant_config_file = 'PlantMonitor/config.json'
neopixel_number = 10

# Setup the neopixel strip
np = neopixel.NeoPixel(machine.Pin(5), neopixel_number)


connect_wifi(2, wifi_config_file)

# setup own wifi network if not connected
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    setup_access_point(wifi_config_file)

# Setup the tinyweb app
app = tinyweb.server.webserver()
# Add the update wifi settings to the app
setup_tinyweb_wifi(app, wifi_config_file)

# Setup the webpages to update the config of the soil sensor
setup_tinyweb_soil_moisture(app, wifi_config_file, plant_config_file)


# define the main loop of the application
async def my_app():
    plant_config = load_json_settings(plant_config_file)
    soil_moisture = get_soil_moisture(
        **plant_config['soil_moisture_calibration'])  # get SMD
    number = get_neopixel_number(soil_moisture, neopixel_number,
                                 **plant_config['soil_moisture'])
    if number > neopixel_number:
        colour = (255, 255, 0)
        number = neopixel_number
    else:
        temp = get_temperature()
        colour = get_colour(temp, **plant_config['temperature'])  # calculate colour
    update_neopixels(number, colour, np)
    print('sleeping')
    await uasyncio.sleep(60)

app.loop.create_task(my_app())

print('loaded')

# Run the app
app.run(host='0.0.0.0', port=80)
