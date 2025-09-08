import bme280
import _thread
import utime
import web_server
from data_pool import add_data
from machine import I2C, Pin

# センサーデータ用キュー
sensor_queue = []
queue_lock = _thread.allocate_lock()

SEA_LEVEL_PRESSURE = 1011.1
API_ELEVATION = 25
SENSOR_INTERVAL_MS = 5000

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = bme280.BME280(i2c=i2c)

def calculate_altitude_sea_level(pressure_hpa, temperature_c):
    temperature_k = temperature_c + 273.15
    return ((((SEA_LEVEL_PRESSURE / pressure_hpa) ** 0.1903) - 1) * temperature_k) / 0.0065

def sensor_loop():
    while True:
        temp, pressure, humidity = bme.read_compensated_data()
        pressure_hpa = pressure / 25600
        temperature_c = temp / 100

        altitude_sea_level = calculate_altitude_sea_level(pressure_hpa, temperature_c)
        current_altitude = altitude_sea_level - API_ELEVATION

        print("Pressure: {:.2f} hPa, Altitude (気圧計): {:.2f} m, API標高: {:.2f} m, 現在高度: {:.2f} m, Temp: {:.2f} C".format(
            pressure_hpa, altitude_sea_level, API_ELEVATION, current_altitude, temperature_c))

        sensor_data = {
            'temperature': temperature_c,
            'humidity': humidity / 1024,
            'pressure': pressure_hpa,
            'altitude_sea_level': altitude_sea_level,
            'current_altitude': current_altitude
        }
        # キューに追加
        queue_lock.acquire()
        sensor_queue.append(sensor_data)
        queue_lock.release()
        utime.sleep_ms(SENSOR_INTERVAL_MS)

# サブスレッド：キューからデータを取り出してadd_data
def data_pool_loop():
    while True:
        queue_lock.acquire()
        if sensor_queue:
            data = sensor_queue.pop(0)
            queue_lock.release()
            add_data(data)
        else:
            queue_lock.release()
        utime.sleep_ms(SENSOR_INTERVAL_MS - 300)  # キュー監視間隔

# Webサーバーを別スレッドで起動
_thread.start_new_thread(web_server.run, ())
# データプール処理を別スレッドで起動
_thread.start_new_thread(data_pool_loop, ())
# Wi-Fi + Webサーバー起動待機
utime.sleep_ms(7000)
# メインでセンサーループ
sensor_loop()
