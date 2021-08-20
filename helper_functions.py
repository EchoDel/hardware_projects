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


def connect_wifi(config_file):
    import json
    wireless_properties = json.load(open(config_file, 'rb'))
    return do_connect(**wireless_properties)
