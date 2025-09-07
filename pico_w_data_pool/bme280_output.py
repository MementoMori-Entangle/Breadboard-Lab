import bme280
import _thread
import utime
import web_server
from data_pool import add_data
from machine import I2C, Pin

SEA_LEVEL_PRESSURE = 1011.1
API_ELEVATION = 25

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
        add_data(sensor_data)
        utime.sleep_ms(5000)

# Webサーバーを別スレッドで起動
_thread.start_new_thread(web_server.run, ())
# Wi-Fi + Webサーバー起動待機
utime.sleep_ms(7000)
# メインでセンサーループ
sensor_loop()
