#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import sensor
import config

class SensorVision(sensor.Sensor):

    capture = None
    
    def __init__(self, data, lock):
        sensor.Sensor.__init__(self, data)
        self.key = 'SensorVision::init'
        self.lock = lock
        self.delay = 0
        self.capture = cv.CaptureFromCAM (config.camara)
        cv.SetCaptureProperty (self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, config.ancho)
        cv.SetCaptureProperty (self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, config.alto)

    def action(self) :
        if (not (self.delay == 5)):
            self.delay += 1
        else:
            self.delay = 0
            frame = cv.QueryFrame (self.capture)
            maskN = cv.CreateImage (cv.GetSize (frame), 8, 1)
            hsvN = cv.CloneImage (frame)

            cv.Smooth (frame, frame, cv.CV_BLUR, 3)

            cv.CvtColor (frame, hsvN, cv.CV_BGR2HSV)
            cv.InRangeS (hsvN, config.min_range, config.max_range, maskN)

            moment = cv.Moments (cv.GetMat (maskN), 0)
            a = cv.GetCentralMoment (moment, 0, 0)
            if a == 0 :
                a = 1

            self.data.write('Camara::area', a)
            self.data.write('Camara::lata_x', int( cv.GetSpatialMoment (moment, 1, 0) / a ) )

            cv.WaitKey (10)

