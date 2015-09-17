from lib.blink1_ctypes import Blink1
import argparse

parser = argparse.ArgumentParser(description='Sets the blink(1) to red to indicate you are busy.')
led_options = parser.add_mutually_exclusive_group()
led_options.add_argument('--both-leds', action='store_true')
led_options.add_argument('--top-led', action='store_true')
led_options.add_argument('--bottom-led', action='store_true')
args = parser.parse_args()
if args.top_led:
    ledn = 1
elif args.bottom_led:
    ledn = 2
else:
    # either both or not specified
    ledn = 0

b1 = Blink1()
b1.fade_to_rgbn(1000, 255, 0, 0, ledn)
