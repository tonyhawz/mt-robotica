#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorCamaraPos(sensor.Sensor):

    u = None
    i = None
    key = None

    def __init__(self, data, usb4b, indice, lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        self.i = indice
        self.key = 'SensorCamPos::'
        self.nombre = self.key
        self.lock = lock

    def action(self):
        self.lock.acquire()
        (x, y) = self.u.getPosicionCamara()
        self.lock.release()
        print "SensorCamPos::x" + x + " y " + y
        self.data.write(self.key + 'pos_x', x)
        self.data.write(self.key + 'pos_y', y)