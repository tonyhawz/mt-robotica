#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorCamaraPos(sensor.Sensor):

    u = None
    i = None
    key = None

    def __init__(self, data, motor, lock):
        sensor.Sensor.__init__(self, data)
        self.u = motor
        self.key = 'SensorCamPos::'
        self.nombre = self.key
        self.lock = lock
        self.data.write(self.key + 'pos_x', 511)
        self.data.write(self.key + 'pos_y', 0)

    def action(self):
        self.lock.acquire()
        (x, y) = self.u.get_posicion_camara()
        self.lock.release()
        #print "SensorCamPos::x" + str(x) + " y " + str(y)
        self.data.write(self.key + 'pos_x', x)
        self.data.write(self.key + 'pos_y', y)