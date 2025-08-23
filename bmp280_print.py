import ntptime
import utime
from bmp280 import get_bmp280_data
from lcd_print import print_to_lcd
from wifi_connect import connect_wifi

SSID = "YourSSID"
PASSWORD = "YourPassword"

if connect_wifi(SSID, PASSWORD):
    ntptime.settime()

def get_datetime_string():
    tm = utime.localtime(utime.time() + 9*60*60)
    # 例: "250821 23:59:59"
    return "{:02d}{:02d}{:02d} {:02d}:{:02d}:{:02d}".format(tm[0]%100, tm[1], tm[2], tm[3], tm[4], tm[5])

while True:
    data = get_bmp280_data()
    # 1行目: 日時
    line1 = get_datetime_string()
    # 2行目: 高度,温度
    line2 = "A:{:.1f}m T:{:.1f}C".format(data["altitude"], data["temperature_c"])
    print_to_lcd([line1, line2])
    utime.sleep(5)
