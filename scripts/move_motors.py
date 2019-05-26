#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

motorHand = ev3.Motor('outA')
motorLeft = ev3.LargeMotor('outB')
motorRight = ev3.LargeMotor('outC')

def rotateRight(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=300)
  motorRight.run_timed(time_sp=duration, speed_sp=-300)
  motorLeft.wait_until_not_moving()

def rotateLeft(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=-300)
  motorRight.run_timed(time_sp=duration, speed_sp=300)
  motorLeft.wait_until_not_moving()

def forward(duration):
  motorLeft.run_timed(time_sp=duration, speed_sp=300)
  motorRight.run_timed(time_sp=duration, speed_sp=300)
  motorLeft.wait_until_not_moving()

def rotateHandRight(duration):
  motorHand.run_timed(time_sp=duration, speed_sp=300)

def rotateHandLeft(duration):
  motorHand.run_timed(time_sp=duration, speed_sp=-300)

def runLoop():
  while True:
    rotateHandRight(2000)
    forward(5000)
    rotateRight(2000)
#    rotateHandLeft(1000)
#    rotateHandRight(4000)
    forward(2000)
    rotateLeft(5000)
#    rotateHandLeft(3000)
    forward(2000)

print("ready")
runLoop()
