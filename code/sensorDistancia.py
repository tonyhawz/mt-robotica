#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config

from pybot import usb4butia

class SensorDistancia(sensor.Sensor):

    u = None
    i = None
    key_izq = None
    key_der = None
    buf_izq = None
    buf_der = None
    max_len = 5

    def __init__(self,data,usb4b,indice,lock):
        sensor.Sensor.__init__(self, data)
        self.u = usb4b
        self.i = indice
        self.key_izq = 'SensorDistancia::' + str(config.idDistIzq)
        self.key_der = 'SensorDistancia::' + str(config.idDistDer)
        self.nombre = 'SensorDistancia'
        self.lock = lock
        self.data.write(self.key_izq, 0)
        self.data.write(self.key_der, 0)
        self.buf_izq = []
        self.buf_der = []

    def action(self) :
        self.lock.acquire()
        tmp_izq = self.u.getDistance(config.idDistIzq)
        tmp_der = self.u.getDistance(config.idDistDer)
        self.lock.release()
        if (isinstance(tmp_izq, int)):
            self.buf_izq.append(tmp_izq)
            if len(self.buf_izq) > config.max_len:
                self.buf_izq.pop(0)
            valor = sum(self.buf_izq) / len(self.buf_izq)
            # self.data.lock()
            self.data.write(self.key_izq,valor)
        if (isinstance(tmp_der, int)):
            self.buf_der.append(tmp_der)
            if len(self.buf_der) > config.max_len:
                self.buf_der.pop(0)
            valor = sum(self.buf_der) / len(self.buf_der)
            self.data.write(self.key_der,valor)

        #print ("Distancia :: IZQ" + str(tmp_izq) +" DER "+ str(tmp_der))



