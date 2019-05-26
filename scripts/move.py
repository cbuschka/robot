#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time
import random

colorNames = [ None, # none
  "black",
  "blue",
  "green",
  "yellow",
  "red",
  "white",
  "brown" ]

colorSensor = ev3.ColorSensor()
motorHand = ev3.Motor('outA')
motorLeft = ev3.LargeMotor('outB')
motorRight = ev3.LargeMotor('outC')

def say(text):
  ev3.Sound.speak(text)

def getColor():
  return colorNames[colorSensor.color if colorSensor.color < len(colorNames) else None]

def rotateRight(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=300)
  motorRight.run_timed(time_sp=duration, speed_sp=-300)

def rotateLeft(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=-300)
  motorRight.run_timed(time_sp=duration, speed_sp=300)

def backward(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=-300)
  motorRight.run_timed(time_sp=duration, speed_sp=-300)

def forward(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=300)
  motorRight.run_timed(time_sp=duration, speed_sp=300)

def stopMotor():
  motorLeft.stop()
  motorRight.stop()

print("ready")
while True:
  color = getColor()
  if color == "white":
    forward(100)
  elif color == "red":
    stopMotor()
    rnd = random.randint(0,50)
    if rnd >= 25:
      rotateLeft(100*rnd)
    else:
      rotateRight(100*rnd)
    time.sleep(100*rnd/1000.0)
  else:
    rnd = random.randint(0,50)
    if rnd >= 25:
      rotateLeft(100*rnd)
    else:
      rotateRight(100*rnd)
    time.sleep(100*rnd/1000.0)

print("done")
