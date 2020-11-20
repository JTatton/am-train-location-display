#!/usr/bin/python3

import time
from rpi_ws281x import *

OUTHA_COUNT = 25
GAW_COUNT = 26
SEAF_COUNT = 25
BEL_COUNT = 11

OUTHA_PIN = 10
GAW_PIN = 12
SEAF_PIN = 18
BEL_PIN = 21

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = 0
LED_CHANNEL = 0

outhaStrip = Adafruit_NeoPixel(OUTHA_COUNT, OUTHA_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
gawStrip = Adafruit_NeoPixel(GAW_COUNT, GAW_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
seafStrip = Adafruit_NeoPixel(SEAF_COUNT, SEAF_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
belStrip = Adafruit_NeoPixel(BEL_COUNT, BEL_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

def setupStrips():
    outhaStrip.begin()
    gawStrip.begin()
    seafStrip.begin()
    belStrip.begin()

def light(line, stop):
    if line == "OUTHA":
        outhaStrip.setPixelColor(stop, Color(255,0,0))
        outhaStrip.show()
    elif line == "GAW":
        gawStrip.setPixelColor(stop, Color(255,0,0))
        gawStrip.show()
    elif line == "SEAF":
        seafStrip.setPixelColor(stop, Color(255,0,0))
        seafStrip.show()
    elif line == "BEL":
        belStrip.setPixelColor(stop, Color(255,0,0))
        belStrip.show()
    else:
        print("Incorrect use of line. Use; OUTHA, GAW, SEAF, BEL")

def clear():
    for i in range(OUTHA_COUNT):
        outhaStrip.setPixelColor(i, Color(0,0,0))
        outhaStrip.show()
        time.sleep(50/1000.0)
    for i in range(GAW_COUNT):
        gawStrip.setPixelColor(i, Color(0,0,0))
        gawStrip.show()
        time.sleep(50/1000.0)
    for i in range(SEAF_COUNT):
        seafStrip.setPixelColor(i, Color(0,0,0))
        seafStrip.show()
        time.sleep(50/1000.0)
    for i in range(BEL_COUNT):
        belStrip.setPixelColor(i, Color(0,0,0))
        belStrip.show()
        time.sleep(50/1000.0)