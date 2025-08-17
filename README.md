# Breadboard-Lab
ブレッドボード実験室

# 高度を取得する実験
<img width="1008" height="399" alt="bmp280_高度取得実験" src="https://github.com/user-attachments/assets/5a5f6ddd-bc95-4097-85c2-f6258a36fa7c" />

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
　　GND　　23  
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
