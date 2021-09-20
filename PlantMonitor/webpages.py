from PlantMonitor.helper_functions import get_colour
from helper_functions.io import load_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import get_wireless_settings
from helper_functions.html import setup_webpage

async def landing_page(request, response):
    # Start HTTP response with content-type text/html
    await response.start_html()
    # Send actual HTML page
    await response.send(setup_webpage("PlantMonitor/resources/index/index.min.html"))


# tinyweb server based classed instead of sockets
class GetStatus:
    def get(self, data, plant_config_file):
        data = {'debug':{}}
        data['network'] = get_wireless_settings()
        data['config'] = load_json_settings(plant_config_file)
        adc_raw, soil_moisture_perc = get_soil_moisture(**data['config']['soil_moisture_calibration'])
        data['soil_moisture'] = soil_moisture_perc
        data['debug']['adc_raw'] = adc_raw

        if soil_moisture_perc > data['config']['soil_moisture']['maximum']:
            colour = (200, 0, 200)
        else:
            temp = get_temperature()
            colour = get_colour(temp, **data['config']['temperature'])

        data['temperature'] = temp
        data['colour'] = colour
        return data


# Class to return the current soil moisture
class GetSingleProperty:
    def get(self, data, plant_config_file, sensor, get_function):
        data = {}
        plant_config = load_json_settings(plant_config_file)
        data['config'] = plant_config[sensor]
        if sensor == 'soil_moisture':
            data[sensor] = get_function(
                **plant_config['soil_moisture_calibration'])
        else:
            data[sensor] = get_function()
        return data


def setup_tinyweb_soil_moisture(app, plant_config_file):
    # from tinyweb.server import parse_query_string
    # Update wifi page
    @app.route('/')
    async def index(request, response):
        await response.send_file("PlantMonitor/resources/index/index.min.html.gz",
                                 content_type="text/html",
                                 content_encoding="gzip")

    @app.route('/index')
    async def index(request, response):
        await landing_page(request, response)

    @app.route('/index.css')
    async def css_style(request, response):
        await response.send_file("PlantMonitor/resources/index/index.min.css",
                                 content_type="text/css")

    @app.route('/index.js')
    async def css_style(request, response):
        await response.send_file("PlantMonitor/resources/index/index.min.js",
                                 content_type="application/javascript")
        # content type https://stackoverflow.com/questions/23714383/what-are-all-the-possible-values-for-http-content-type-header

    @app.route('/favicon.ico')
    async def css_style(request, response):
        await response.send_file("PlantMonitor/resources/favicon.ico",
                                 content_type="image/x-icon")

    app.add_resource(GetStatus,
                     '/get_status',
                     plant_config_file=plant_config_file)

    app.add_resource(GetSingleProperty,
                     '/get_soil_moisture',
                     plant_config_file=plant_config_file,
                     sensor='soil_moisture',
                     get_function=get_soil_moisture)

    app.add_resource(GetSingleProperty,
                     '/get_temperature',
                     plant_config_file=plant_config_file,
                     sensor='temperature',
                     get_function=get_temperature)
