#!/usr/bin/python

import thermocouple
import wiringpi2

class temp_control:
	def __init__(self):
		SPI_data = 1
		SPI_clock = 2
		SPI_latch = 0
		self.heat_relay = 3

		wiringpi2.wiringPiSetup()

		self.thermocouple = thermocouple.thermocouple()
		self.setup(SPI_data, SPI_clock, SPI_latch)

		wiringpi2.pinMode(self.heat_relay,1)
		wiringpi2.digitalWrite(self.heat_relay,0)

	def relay_on(self):
		wiringpi2.digitalWrite(self.heat_relay,1)

	def relay_off(self):
		wiringpi2.digitalWrite(self.heat_relay,0)

		
		
