# Breadboard-Lab
ブレッドボード実験室

# 高度データをLCDで表示する実験
<img width="504" height="378" alt="bmp280_lcd_1" src="https://github.com/user-attachments/assets/22cbb537-118c-4821-aa22-30b3225a2ea2" />

ハードウェア  
Raspberry Pi Pico WH  
ブレッドボード EIC-301  
USBケーブル USB2.0 Aオス-マイクロBオス 0.15m A-microB  
ブレッドボード・ジャンパーワイヤ 15cm黒と白  
BMP280 3.3V I2C IIC (抵抗103)  
Freenove I2C LCD 1602 (5V)

ソフトウェア  
bmp280_print(main).py  
lcd_print.py  
wifi_connect.py

I2C通信  
左　　　　GPIO  
　VSS　　　33(→28)  
　VDD　　　39  
　SDA　　　19(GP14)  
　SCK　　　20(GP15)  
右

VSS → GND  
VDD → VCC  
SDA → SDA  
SCK → SCL

MicroPython  
| パッケージ名                 | バージョン   | ライセンス    |
|-----------------------------|-------------|--------------|
| machine                     | -           | MIT          |
| utime                       | -           | MIT          |
| bme280                      | 0.7         | BSD          |
| I2cLcd                      | -           | MIT          |　　　　
| network                     | -           | MIT          |
| ntptime                     | -           | MIT          |

# 高度を取得する実験
<img width="504" height="200" alt="bmp280_高度取得実験" src="https://github.com/user-attachments/assets/5a5f6ddd-bc95-4097-85c2-f6258a36fa7c" />

ハードウェア  
Raspberry Pi Pico WH  
ブレッドボード EIC-301  
USBケーブル USB2.0 Aオス-マイクロBオス 0.15m A-microB  
ブレッドボード・ジャンパーワイヤ 15cm黒と白  
BMP280 3.3V I2C IIC (抵抗103)

ソフトウェア  
bme280.py

I2C通信  
左　　　　GPIO  
　　VCC　　36  
　　GND　　23(→33)  
　　SCL　　02  
　　SDA　　01  
　　CSB　　未使用  
　　SDO　　未使用  
右

MicroPython
| パッケージ名                 | バージョン   | ライセンス    |
|-----------------------------|-------------|--------------|
| machine                     | -           | MIT          |
| utime                       | -           | MIT          |
| bme280                      | 0.7         | BSD          |
