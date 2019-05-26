#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

colorNames = [ None, # none
  "sworz",
  "blow",
  "gruen",
  "gelb",
  "rod",
  "vice",
  "prown",
  ]
cs = ev3.ColorSensor()
print("ready")

def runLoop():
  prevColorName = None
  while True:
    currColorName = colorNames[cs.color if cs.color < len(colorNames) else None]
    if currColorName is not None and currColorName != prevColorName:
      print(currColorName + " " + str(cs.color))
      ev3.Sound.speak(currColorName).wait()
    else:
      time.sleep(0.01)
    prevColorName = currColorName

runLoop()
