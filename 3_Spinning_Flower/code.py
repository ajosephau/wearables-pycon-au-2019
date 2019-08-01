import time

from adafruit_circuitplayground.express import cpx
import board
import pulseio
from adafruit_motor import servo

pwm = pulseio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

def spin_motor():
    for angle in range(0, 180, 1):
        my_servo.angle = angle
        time.sleep(0.001)
    for angle in range(180, 0, -1):
        my_servo.angle = angle
        time.sleep(0.001)

while True:
    if cpx.button_a or cpx.button_b:
        spin_motor()
