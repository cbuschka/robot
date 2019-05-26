#!/usr/bin/env python3

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import ev3dev.ev3 as ev3
import time
import random

SPEED=500
HAND_SPEED=1300

motorHand = ev3.Motor('outA')
motorLeft = ev3.LargeMotor('outB')
motorRight = ev3.LargeMotor('outD')

def rotateRight(duration):
  motorLeft.run_forever(speed_sp=SPEED)
  motorRight.run_forever(speed_sp=-SPEED)

def rotateLeft(duration):
  motorLeft.run_forever(speed_sp=-SPEED)
  motorRight.run_forever(speed_sp=SPEED)

def forward(duration):
  motorLeft.run_forever(speed_sp=SPEED)
  motorRight.run_forever(speed_sp=SPEED)

def backward(duration):
  motorLeft.run_forever(speed_sp=-SPEED)
  motorRight.run_forever(speed_sp=-SPEED)

def rotateHandRight(duration):
  motorHand.run_forever(speed_sp=HAND_SPEED)

def rotateHandLeft(duration):
  motorHand.run_forever(speed_sp=-HAND_SPEED)

def stop():
  motorLeft.stop()
  motorRight.stop()
  motorHand.stop()

def say():
  message = 'robbi'
  with open('./message.txt') as f:
    messages = f.readlines()
    message = random.choice(messages)
  ev3.Sound.speak(message).wait()
  time.sleep(1)


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
    action = query_components["action"]
    print(action)
    if action[0] == 'forward':
      forward(2000)
    elif action[0] == 'backward':
      backward(2000)
    elif action[0] == 'left':
      rotateLeft(2000)
    elif action[0] == 'right':
      rotateRight(2000)
    elif action[0] == 'stop':
      stop()
    elif action[0] == 'motor1':
      rotateHandLeft(2000)
    elif action[0] == 'say':
      say()

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
