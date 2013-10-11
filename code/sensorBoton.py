#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorBoton(sensor.Sensor):

    u = None
    i = None
    key = None

    #def __init__(self, data, usb4b, indice, lock):
    def __init__(self, data, usb4b, lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        #self.i = indice
        self.key = 'SensorBoton::' + str(config.idBoton)
        self.data.write(self.key, -1)
        self.nombre = self.key
        self.lock = lock

    def action(self) :
        self.lock.acquire()
        #butia.getButton(6, 0)
        bot = self.u.getButton(config.idBoton)
        self.lock.release()
        #print ("boton :: " + str(bot))
        self.data.write(self.key, bot)


