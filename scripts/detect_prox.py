#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

irSensor = ev3.InfraredSensor()

print("ready")

def runLoop():
  while True:
    print(irSensor.proximity)
    time.sleep(1)

runLoop()
