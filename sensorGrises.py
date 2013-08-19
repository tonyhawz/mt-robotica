#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sensor
import config
import time

from pybot import usb4butia

class SensorGrises(sensor.Sensor):
    
    buf = None
#    max_len = 5
    u = None 
    i = None
    key = None
    
    def __init__(self,data,usb4b,indice,lock):
        sensor.Sensor.__init__(self, data)
        self.buf = []
        self.u = usb4b
        self.i = indice
        self.key = 'SensorGrises::' + str(indice)
        self.nombre = self.key
        self.lock = lock
        #data.lock()
        #data.write(self.key,-1)
        #data.unlock()

    def action(self) :
        self.lock.acquire()
	ti = time.time()
        tmp = self.u.getGray(self.i)
        self.lock.release()
        if (isinstance(tmp, int)):
            self.buf.append(tmp)        
            # if len(self.buf) > self.max_len:
            if len(self.buf) > config.max_len:
                self.buf.pop(0)
            valor = sum(self.buf) / len(self.buf)
            # self.data.lock()
            self.data.write(self.key,valor)
        # self.data.unlock() 
        tf = time.time()
        print (tf - ti)
        #print 'SensorGrises time ' + str(tf-ti)

    
