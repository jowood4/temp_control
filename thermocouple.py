#!/usr/bin/python

import wiringpi2

class thermocouple:
        def __init__(self):
                self.data = 0
        def setup(self, data, clock, latch):
                self.dataPin = data 
                self.clockPin = clock
                self.latchPin = latch
                
                wiringpi2.wiringPiSetupGpio()
                
                wiringpi2.pinMode(self.latchPin,1)
                wiringpi2.pinMode(self.dataPin,0)
                wiringpi2.pinMode(self.clockPin,1)

##                wiringpi2.digitalWrite(self.dataPin,0)
                wiringpi2.digitalWrite(self.clockPin,0)
                wiringpi2.digitalWrite(self.latchPin,1)

        def read_temp(self):
                
                data = self.spi_shift()
                self.thermocouple_temp = (data[0]<<6) + (data[1]>>2)
                self.fault = data[1] & 0x01
                self.chip_temp = (data[2]<<4) + (data[3]>>4)
                self.scv_fault = data[3] & 0x04
                self.scg_fault = data[3] & 0x02
                self.oc_fault = data[3] & 0x01

        def spi_shift(self):
                data = list()
                wiringpi2.digitalWrite(self.latchPin,0)
                for i in range(4):
                        temp_data = 0
                        for j in range(8):
                                bit = wiringpi2.digitalRead(self.dataPin)
                                temp_data = temp_data + (pow(2,7-j) * bit)
                                wiringpi2.digitalWrite(self.clockPin,1)
                                wiringpi2.digitalWrite(self.clockPin,0)
                        data.append(temp_data)
                wiringpi2.digitalWrite(self.latchPin,1)
                return data
