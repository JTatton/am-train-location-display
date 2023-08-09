import leds
import random
import time

leds.setupStrip()

def test_all(r,g,b,t):
    for i in range(0,88):
        leds.light(i, r, g, b)
    leds.show()
    time.sleep(t)

test_all(255,0,0,2)
test_all(0,255,0,2)
test_all(0,0,255,2)
test_all(255,255,255,2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)
test_all(random.randint(0,255), random.randint(0,255), random.randint(0,255),2)


leds.clearAll()