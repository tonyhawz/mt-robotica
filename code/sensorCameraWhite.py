#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import cv2
import numpy as np 
import sensor
import config
from data import Data
import camera_utils  as cu 
import time

class SensorCameraWhite(sensor.Sensor):
    
    capture = None
    video = None
    zeros = None
            
    detectar_tacho = True
    dibujar_area = False

    def __init__(self, data, lock):
        sensor.Sensor.__init__(self, data)
        self.key = 'SensorVision::init'
        self.lock = lock
        self.video = cv2.VideoCapture(config.camara)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, config.ancho);
        self.data.write('Camara::area', 0)
        self.data.write('Camara::lata_x', int(0))
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, config.alto);
        f, img = self.video.read()
        if not f :
            print ("nO ENCARO")
        img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        self.zeros = np.zeros(img_bw.shape,np.uint8)
        self.shape =  img_bw.shape
        self.display = config.display or config.dual_display
        # self.resize = False
        self.data.write('Camara::tacho_x', 0)
        self.data.write('Camara::tacho_y', 0)
        self.data.write('Camara::tacho', 'FALSE')


    # def enable_resize(self) :
        # self.resize = True
        # shape = self.zeros.shape
        # shape[0] = config.ancho
        # shape[1] = config.alto
        # self.zeros = np.zeros(shape,np.uint8)       

    def run(self) :
        self.stopped = False
        while not self.stopped :
            self.action() 
            v = cv2.waitKey(50) % 0x100
            #time.sleep(self.refresh_rate)

    def detectar_contornos(self,img_hsv,_min,_max,_mask=None):
        img_bw = cv2.inRange(img_hsv, _min,_max)
        if _mask != None:
            img_bw = cv2.bitwise_and(img_bw,img_bw,mask=_mask)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(10,3)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def action(self) :
        ti = time.time() 
        f, img = self.video.read()
        # if self.resize and f:
            # img = cv2.resize(img,(config.ancho,config.alto))
        old_zeros = self.zeros 
        self.zeros = np.zeros(self.shape,np.uint8)
    	#img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
        
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        
        contours = self.detectar_contornos(img_hsv,config.min_hsv_blanc,config.max_hsv_blanc)
        '''
        img_bw = cv2.inRange(img_hsv, config.min_hsv_blanc,config.max_hsv_blanc)
        img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(10,3)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        '''
        #mask_white = np.zeros(img.shape,np.uint8)
        mask_white = np.zeros(self.shape,np.uint8)

        cajas = []
        big_cnt_white = None
        big_cnt_white_area = 0
        for cnt in contours:
            #approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
            approx = cv2.convexHull(cnt)
            area_tmp = cv2.contourArea(approx)
            #print area_tmp
            if big_cnt_white_area < area_tmp :
                big_cnt_white = approx
                big_cnt_white_area = area_tmp
                #print 'encontre'
        if big_cnt_white != None :
            #cv2.drawContours(img,contours,0,(0,0,255),-1)
            cv2.drawContours(mask_white,[big_cnt_white],0,(255,0,0),-1)
            cv2.drawContours(img,[big_cnt_white],0,(255,255,0),3)
            #rect = cv2.minAreaRect(cnt)
            #w,h = rect[1]
            #rect = (rect[0],(w*1.5,h*1.5),rect[2])
            #box = cv2.cv.BoxPoints(rect)
            #box = np.int32(np.around(box))
            #cv2.drawContours(mask,[box],0,255,-1)
            #cv2.drawContours(img,[box],0,255,1)
            #cv2.drawContours(img_hsv,[box],0,(255,255,255),-1)
            #cajas.append(box)
        #mean = cv2.mean(img,mask = img_bw)
        #mask = cv2.bitwise_not(mask)
        
        contours = self.detectar_contornos(img_hsv,config.min_hsv_negro,config.max_hsv_negro,mask_white)
        
        '''
        img_bw = cv2.inRange(img_hsv, config.min_hsv_negro,config.max_hsv_negro)
        masked = cv2.bitwise_and(img_bw,img_bw,mask=mask_white)
        img_eroded = cv2.erode(masked,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
        '''
        '''
        img_bw = cv2.inRange(img_hsv, config.min_hsv_negro,config.max_hsv_negro)
        print img_bw
        #img_bw = cv2.inRange(masked, config.min_hsv_negro,config.max_hsv_negro)
        masked = cv2.bitwise_and(img_bw,img_bw,mask=mask_white)
  
        #img_eroded = cv2.erode(img_bw,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        img_eroded = cv2.erode(masked,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        img_dilated = cv2.erode(img_eroded,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
        ret,thresh = cv2.threshold(img_dilated,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
       '''
        cv2.drawContours(img,contours,-1,(0,0,0),-1)
        
        c = None
        x_old,y_old = (0,0)

        # dibujar todos los contornos en amarillo
        if self.display:
            cv2.drawContours(img,contours,-1,(0,255,255),1)

        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int32(np.around(box))
            cv2.drawContours(self.zeros,[box],0,255,-1)
        
        mask =  cv2.bitwise_and(self.zeros,old_zeros)
        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img,contours,-1,(0,0,255),1)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            #print area
            if area > config.min_area:
                self.data.write('Camara::area', area)
                rect = cv2.minAreaRect(cnt)
                box = cv2.cv.BoxPoints(rect)
                box = np.int32(np.around(box))
                cv2.drawContours(self.zeros,[box],0,255,-1)
                x,y = rect[0]
                if self.dibujar_area and self.display:
                    cv2.putText(img,str(area)+' px',(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255))
                if y > y_old :
                    c = box
                    y_old = y
                    x_old = x
        
        if self.display:
            cv2.drawContours(img,[c],0,(0,255,0),3)

        if c != None :
            #print ('ENCONTRE'+ str(x_old)) 
            #self.data.write('Camara::area', a)
            self.data.write('Camara::lata_x', int(x_old) )
            self.data.write('Camara::lata_y', int(y_old) )
            self.data.write('Camara::encontro', 'TRUE')
            #if  x_old >  config.min_x and x_old  < config.max_x 
        else :
            self.data.write('Camara::encontro', 'FALSE')
            self.data.write('lata::disponible', 0)
        
        if self.detectar_tacho :
            contours = self.detectar_contornos(img_hsv,config.min_hsv_tacho,config.max_hsv_tacho,mask_white)
            old_area = 0
            old_cnt = None
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100 and old_area < area :
                    old_cnt = cnt
                    old_area = area 
            if old_cnt != None:
                if self.display:
                    cv2.drawContours(img,[old_cnt],0,(0,0,255),-1)
                rect = cv2.minAreaRect(cnt)
                x,y = rect[0]
                self.data.write('Camara::tacho', 'TRUE')
                self.data.write('Camara::tacho_x', x)
                self.data.write('Camara::tacho_y', y)
            else:
                self.data.write('Camara::tacho', 'FALSE')
            
        if config.display and not config.dual_display :
            cv2.imshow("ventana",img)
        if config.dual_display :
            cv2.imshow("ventana", cu.join_images(mask,img)) 
        tf = time.time()
        delta_t = tf - ti
        # print 'SensorCameraWhite::action ' + str(delta_t)

    def getNombre(self): 
        return 'SensorCameraWhite'

def main():
    data = Data() 
    lock = None
    config.camara = '../video-2013-07-09-1373414462.avi'
    config.camara = '../video-2013-07-09-1373414439.avi'
    config.camara = '../video-2013-07-09-1373413875.avi'
    #config.camara = '../video2013-07-09.avi'
    #config.camara = '../video-2013-07-09-1373413843.avi'
    #config.camara = '../video7.avi'
    config.camara = 0
    config.display = True
    config.dual_display = True
    m = SensorCameraWhite(data , lock) 
    m.dibujar_area = True
    m.detectar_tacho = True
    # m.enable_resize() 
    while True:
        m.action()
        v = cv2.waitKey(50) % 0x100
        if v == 27 :
            break
    while True and False:
        m.action()
        time.sleep(.1)
   # m.run()


if __name__ == "__main__":
    main ()

