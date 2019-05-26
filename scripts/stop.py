#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

motorHand = ev3.Motor('outA')
motorLeft = ev3.LargeMotor('outB')
motorRight = ev3.LargeMotor('outC')

motorLeft.reset()
motorRight.reset()

