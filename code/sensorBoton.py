#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorBoton(sensor.Sensor):
    
    u = None 
    i = None
    key = None
    
    def __init__(self, data, usb4b, indice, lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        self.i = indice
        self.key = 'SensorBoton::' + str(config.idBoton)
        self.data.write(self.key, 0)
        self.nombre = self.key
        self.lock = lock

    def action(self) :
        self.lock.acquire()
#        butia.getButton(6, 0)
        bot = self.u.getButton(6)
        self.lock.release()
        print ("boton :: " + str(bot))
        self.data.write(self.key, bot)

    
