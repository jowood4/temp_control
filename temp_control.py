#!/usr/bin/python

import thermocouple
import wiringpi2

class temp_control:
        def __init__(self):
                SPI_data = 16
                SPI_clock = 21
                SPI_latch = 20
                self.heat_relay = 12

                wiringpi2.wiringPiSetup()

                self.thermocouple = thermocouple.thermocouple()
                self.thermocouple.setup(SPI_data, SPI_clock, SPI_latch)

                self.relay_state = 0
                wiringpi2.pinMode(self.heat_relay,1)
                wiringpi2.digitalWrite(self.heat_relay, self.relay_state)

        def relay_on(self):
                wiringpi2.digitalWrite(self.heat_relay,1)

        def relay_off(self):
                wiringpi2.digitalWrite(self.heat_relay,0)

        def read_thermo_temp(self):
                self.thermocouple.read_temp()
                return self.thermocouple.thermocouple_temp * 0.25

        def regulate_temp(self, set_temp):
                delta = 1
                timeout = 20

                for i in range(timeout):
                        read_temp = self.read_thermo_temp()
                        print read_temp
                        self.relay_off()

                        if(read_temp <= set_temp - delta):
                                self.relay_on()
                                print('Relay ON')
                                wiringpi2.delay(100)
                                self.relay_off()
                                wiringpi2.delay(2000)
                        elif(read_temp >= set_temp - delta):
                                self.relay_off()
                                print('Relay Off')

                        wiringpi2.delay(100)

                self.relay_off()
                
                
                
