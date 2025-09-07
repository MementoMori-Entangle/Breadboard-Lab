import network
import socket
import time
from data_pool import data_pool

# Wi-Fi接続情報
ssid = 'YourSSID'
password = 'YourPassword'

ports = [80]

def run():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)

    sockets = []
    for port in ports:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        sockets.append((s, port))
        print(f"Listening on port {port}")

    print("Webサーバー起動 IP:", wlan.ifconfig()[0])

    while True:
        for s, port in sockets:
            s.settimeout(1)
            try:
                cl, addr = s.accept()
                print('接続:', addr, 'on port', port)
                request = cl.recv(1024)
                print('受信:', request)

                try:
                    status = data_pool.server_received_data(request.decode())
                except Exception as e:
                    print('server_received_data error:', e)
                    status = 500

                if status == 200:
                    status_line = 'HTTP/1.0 200 OK\r\n'
                    body = 'Success'
                elif status == 400:
                    status_line = 'HTTP/1.0 400 Bad Request\r\n'
                    body = 'Bad Request'
                elif status == 404:
                    status_line = 'HTTP/1.0 404 Not Found\r\n'
                    body = 'Not Found'
                elif status == 500:
                    status_line = 'HTTP/1.0 500 Internal Server Error\r\n'
                    body = 'Server Error'
                else:
                    status_line = f'HTTP/1.0 {status} Unknown\r\n'
                    body = f'Status: {status}'

                cl.send(status_line + 'Content-Type: text/plain; charset=utf-8\r\n\r\n')
                cl.send(body)
                cl.close()
            except OSError as e:
                pass
