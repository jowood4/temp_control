#!/usr/bin/python

import wiringpi2

class led_controller:
        def __init__(self):
                self.dataPin = 1  
                self.clockPin = 3
                self.latch = 0
                
                wiringpi2.wiringPiSetup()
                
                wiringpi2.pinMode(self.latch,1)
                wiringpi2.pinMode(self.dataPin,1)
                wiringpi2.pinMode(self.clockPin,1)

                wiringpi2.digitalWrite(self.dataPin,0)
                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latch,0)

        def read_temp(self):
                wiringpi2.digitalWrite(self.latch,0)
                for i in range(16):
                    #wiringpi2.digitalWrite(self.clockPin,0)
                    wiringpi2.shiftIn(self.dataPin, self.clockPin, 0)
                    #print int(self.led_matrix[i,j])
                    #wiringpi2.digitalWrite(self.dataPin,int(string[k]))
                    #wiringpi2.digitalWrite(self.clockPin,1)

                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latch,1)
