# Use the blink(1) to communicate the state of our continuous integration system
# Green is OK, Red is :(, Orange is request failed
# The vast majority of this code originally written by Kevin Conley (@kevincon)

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import atexit
import requests
from lib.blink1_ctypes import Blink1
from time import sleep
import argparse

WALTER_MASTER_STATUS_URL = 'http://walter.marlinspike.hq.getpebble.com/ci/status/master'

FADE_DURATION_MS = 1000
STATUS_POLLING_INTERVAL_SECONDS = 5

GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
OFF = (0, 0, 0)

parser = argparse.ArgumentParser(description='Use the blink(1) to communicate build status.')
led_options = parser.add_mutually_exclusive_group()
led_options.add_argument('--both-leds', action='store_true', help='Use both LEDs')
led_options.add_argument('--top-led', action='store_true', help='Use only the top LED')
led_options.add_argument('--bottom-led', action='store_true', help='Use only the bottom LED')
args = parser.parse_args()
if args.top_led:
    ledn = 1
elif args.bottom_led:
    ledn = 2
else:
    # Either --both-leds was specified or nothing was (in which case use both)
    ledn = 0

b1 = Blink1()
# We should close the device when we're not using is to allow other scripts to access it
b1.close()

def fade_to_color(duration_ms, r, g, b):
  # Only open the device long enough to set the desired color
  b1.open()
  b1.fade_to_rgbn(duration_ms, r, g, b, ledn)
  b1.close()

def back_to_black():
  fade_to_color(0, *OFF)

# Turn the blink(1) off when script exits
atexit.register(back_to_black)

while True:
  try:
    build_status_page = requests.get(WALTER_MASTER_STATUS_URL)
    color = GREEN if (build_status_page.text == 'Successful') else RED
  except requests.ConnectionError:
    color = ORANGE
  fade_to_color(FADE_DURATION_MS, *color)
  sleep(STATUS_POLLING_INTERVAL_SECONDS)

