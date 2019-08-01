from adafruit_circuitplayground.express import cpx
import array
import audiobusio
import board
import math
from random import randint
from time import sleep

MAX_VALUE = 10
NUM_SAMPLES = 160

def sqrt(x):
    return x ** 0.5

def mean(values):
    return sum(values) / len(values)

def vector_mag(x, y, z):
    return sqrt(current_x ** 2 + current_y ** 2 + current_z ** 2)


def enable_value_on_led(score, led_id, r, g, b):
    if score > led_id:
        cpx.pixels[led_id] = (r, g, b)
    else:
        cpx.pixels[led_id] = (0, 0, 0)


def display_value_on_leds(value, max_value):
    score = value / max_value * MAX_VALUE
    enable_value_on_led(score, 0, 255, 0, 0)
    enable_value_on_led(score, 1, 255, 85, 0)
    enable_value_on_led(score, 2, 255, 255, 0)
    enable_value_on_led(score, 3, 0, 255, 0)
    enable_value_on_led(score, 4, 34, 139, 34)
    enable_value_on_led(score, 5, 0, 255, 255)
    enable_value_on_led(score, 6, 0, 0, 255)
    enable_value_on_led(score, 7, 0, 0, 139)
    enable_value_on_led(score, 8, 255, 0, 255)
    enable_value_on_led(score, 9, 75, 0, 130)
    sleep(0.1)


def increment_mode(mode):
    sleep(0.5)

    mode = mode + 1
    if mode > MAX_MODE:
        mode = MIN_MODE
    return mode


def decrement_mode(mode):
    sleep(0.5)
    mode = mode - 1
    if mode < MIN_MODE:
        mode = MAX_MODE
    return mode

# https://core-electronics.com.au/tutorials/sound-reactive-lights-circuitpython-circuit-playground-express-tutorial.html
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
 
    return math.sqrt(samples_sum / len(values))

past_measure = 0
max_value = 0
mode = 1
MIN_MODE = 1
MAX_MODE = 5

samples = array.array('H', [0] * NUM_SAMPLES)
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

while True:
    if cpx.button_a:
        mode = decrement_mode(mode)
    if cpx.button_b:
        mode = increment_mode(mode)
    if mode == 1:
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)

        print(magnitude)
        display_value_on_leds(magnitude, 2000)
        sleep(0.1)

    if mode == 2:
        current_x, current_y, current_z = cpx.acceleration
        current_measure = vector_mag(current_x, current_y, current_z)
        measure_delta = abs(current_measure - past_measure)

        if measure_delta > max_value:
            max_value = measure_delta

        print(current_x, MAX_VALUE)
        display_value_on_leds(measure_delta, max_value)

        past_measure = current_measure
    elif mode == 3:
        value = randint(0, MAX_VALUE)

        display_value_on_leds(value, MAX_VALUE)
    elif mode == 4:
        # Set to blue
        cpx.pixels.fill((0, 0, 255))
        sleep(0.1)
    elif mode == 5:
        # Set to gold
        cpx.pixels.fill((255, 215, 0))
        sleep(0.1)
