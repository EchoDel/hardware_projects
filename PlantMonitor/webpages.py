from helper_functions.io import load_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import update_wifi_html, \
    get_wireless_settings


async def landing_page(request, response, wifi_config_file):
    wireless_properties = load_json_settings(wifi_config_file)
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send(update_wifi_html(**wireless_properties))


# tinyweb server based classed instead of sockets
class GetStatus:
    def get(self, data, plant_config_file):
        data = {}
        data['network'] = get_wireless_settings()
        data['config'] = load_json_settings(plant_config_file)
        data['soil_moisture'] = get_soil_moisture()
        data['temperature'] = get_temperature()
        return data


# Class to return the current soil moisture
class GetSingleProperty:
    def get(self, data, plant_config_file, property, get_function):
        data = {}
        plant_config = load_json_settings(plant_config_file)
        data['config'] = plant_config[property]
        if property == 'soil_moisture':
            data[property] = get_function(
                **plant_config['soil_moisture_calibration'])
        else:
            data[property] = get_function()
        return data


def setup_tinyweb_soil_moisture(app, wifi_config_file, plant_config_file):
    # from tinyweb.server import parse_query_string
    # Update wifi page
    @app.route('/')
    async def index(request, response):
        await landing_page(request, response, wifi_config_file)

    @app.route('/index')
    async def index(request, response):
        await landing_page(request, response)

    app.add_resource(GetStatus,
                     '/get_status',
                     plant_config_file=plant_config_file)

    app.add_resource(GetSingleProperty,
                     '/get_soil_moisture',
                     plant_config_file=plant_config_file,
                     property='soil_moisture',
                     get_function=get_soil_moisture)

    app.add_resource(GetSingleProperty,
                     '/get_temperature',
                     plant_config_file=plant_config_file,
                     property='temperature',
                     get_function=get_temperature)
