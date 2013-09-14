#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorCamaraPos(sensor.Sensor):

    u = None
    i = None
    key = None

    def __init__(self, data, usb4b, lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        self.key = 'SensorCamPos::'
        self.nombre = self.key
        self.lock = lock
        self.data.write(self.key + 'pos_x', 511)
        self.data.write(self.key + 'pos_y', 0)

    def action(self):
        self.lock.acquire()
        (x, y) = self.u.getPosicionCamara()
         #             x =#
        self.lock.release()
        print "SensorCamPos::x" + x + " y " + y
        self.data.write(self.key + 'pos_x', x)
        self.data.write(self.key + 'pos_y', y)