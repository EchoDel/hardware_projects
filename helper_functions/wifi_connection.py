import random
from helper_functions.io import load_json_settings, update_json_settings


def do_connect(attempts, ssid, password, hostname):
    import network
    from time import sleep
    sta_if = network.WLAN(network.STA_IF)
    max_attempts = attempts
    attempts = 0

    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.config(dhcp_hostname=hostname)
        print(ssid, password)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print('trying to connect')
            if attempts > max_attempts:
                break
            else:
                sleep(5)
                attempts += 1
    print('network config:', sta_if.ifconfig())
    return sta_if.isconnected()


def connect_wifi(attempts, config_file):
    wireless_properties = load_json_settings(config_file)
    return do_connect(attempts, **wireless_properties)


def setup_access_point(config_file):
    wireless_properties = load_json_settings(config_file)
    import network
    ap_if = network.WLAN(network.AP_IF)
    if 'hostname' in wireless_properties:
        ap_if.config(essid=wireless_properties['hostname'],
                     password=wireless_properties['hostname'],
                     channel=3)
    else:
        ssid = 'PlantPot' + str(random.randint(0, 1000))
        ap_if.config(essid=ssid, password=ssid, channel=3)


def update_wifi_html(ssid, password, hostname):
    with open("helper_functions/resources/update_wifi.html") as f:
        text = f.read()
    return text.format(ssid=ssid, password=password, hostname=hostname)


def new_wifi_html(ssid, password, hostname):
    with open("helper_functions/resources/new_wifi_settings.html") as f:
        text = f.read()
    return text.format(ssid=ssid, password=password, hostname=hostname)


def send_response(conn, response):
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)


def update_wifi(config_file):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    wireless_properties = load_json_settings(config_file)
    max_attempts = 10
    for attempts in range(max_attempts):
        conn, addr = s.accept()
        conn.settimeout(30.0)
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Request Content = %s' % request)
        if request.find('/update_wifi') > 0:
            update_json_settings(config_file, request)
            wireless_properties = load_json_settings(config_file)
            response = new_wifi_html(**wireless_properties)
            send_response(conn, response)
            conn.close()
            break
        else:
            response = update_wifi_html(**wireless_properties)
            send_response(conn, response)
        conn.close()
        attempts += 1


# tinyweb server based classed instead of sockets
class TinywebUpdateWifi:
    def get(self, data, config_file):
        print(data)
        update_json_settings(config_file, data)
        wireless_properties = load_json_settings(config_file)
        return update_wifi_html(**wireless_properties)
