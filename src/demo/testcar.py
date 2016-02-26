#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import curses                                                                                                                                                       
from curses import wrapper 
stdscr = curses.initscr()   
stdscr.clear() 
stdscr.scrollok(True)

class Wheel(object):
    def __init__(self, in_pin1, in_pin2, enable_pin1, enable_pin2):
        '''
        :param in_pin1 in_pin2: IN1 IN2 or IN3 IN4
        :param enable_pin1 enable_pin2: ENA or ENB
        '''
        self.pin1 = in_pin1
        self.pin2 = in_pin2

        # setup I/O OUT
        gpio.setup(in_pin1, gpio.OUT)
        gpio.setup(in_pin2, gpio.OUT)
        gpio.setup(enable_pin1, gpio.OUT)
        gpio.setup(enable_pin2, gpio.OUT)

        # disable
        gpio.output(enable_pin1, gpio.LOW)
        gpio.output(enable_pin2, gpio.LOW) 
        

    def forward(self):
        gpio.output(self.pin1, gpio.HIGH)
        gpio.output(self.pin2, gpio.LOW)

    def backward(self):
        gpio.output(self.pin1, gpio.LOW)
        gpio.output(self.pin2, gpio.HIGH)

    def stop(self):
        gpio.output(self.pin1, gpio.LOW)
        gpio.output(self.pin2, gpio.LOW)  


PWM_FRQ = 30		
ENA_PIN = 7
ENB_PIN = 12
IN1_PIN = 11
IN2_PIN = 13
IN3_PIN = 16
IN4_PIN = 18

class Car(object):

    def __init__(self):   		
        gpio.setmode(gpio.BOARD)

        self.left_wheel = Wheel(IN1_PIN, IN2_PIN, ENA_PIN, ENA_PIN)
        self.right_wheel = Wheel(IN3_PIN, IN4_PIN, ENB_PIN, ENB_PIN)
        
        self.pwma = gpio.PWM(ENA_PIN, PWM_FRQ)
        self.pwmb = gpio.PWM(ENB_PIN, PWM_FRQ)
        self.pwma.start(0)
        self.pwmb.start(0)

    def forward(self, dc = 10):
        self.pwma.ChangeDutyCycle(dc)
        self.pwmb.ChangeDutyCycle(dc)
        self.left_wheel.forward()
        self.right_wheel.forward()

    def backward(self, dc = 10):
        self.pwma.ChangeDutyCycle(dc)
        self.pwmb.ChangeDutyCycle(dc)
        self.left_wheel.backward()
        self.right_wheel.backward()

    def right(self, dc = 10):
        self.left_wheel.stop()
        self.right_wheel.forward()

    def left(self, dc = 10):
        self.left_wheel.forward()
        self.right_wheel.stop()

    def stop(self):
        self.left_wheel.stop()
        self.right_wheel.stop()
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)

    def shutdown(self):
        self.stop()
        self.pwma.stop()
        self.pwmb.stop()
        gpio.cleanup()

def exit_curses():        
    curses.nocbreak()    
    stdscr.keypad(0)    
    curses.echo()      
    curses.endwin()  
            
if __name__ == '__main__':                                                                                                                                          
    print 'test car' 
    DC_STEP = 10
    curses.noecho()   
    car = Car()
    cur_dc = 10 
    cur_key = 'n'                                                                                                                                             
    while True:  
        try:                                                                                                                                                   
            ch = stdscr.getkey()  
        except KeyboardInterrupt:
            stdscr.addstr("Force Exit!\n")   
            stdscr.refresh()           
            car.shutdown()   

        if ch == 'w':                    
            stdscr.addstr("Forward \n") 
            stdscr.refresh() 
            if (cur_key == 's'):
                cur_dc = 0
            if (cur_key == 'w'):                                                                                        
                cur_dc =  cur_dc + DC_STEP  
            if cur_dc >= 100 :
                cur_dc = 100
            cur_key = 'w' 
            car.forward(cur_dc)    

        if ch == 's': 
            stdscr.addstr("Backward \n")       
            stdscr.refresh()   
            if (cur_key == 'w'):
                cur_dc = 0
            if (cur_key == 's'):                                                                                        
                cur_dc =  cur_dc + DC_STEP  
            if cur_dc >= 100 :
                cur_dc = 100
            cur_key = 's' 
            car.backward(cur_dc)   

        if ch == 'a':                         
            stdscr.addstr("Left \n")                                                                                                                              
            stdscr.refresh()                                                                                                                                     
            car.left(cur_dc)  

        if ch == 'd':                        
            stdscr.addstr("Right \n")                                                                                                                              
            stdscr.refresh()                
            car.right(cur_dc)  

        if ch == 'p':                      
            stdscr.clear() 
            stdscr.addstr("Stop \n")                                                                                                                              
            stdscr.refresh()              
            cur_dc = 0
            car.stop()     

        if ch == 'c':                        
            stdscr.clear() 

        if ch == 'q':    
            stdscr.clear() 
            stdscr.addstr("Shutdown exit\n")
            stdscr.refresh()               
            car.shutdown()                
            break      

    exit_curses()      
    print 'Exit car test!'                                                                                                                                             


