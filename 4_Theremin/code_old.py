from adafruit_circuitplayground.express import cpx
import time
import board
import pulseio

piezo = pulseio.PWMOut(board.A1, duty_cycle=0, frequency=440, variable_frequency=True)

while True:
    x, y, z = cpx.acceleration
    tone = 400 + x + 10 * y + 50 * z
    print(x, y, z)

    if cpx.switch:
        print("Play tone through speaker:", tone)
        cpx.play_tone(tone, 0.1)
    else:
        print("Play tone through audio:", tone)
        piezo.frequency = int(tone)
        piezo.duty_cycle = 65535 // 5  # On 50%
        time.sleep(0.1)
        piezo.duty_cycle = 0  # Off
