#!/usr/bin/python3

import time
from rpi_ws281x import *

LED_COUNT = 87
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = 0
LED_CHANNEL = 0

ledStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)


def setupStrip():
    ledStrip.begin()

def light(ledNum):
    ledStrip.setPixelColor(ledNum, Color(255,0,0))
    ledStrip.show()


def clear():
    for i in range(LED_COUNT):
        ledStrip.setPixelColor(i, Color(0,0,0))
        ledStrip.show()
        time.sleep(50/1000.0)