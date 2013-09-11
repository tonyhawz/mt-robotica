#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorDistancia(sensor.Sensor):

    u = None
    i = None
    key = None

    def __init__(self,data,usb4b,indice,lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        self.i = indice
        self.key = 'SensorDistancia::' + str(config.idDist)
        self.nombre = self.key
        self.lock = lock

    def action(self) :
        self.lock.acquire()
        tmp = self.u.getDistance(config.idDist)
        self.lock.release()
        print ("Distancia :: " + str(tmp))
        self.data.write(self.key, tmp)


