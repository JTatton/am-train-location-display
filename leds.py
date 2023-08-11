"""
LEDs Module
Josh Tatton 2023

This is a quick and dirty implementation to make use of WS281x LEDs / Adafruit NeoPixels on the Raspberry Pi. 
This is specifically used for the realtime train display project, but could be extended and used elsewhere.
"""

from time import sleep
from random import randint
from rpi_ws281x import *

LED_COUNT = 88
LED_PIN = 18
led_strip = PixelStrip(LED_COUNT, LED_PIN, brightness=64)

"""
Using the default values for the PixelStrip class.
    Taken from documentation:
        class PixelStrip:
        def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
                brightness=255, channel=0, strip_type=None, gamma=None):
            '''Class to represent a SK6812/WS281x LED display.  Num should be the number of pixels in the display, and pin should be the GPIO pin connected to the display signal line (must be a PWM pin like 18!).  Optional parameters are freq, the frequency of the display signal in hertz (default 800khz), dma, the DMA channel to use (default 10), invert, a boolean specifying if the signal line should be inverted (default False), and channel, the PWM channel to use (defaults to 0).'''
"""

gamma8 = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,\
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,\
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,\
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,\
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,\
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,\
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,\
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,\
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,\
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,\
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,\
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,\
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,\
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,\
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,\
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]

def setup_strip():
    """Call first to Initialise LED strip"""
    led_strip.begin()

def light(ledNum, red=255, green=255, blue=255):
    """Basic call to light ledNum a specific colour. 
    Must call show() afterwards."""
    led_strip.setPixelColor(ledNum, Color(gamma8[red],gamma8[green],gamma8[blue]))

def light_all(r,g,b,t):
    """Light all leds the same colour for t amount of time.
    Must call clear_all() after to turn off"""
    for i in range(LED_COUNT):
        light(i, r, g, b)
    show()
    sleep(t)

def show():
    """Calls .show() on led_strip from ws281x Library"""
    led_strip.show()

def clear_all():
    """Clears all LEDs and turns off"""
    for i in range(LED_COUNT):
        clear(i)
    show()

def clear(led_num):
    """Turns off specified LED"""
    light(led_num,0,0,0)

def test_leds():
    """Test function for testing all LEDs and cycles colours"""
    light_all(255,0,0,0.5)
    light_all(0,255,0,0.5)
    light_all(0,0,255,0.5)
    light_all(255,255,255,0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    light_all(randint(0,255), randint(0,255), randint(0,255),0.5)
    clear_all()

if __name__ == "__main__":
    print("LEDs Module\n")

    print("Setting Up")
    setup_strip()

    print("Testing All LEDs")
    test_leds()

    print("Test Complete")
    clear_all()
    