#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np 
import sensor
import config

class SensorCamera(sensor.Sensor):
    
    capture = None
    video = None
    zeros = None
            
    def __init__(self, data, lock):
        sensor.Sensor.__init__(self, data)
        self.key = 'SensorVision::init'
        self.lock = lock
        #self.capture = cv.CaptureFromCAM (config.camara)
        self.video = cv2.VideoCapture(config.camara)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, config.ancho);
        
	self.data.write('Camara::area', 0)
	self.data.write('Camara::lata_x', int(0))
 
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, config.alto);
        f, img = self.video.read()
        self.zeros = np.zeros(img.shape,np.uint8)


    def action(self) :
        f, img = self.video.read()
        old_zeros = self.zeros 
        self.zeros = np.zeros(img.shape,np.uint8)
    	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
        
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        img_bw = cv2.inRange(img_hsv, config.min_hsv_arena,config.max_hsv_arena)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(10,3)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(img_bw.shape,np.uint8)
        cajas = []
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            w,h = rect[1]
            rect = (rect[0],(w*1.5,h*1.5),rect[2])
            box = cv2.cv.BoxPoints(rect)
            box = np.int32(np.around(box))
            #cv2.drawContours(mask,[box],0,255,-1)
            #cv2.drawContours(img,[box],0,255,1)
            cv2.drawContours(img_hsv,[box],0,(255,255,255),-1)
            cajas.append(box)
        #mean = cv2.mean(img,mask = img_bw)
        #mask = cv2.bitwise_not(mask)
        #masked = cv2.bitwise_and(img_hsv,img_hsv,mask=mask)
        #cv2.drawContours(masked,cajas,-1,(255,255,255),-1)
        cv2.drawContours(img_hsv,cajas,-1,(255,255,255),-1) 
        #img_bw = cv2.inRange(masked, config.min_hsv_negro,config.max_hsv_negro)
        img_bw = cv2.inRange(img_hsv, config.min_hsv_negro,config.max_hsv_negro)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
        cv2.drawContours(img,contours,-1,(0,0,0),-1)
	
        c = None
        x_old,y_old = (0,0)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 600:
                rect = cv2.minAreaRect(cnt)
                #w,h = rect[1]
                #rect = (rect[0],(w*1.5,h*1.5),rect[2])
                box = cv2.cv.BoxPoints(rect)
                box = np.int32(np.around(box))
                cv2.drawContours(img,[box],0,(0,0,255),1) 
                #cv2.drawContours(self.zeros,[box],0,(255,255,255),-1)
                cv2.drawContours(self.zeros,[box],0,255,-1)
                x,y = rect[0]
                if y > y_old :
                    c = box
                    y_old = y
                    x_old = x
        
        mask =  cv2.bitwise_and(self.zeros,old_zeros)
        #masked = cv2.bitwise_and(img_hsv,img_hsv,mask=mask)
        #ret,thresh = cv2.threshold(masked,127,255,0)
        #contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img,[c],0,(0,255,0),3)
        if c != None :
            print ('ENCONTRE'+ str(x_old)) 
            #self.data.write('Camara::area', a)
            self.data.write('Camara::lata_x', int(x_old) )
            self.data.write('Camara::lata_y', int(y_old) )
            self.data.write('Camara::encontro', 'TRUE')
            #if  x_old >  config.min_x and x_old  < config.max_x 
        else :
            self.data.write('Camara::encontro', 'FALSE')
            self.data.write('lata::disponible', 0)
        v = cv2.waitKey(50) % 0x100
        #cv2.imshow("ventana",cu.join_images(img_dilated,masked))
        #cv2.imshow("ventana",cu.join_images(img,masked))
        if config.display :
            cv2.imshow("ventana",img)

    def run(self) :
        self.stopped = False
        while not self.stopped :
            self.action() 
#            time.sleep(self.refresh_rate)
