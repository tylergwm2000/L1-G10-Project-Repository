from RPLCD.gpio import CharLCD
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=40, pin_e=38, pins_data=[36, 32, 22, 18])
lcd.write_string(u'Hello world!')
