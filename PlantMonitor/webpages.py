from PlantMonitor.helper_functions import get_colour
from helper_functions.io import load_json_settings, update_json_settings
from helper_functions.soil_moisture import get_soil_moisture
from helper_functions.temperature import get_temperature
from helper_functions.wifi_connection import get_wireless_settings
from tinyweb.server import parse_query_string


# tinyweb server based classed instead of sockets
class GetStatus:
    def get(self, data, plant_config_file):
        data = {'debug':{}}
        data['network'] = get_wireless_settings()
        data['config'] = load_json_settings(plant_config_file)
        adc_raw, soil_moisture_perc = get_soil_moisture(**data['config']['soil_moisture_calibration'])
        data['soil_moisture'] = soil_moisture_perc
        data['debug']['adc_raw'] = adc_raw
        temp = get_temperature()

        if soil_moisture_perc > data['config']['soil_moisture']['maximum']:
            colour = (200, 0, 200)
        else:
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
        await response.send_file("PlantMonitor/resources/index/index.min.html.gz",
                                 content_type="text/html",
                                 content_encoding="gzip")

    @app.route('/index.css')
    async def index_css(request, response):
        await response.send_file("PlantMonitor/resources/index/index.min.css",
                                 content_type="text/css")

    @app.route('/index.js')
    async def index_js(request, response):
        await response.send_file("PlantMonitor/resources/index/index.min.js",
                                 content_type="application/javascript")
        # content type https://stackoverflow.com/questions/23714383/what-are-all-the-possible-values-for-http-content-type-header

    @app.route('/favicon.ico')
    async def favicon(request, response):
        await response.send_file("PlantMonitor/resources/favicon.ico",
                                 content_type="image/x-icon")

    @app.route('/update_temperature')
    async def update_temperature(request, response):
        result = parse_query_string(request.query_string.decode())
        new_config = {}
        new_config['temperature'] = {key: float(value)
                                     for key, value in result.items()}
        update_json_settings(plant_config_file, new_config)
        await response.start_html()
        # Send actual HTML page
        await response.send('<meta http-equiv="Refresh" content="0; url=\'/index\'" />')

    @app.route('/update_soil')
    async def update_soil(request, response):
        result = parse_query_string(request.query_string.decode())
        new_config = {}
        new_config['soil_moisture'] = {key: float(value)
                                       for key, value in result.items()}
        update_json_settings(plant_config_file, new_config)
        await response.start_html()
        # Send actual HTML page
        await response.send(
            '<meta http-equiv="Refresh" content="0; url=\'/index\'" />')

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
