from time import sleep

import board
import neopixel

from adafruit_circuitplayground.express import cpx
import adafruit_fancyled.adafruit_fancyled as fancy


NUM_CPX_LEDS = len(cpx.pixels)
NUM_LED_STRIP = 30
NUM_STRIP_COLOURS = 5

STATUS_CHARGING = 0
STATUS_CHARGED = 1
STATUS_CHARGING_FAILED = 2
STATUS_ACTIVE = 3

MIN_CHARGE = 0
MAX_CHARGE = NUM_CPX_LEDS - 1

cpx.pixels.auto_write = False  # Update only when we say
cpx.pixels.brightness = 0.5   # make less blinding

pixel_strip = neopixel.NeoPixel(board.A1, NUM_LED_STRIP)
pixel_strip.auto_write = False
pixel_strip.brightness = 0.8

colour_red  = fancy.CRGB(1.0, 0, 0)
colour_blue = fancy.CRGB(0, 0, 1.0)
status_using_strip_palette = [fancy.mix(colour_red, colour_blue, i / (NUM_STRIP_COLOURS-1)) for i in range(NUM_STRIP_COLOURS)]
status_using_cpx_palette = [fancy.mix(colour_red, colour_blue, i / (NUM_CPX_LEDS-1)) for i in range(NUM_CPX_LEDS)]

colour_green = fancy.CRGB(0, 1.0, 0)
status_charging_palette = [fancy.mix(colour_red, colour_green, i / (NUM_CPX_LEDS-1)) for i in range(NUM_CPX_LEDS)]

colour_gold = fancy.CRGB(1.0, 0.8, 0)
colour_black = fancy.CRGB(0, 0, 0)

offset = 0

button_press = False
play_sound = False

status = STATUS_CHARGING
charge = MIN_CHARGE

def show_spinning_track(pixels, palette):
    for i in range(len(pixels)):
        color = fancy.palette_lookup(palette, offset + i / (len(pixels)-1))
        pixels[i] = color.pack()
    pixels.show()

def set_all_colours(pixels, colour_pack):
    pixels.fill(colour_pack)
    pixels.show()

def play_sound_file(file_name, should_play_sound):
    if should_play_sound:
        cpx.play_file(file_name)
        return False
    else:
        return should_play_sound


while True:
    should_play_sound_switch = cpx.switch

    if cpx.button_a or cpx.button_b:
        button_press = True
        play_sound = True and should_play_sound_switch
        
    if cpx.button_a: # Charge wand
        status = STATUS_CHARGING
        charge += 1
        if charge >= MAX_CHARGE:
            charge = MAX_CHARGE
            status = STATUS_CHARGED
        elif charge <= MIN_CHARGE:
            charge = MIN_CHARGE

    if cpx.button_b: # Use wand
        charge = MIN_CHARGE - 1
        if status == STATUS_CHARGED or status == STATUS_ACTIVE:            
            status = STATUS_ACTIVE
        else:
            status = STATUS_CHARGING_FAILED

    if status == STATUS_CHARGING:
        color = status_charging_palette[charge]
        pixel_strip.fill(color.pack())
        pixel_strip.show()
        
        for i in range(0, NUM_CPX_LEDS, 1):
            if i <= charge:
                cpx.pixels[i] = color.pack()
            else:
                cpx.pixels[i] = (0,0,0)
        cpx.pixels.show()
        
    elif status == STATUS_CHARGED:
        set_all_colours(pixel_strip, colour_gold.pack())
        set_all_colours(cpx.pixels, colour_gold.pack())
        play_sound = play_sound_file('charging.wav', play_sound)
        sleep(0.25)
        set_all_colours(pixel_strip, colour_black.pack())
        set_all_colours(cpx.pixels, colour_black.pack())

    elif status == STATUS_CHARGING_FAILED:
        set_all_colours(pixel_strip, colour_red.pack())
        set_all_colours(cpx.pixels, colour_red.pack())
        play_sound = play_sound_file('fail.wav', play_sound)
        sleep(0.25)
        set_all_colours(pixel_strip, colour_black.pack())
        set_all_colours(cpx.pixels, colour_black.pack())
        
    elif status == STATUS_ACTIVE:
        show_spinning_track(pixel_strip, status_using_strip_palette)
        show_spinning_track(cpx.pixels, status_using_cpx_palette)
        offset += 0.1
        play_sound = play_sound_file('success.wav', play_sound)
    
    if button_press:
        sleep(0.25)
        button_press = False
        print((charge, status))
