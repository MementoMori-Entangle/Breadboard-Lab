import network
import utime

def connect_wifi(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        for _ in range(timeout * 10):  # timeout秒、0.1秒ごとチェック
            if wlan.isconnected():
                print('Wi-Fi connected:', wlan.ifconfig())
                return True
            utime.sleep(0.1)
        print('Wi-Fi connect failed')
        return False
    else:
        print('Already connected:', wlan.ifconfig())
        return True
