# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import neopixel

from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel as seesaw_neopixel

# from adafruit_seesaw.seesaw import Seesaw
sda=board.GP4
scl=board.GP5

# This is the bus for the slider
i2c = busio.I2C(scl, sda)

# NeoSlider setup
neoslider = Seesaw(i2c, 0x30)
potentiometer = AnalogInput(neoslider, 18)
neoslider_pixels = seesaw_neopixel.NeoPixel(neoslider, 14, 4)

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.GP0

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 24

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def fill_ring_color(color):
    for i in range(num_pixels):
        pixels[i] = wheel(color)
    pixels.show()

def potentiometer_to_color(value):
    """Scale the potentiometer values (0-1023) to the colorwheel values (0-255)."""
    return value / 1023 * 255

while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #pixels.fill((255, 0, 0, 0))
    #pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 255, 0, 0))
    #pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #pixels.fill((0, 0, 255, 0))
    #pixels.show()
    #time.sleep(1)

    # Fill the pixels a color based on the position of the potentiometer.
    led_color = potentiometer_to_color(potentiometer.value)
    neoslider_pixels.fill(colorwheel(led_color))
    fill_ring_color(led_color)

    # run the rainbow cycle for the pixel ring
    # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

    # ss.digital_write(15, True)  # turn the LED on (True is the voltage level)
    # time.sleep(1)  # wait for a second
    # ss.digital_write(15, False)  # turn the LED off by making the voltage LOW
    # time.sleep(1)
