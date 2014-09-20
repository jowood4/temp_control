#!/usr/bin/python

import wiringpi2

class thermocouple:
        def __init__(self):

	def setup(self, data, clock, latch):
                self.dataPin = data 
                self.clockPin = clock
                self.latchPin = latch
                
                wiringpi2.wiringPiSetup()
                
                wiringpi2.pinMode(self.latch,1)
                wiringpi2.pinMode(self.dataPin,1)
                wiringpi2.pinMode(self.clockPin,1)

                wiringpi2.digitalWrite(self.dataPin,0)
                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latch,0)

        def read_temp(self):
                data = list()
                wiringpi2.digitalWrite(self.latchPin,0)
                for i in range(4):
                    #wiringpi2.digitalWrite(self.clockPin,0)
                    data.append(wiringpi2.shiftIn(self.dataPin, self.clockPin, 0))
                    #print int(self.led_matrix[i,j])
                    #wiringpi2.digitalWrite(self.dataPin,int(string[k]))
                    #wiringpi2.digitalWrite(self.clockPin,1)

                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latchPin,1)
                
                self.thermocouple_temp = (data[0]<<4) + (data[1]>>2)
                self.fault = data[1] & 0x01
                self.chip_temp = (data[2]<<4) + (data[3]>>2)
                self.scv_fault = data[3] & 0x04
                self.scg_fault = data[3] & 0x02
                self.oc_fault = data[3] & 0x01
