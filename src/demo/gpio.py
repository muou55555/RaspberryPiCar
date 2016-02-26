#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(12, GPIO.HIGH)
def clean():
    GPIO.cleanup()

def f():
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
def b():
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
def s():
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)


#while True:

#while True:
'''
if 1:
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    time.sleep(5)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(2)
'''
if __name__ == '__main__':
    print 'test car'
    setup()
    f()
    time.sleep(0.5)
    s()
    time.sleep(2)
    b()
    time.sleep(0.5)
    s()
    time.sleep(2)
    clean()
