#!/usr/bin/python3

import time
from rpi_ws281x import *
import random

LED_COUNT = 87
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 63
LED_INVERT = 0
LED_CHANNEL = 0

ledStrip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

def setupStrip():
    ledStrip.begin()

def light(ledNum, red=255, green=255, blue=255):
    ledStrip.setPixelColor(ledNum, Color(red,green,blue))

def show():
    ledStrip.show()

def clearAll():
    for i in range(LED_COUNT):
        ledStrip.setPixelColor(i, Color(0,0,0))
        time.sleep(50/1000.0)
    ledStrip.show()

def clear(ledNum):
    ledStrip.setPixelColor(ledNum, Color(0,0,0))
