#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

print("ready")

while True:
  ev3.Sound.speak('hello').wait()
  time.sleep(1)
