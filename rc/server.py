#!/usr/bin/env python3

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import ev3dev.ev3 as ev3
import time
import random
import sys

SPEED=500
HAND_SPEED=500

lm1 = ev3.LargeMotor('outD')
lm2 = ev3.LargeMotor('outB')
m1 = ev3.Motor('outA')

def driveMotor(motor, speed):
  print("speed=", speed)
  motor.run_forever(speed_sp=speed)

def stopMotor(motor):
  try:
    motor.stop()
  except:
    print("Unexpected error:", sys.exc_info()[0])

def stop():
  stopMotor(m1)
  stopMotor(lm1)
  stopMotor(lm2)

def say():
  message = 'robbi'
  with open('./message.txt') as f:
    messages = f.readlines()
    message = random.choice(messages)
  ev3.Sound.speak(message).wait()
  time.sleep(1)

ACTIONS = {
  "m1f": lambda : driveMotor(m1, HAND_SPEED),
  "m1b": lambda : driveMotor(m1, -HAND_SPEED),
  "lm1f": lambda : driveMotor(lm1, SPEED),
  "lm1b": lambda : driveMotor(lm1, -SPEED),
  "lm2f": lambda : driveMotor(lm2, SPEED),
  "lm2b": lambda : driveMotor(lm2, -SPEED),
  "stop": lambda : stop(),
  "say": lambda : say()
}

class RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    root = os.path.dirname(os.path.abspath(__file__))
    #print(self.path)
    if self.path == '/':
      filename = root + '/index.html'
    else:
      filename = root + self.path

    if not os.path.isfile(filename):
      self.send_not_found
      return
 
    self.send_response(200)
    if filename[-4:] == '.css':
      self.send_header('Content-type', 'text/css')
    elif filename[-3:] == '.js':
      self.send_header('Content-type', 'application/javascript')
    else:
      self.send_header('Content-type', 'text/html')
    self.end_headers()
    with open(filename, 'rb') as fh:
      html = fh.read()
      #html = bytes(html, 'utf8')
      self.wfile.write(html)
 
  def do_POST(self):
    if not self.path.startswith("/api/rc"):
      self.send_not_found
      return
 
    query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
    actions = query_components.get("action", [])
    print(actions)
    for action in actions:
      actionFunc = ACTIONS.get(action, None)
      if actionFunc:
        actionFunc()

    self.send_no_content()

  def send_no_content(self):
    self.send_response(204)
    self.end_headers()

  def send_not_found(self):
    self.send_response(404)
    self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000):
  stop()
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd on port {}'.format(port))
  say()
  httpd.serve_forever()
 
if __name__ == "__main__":
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
