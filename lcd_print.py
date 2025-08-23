from machine import I2C, Pin
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27  # LCDのI2Cアドレス
i2c_lcd = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
lcd = I2cLcd(i2c_lcd, I2C_ADDR, 2, 16)

def print_to_lcd(lines):
    """
    LCDに複数行テキストを表示する
    lines: ["line1", "line2"]
    """
    lcd.clear()
    for i, text in enumerate(lines):
        lcd.move_to(0, i)
        lcd.putstr(text[:16])
