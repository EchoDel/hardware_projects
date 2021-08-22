from PlantHealth.helper_functions import get_colour, get_neopixel_number
from PlantHealth.pixels import update_neopixels
from helper_functions.io import load_json_settings, update_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import connect_wifi, TinywebUpdateWifi, \
    update_wifi_html, setup_access_point
import tinyweb
from tinyweb.server import parse_query_string
import network
import uasyncio


wifi_config_file = 'configs/wireless_network.json'
plant_config_file = 'PlantHealth/config.json'
neopixel_number = 10
connect_wifi(2, wifi_config_file)

# setup own wifi network if not connected
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    setup_access_point(wifi_config_file)


app = tinyweb.server.webserver()


# Update wifi page
@app.route('/update_wifi')
async def index(request, response):
    wireless_properties = load_json_settings(wifi_config_file)
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send(update_wifi_html(**wireless_properties))


@app.route('/send_wifi_update')
async def index(request, response):
    new_config = parse_query_string(request.query_string.decode())
    update_json_settings(wifi_config_file, new_config)
    wireless_properties = load_json_settings(wifi_config_file)
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send(update_wifi_html(**wireless_properties))

app.add_resource(TinywebUpdateWifi,
                 '/post_wifi_update',
                 config_file=wifi_config_file)


async def my_app():
    plant_config = load_json_settings(plant_config_file)
    smd = get_soil_moisture()  # get SMD
    number = get_neopixel_number(smd)
    temp = get_temperature()
    colour = get_colour(temp, **plant_config['temperature'])  # calculate colour
    update_neopixels(number, colour)
    print('sleeping')
    await uasyncio.sleep(60)

print('loaded')

app.run(host='0.0.0.0', port=80, loop_forever=False)
app.loop.create_task(my_app())
app.loop.run_forever()
