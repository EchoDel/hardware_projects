def do_connect(ssid, password, hostname):
    import network
    from time import sleep
    sta_if = network.WLAN(network.STA_IF)
    max_attempts = 100
    attempts = 0

    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.config(dhcp_hostname=hostname)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            if attempts > max_attempts:
                break
            else:
                sleep(5)
                attempts += 1
    print('network config:', sta_if.ifconfig())
    return sta_if.isconnected()


def load_wifi_settings(config_file):
    import json
    with open(config_file, 'rb') as f:
        return json.load(f)


def update_wifi_settings(config_file, request):
    ssid = request.split('ssid=')[1].split('&')[0]
    password = request.split('password=')[1].split('&')[0]
    hostname = request.split('hostname=')[1].split(' ')[0]

    new_wifi_settings = {'ssid': ssid,
                         'password': password,
                         'hostname': hostname}
    import json
    with open(config_file, 'wb') as f:
        json.dump(new_wifi_settings, f)


def connect_wifi(config_file):
    wireless_properties = load_wifi_settings(config_file)
    return do_connect(**wireless_properties)


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

    wireless_properties = load_wifi_settings(config_file)
    max_attempts = 10
    for attempts in range(max_attempts):
        conn, addr = s.accept()
        conn.settimeout(30.0)
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Request Content = %s' % request)
        if request.find('/update_wifi') > 0:
            update_wifi_settings(config_file, request)
            wireless_properties = load_wifi_settings(config_file)
            response = new_wifi_html(**wireless_properties)
            send_response(conn, response)
            conn.close()
            break
        else:
            response = update_wifi_html(**wireless_properties)
            send_response(conn, response)
        conn.close()
        attempts += 1
