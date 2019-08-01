from adafruit_circuitplayground.express import cpx
import time
import board
import pulseio

piezo = pulseio.PWMOut(board.A1, duty_cycle=0, frequency=440, variable_frequency=True)

frequencies = [ 262, # C
                294, # D
                330, # E
                349, # F
                392, # G
                440, # A
                494] # B

colours = [ (255,   0, 0),   # Red
            (255, 255, 0),   # Yellow
            (0,   255, 0),   # Green
            (0,     0, 255), # Blue
            (0,   255, 255), # Aqua
            (255,   0, 255), # Magenta
            (255, 255, 255)] # White

def sqrt(x):
    return x ** 0.5


def vector_mag(x, y, z):
    return sqrt(x ** 2 + y ** 2 + z ** 2)


while True:
    x, y, z = cpx.acceleration
    lookup = abs(int(x))
    if lookup < 0:
        lookup = 0
    if lookup >= (len(frequencies)-1):
        lookup = len(frequencies)-1
    tone = frequencies[lookup]
    colour = colours[lookup]

    cpx.pixels.fill(colour)
    cpx.pixels.show()

    if cpx.button_a or cpx.button_b:
        if cpx.switch:
            print("Play tone through speaker:", tone)
            cpx.play_tone(tone, 0.5)
        else:
            print("Play tone through audio:", tone)
            piezo.frequency = int(tone)
            piezo.duty_cycle = 65535 // 5  # On 50%
            time.sleep(0.5)
            piezo.duty_cycle = 0  # Off
