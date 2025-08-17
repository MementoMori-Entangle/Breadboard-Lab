from machine import I2C, Pin
import bme280
import utime

# アメダス海面気圧データ TODO : OpenWeatherMap APIの海面気圧を定期的に取る(ネットにつながっている場合)
SEA_LEVEL_PRESSURE = 1010.6

# 国土地理院APIで取得したelevation（海面基準の標高[m]）
# リアルタイムで正確な値を取得する場合、GPSから座標を取得して、
# 国土地理院APIから海面基準の標高を取得する必要がある。
# 高負荷になるので好ましくないので、ある一定(都市区間など)で同じ値を使用し、
# どうしても精度が必要な場合のみGPSデータから取得して適用する。
API_ELEVATION = 25

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = bme280.BME280(i2c=i2c)

def calculate_altitude_sea_level(pressure_hpa, temperature_c):
    temperature_k = temperature_c + 273.15
    return ((((SEA_LEVEL_PRESSURE / pressure_hpa) ** 0.1903) - 1) * temperature_k) / 0.0065

while True:
    temp, pressure, humidity = bme.read_compensated_data()
    pressure_hpa = pressure / 25600
    temperature_c = temp / 100

    altitude_sea_level = calculate_altitude_sea_level(pressure_hpa, temperature_c)
    current_altitude = altitude_sea_level - API_ELEVATION

    print("Pressure: {:.2f} hPa, Altitude (気圧計): {:.2f} m, API標高: {:.2f} m, 現在高度: {:.2f} m, Temp: {:.2f} C".format(
        pressure_hpa, altitude_sea_level, API_ELEVATION, current_altitude, temperature_c))

    utime.sleep_ms(5000)
