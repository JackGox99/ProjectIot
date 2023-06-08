from machine import Pin, ADC, SPI
from mfrc522 import MFRC522
from time import sleep
from dht import DHT22

#Boton
boton = Pin(32, Pin.IN, Pin.PULL_UP)
#Temperatura
sensor = DHT22(Pin(14))
#Relay
relay = Pin(26, Pin.OUT)
#RFID
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
spi.init()
grn = Pin(2, Pin.OUT)
red = Pin(15, Pin.OUT)
#Movimiento
led1 = Pin(12, Pin.OUT)
pir = Pin(13, Pin.IN)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        print(temp)
        if temp>=600.4:
            relay.value(1)
        elif temp < 600.4:
            relay.value(0)
        if pir():
            print('Motion detected!')
            led1.on()
            sleep(1)
            if not pir():
                print('Motion stopped')
                led1.off()
    except OSError as e:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print(card_id)
                if card_id == "0xe9a3eeb1":
                    grn.on()
                    red.off()
                    sleep(1)
                    grn.off()
                    red.off()
                elif card_id == "0x396dcfa2":
                    grn.off()
                    red.on()
                    sleep(1)
                    grn.off()
                    red.off()
        


